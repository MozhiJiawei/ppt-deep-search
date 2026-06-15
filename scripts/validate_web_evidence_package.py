#!/usr/bin/env python3
"""Validate HTML review mappings to web-article-capture source packages."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
SCREENSHOT_NAME_FRAGMENTS = (
    "screenshot",
    "full-page",
    "fullpage",
    "page-full",
    "article-region",
    "rendered-evidence",
)


def _is_obj(value: Any) -> bool:
    return isinstance(value, dict)


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _is_http_url(value: Any) -> bool:
    text = str(value or "").strip().lower()
    return text.startswith("http://") or text.startswith("https://")


def _resolve_artifact_path(path_value: str, base_dir: Path) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    if path.parts and path.parts[0] in {"sources", "review", "baselines", "QA"}:
        return base_dir.parent / path
    return base_dir / path


def _files_with_ext(directory: Path, extensions: set[str]) -> list[Path]:
    if not directory.exists():
        return []
    return [path for path in directory.rglob("*") if path.is_file() and path.suffix.lower() in extensions]


def _looks_like_screenshot(path: Path) -> bool:
    text = path.as_posix().lower()
    return any(fragment in text for fragment in SCREENSHOT_NAME_FRAGMENTS)


def _markdown_image_refs(source_md: Path) -> list[str]:
    if not source_md.exists():
        return []
    text = source_md.read_text(encoding="utf-8", errors="replace")
    refs: list[str] = []
    for match in MARKDOWN_IMAGE_RE.finditer(text):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1].strip()
        target = target.split()[0].strip()
        if target.startswith(("http://", "https://", "#")):
            continue
        if target:
            refs.append(target)
    return refs


def _original_image_files(images_dir: Path) -> list[Path]:
    """Return downloaded webpage image assets, excluding page-capture files."""

    return [
        path
        for path in _files_with_ext(images_dir, IMAGE_EXTENSIONS)
        if not _looks_like_screenshot(path)
    ]


def _capture_mapping(citation: dict[str, Any]) -> dict[str, Any] | None:
    capture = citation.get("web_capture")
    if _is_obj(capture):
        return capture
    return None


def validate_report_data(
    data: Any,
    base_dir: Path,
    *,
    require_images: str,
    min_image_sources: int,
) -> list[str]:
    errors: list[str] = []
    if not _is_obj(data):
        return ["Top-level JSON value must be an object"]

    image_source_count = 0
    for idx, citation in enumerate(_as_list(data.get("citations"))):
        if not _is_obj(citation) or not _is_http_url(citation.get("url")):
            continue

        cid = str(citation.get("id") or idx)
        capture = _capture_mapping(citation)
        if not capture:
            errors.append(f"web citation {cid} missing web_capture package mapping")
            continue

        package_value = str(capture.get("package_path") or "").strip()
        source_value = str(capture.get("source_md") or "").strip()
        images_value = str(capture.get("images_dir") or "").strip()
        if not package_value:
            errors.append(f"web citation {cid} missing web_capture.package_path")
            continue

        package_dir = _resolve_artifact_path(package_value, base_dir)
        source_md = _resolve_artifact_path(source_value or f"{package_value}/source.md", base_dir)
        images_dir = _resolve_artifact_path(images_value or f"{package_value}/images", base_dir)
        if not package_dir.exists() or not package_dir.is_dir():
            errors.append(f"web citation {cid} package_path does not exist or is not a directory: {package_value}")
            continue
        if not source_md.exists() or source_md.name.lower() != "source.md":
            errors.append(f"web citation {cid} source_md must point to an existing source.md: {source_value or package_value + '/source.md'}")
        if not images_dir.exists() or not images_dir.is_dir():
            errors.append(f"web citation {cid} images_dir must point to an existing images/ directory: {images_value or package_value + '/images'}")
            continue
        package_resolved = package_dir.resolve()
        for label, path in (("source_md", source_md), ("images_dir", images_dir)):
            try:
                path.resolve().relative_to(package_resolved)
            except ValueError:
                errors.append(f"web citation {cid} {label} must stay inside package_path: {path}")

        for ref in _markdown_image_refs(source_md):
            ref_path = Path(ref)
            if ref_path.is_absolute() or ".." in ref_path.parts:
                errors.append(f"web citation {cid} source.md image reference must stay inside the package: {ref}")
                continue
            resolved_ref = (source_md.parent / ref_path).resolve()
            try:
                resolved_ref.relative_to(package_dir.resolve())
            except ValueError:
                errors.append(f"web citation {cid} source.md image reference points outside package: {ref}")
                continue
            if not resolved_ref.exists():
                errors.append(f"web citation {cid} source.md references missing image: {ref}")

        original_image_files = _original_image_files(images_dir)
        if original_image_files:
            image_source_count += 1
        if require_images == "always" and not original_image_files:
            errors.append(f"web citation {cid} missing original webpage image files under images/")
        if require_images == "when-indexed" and _markdown_image_refs(source_md) and not original_image_files:
            errors.append(f"web citation {cid} source.md references images but images/ has no usable original image files")

    if min_image_sources and image_source_count < min_image_sources:
        errors.append(f"expected at least {min_image_sources} web sources with downloaded original webpage images, found {image_source_count}")

    return errors


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        review = root / "review"
        src = root / "sources" / "web" / "good"
        (src / "images").mkdir(parents=True)
        review.mkdir()
        (src / "source.md").write_text(
            '# Example\n\nSource: https://example.com\n\n![Hero](images/hero.png "title")\n![Hero2](<images/hero.png>)\n',
            encoding="utf-8",
        )
        (src / "images" / "hero.png").write_bytes(b"\x89PNG\r\n")

        good = {
            "citations": [{
                "id": "s1",
                "url": "https://example.com",
                "web_capture": {
                    "package_path": "sources/web/good",
                    "source_md": "sources/web/good/source.md",
                    "images_dir": "sources/web/good/images",
                },
            }]
        }
        bad = {
            "citations": [{
                "id": "s2",
                "url": "https://example.com",
                "web_capture": {
                    "package_path": "sources/web/missing",
                    "source_md": "sources/web/missing/source.md",
                    "images_dir": "sources/web/missing/images",
                },
            }]
        }
        missing_image = {
            "citations": [{
                "id": "s3",
                "url": "https://example.com",
                "web_capture": {
                    "package_path": "sources/web/missing-image",
                    "source_md": "sources/web/missing-image/source.md",
                    "images_dir": "sources/web/missing-image/images",
                },
            }]
        }
        missing_image_src = root / "sources" / "web" / "missing-image"
        (missing_image_src / "images").mkdir(parents=True)
        (missing_image_src / "source.md").write_text("# Example\n\n![Missing](images/missing.png)\n", encoding="utf-8")
        good_errors = validate_report_data(good, review, require_images="always", min_image_sources=1)
        bad_errors = validate_report_data(bad, review, require_images="never", min_image_sources=0)
        missing_image_errors = validate_report_data(missing_image, review, require_images="when-indexed", min_image_sources=0)
        if good_errors:
            print("[ERROR] valid fixture failed:")
            print("\n".join(good_errors))
            return 1
        if not any("package_path does not exist" in error for error in bad_errors):
            print("[ERROR] invalid fixture did not reject missing package:")
            print("\n".join(bad_errors))
            return 1
        if not any("missing image" in error for error in missing_image_errors):
            print("[ERROR] missing-image fixture passed image reference gate:")
            print("\n".join(missing_image_errors))
            return 1
    print("[OK] Web capture mapping self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate web-article-capture source packages referenced by report-data.json.")
    parser.add_argument("json_file", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--require-images", choices=("never", "when-indexed", "always"), default="when-indexed")
    parser.add_argument("--min-image-sources", type=int, default=0, help="Require images from at least this many cited webpage source packages.")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.json_file is None:
        parser.error("json_file is required unless --self-test is used")

    try:
        data = json.loads(args.json_file.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[ERROR] Failed to read JSON: {exc}")
        return 1

    errors = validate_report_data(
        data,
        args.json_file.parent,
        require_images=args.require_images,
        min_image_sources=args.min_image_sources,
    )
    if errors:
        print("[ERROR] Web capture mapping QA failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("[OK] Web capture mapping QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
