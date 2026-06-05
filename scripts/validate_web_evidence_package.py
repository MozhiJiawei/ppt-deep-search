#!/usr/bin/env python3
"""Validate rendered webpage evidence packages for HTML source reviews."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any


BAD_CAPTURE_FRAGMENTS = (
    "raw capture",
    "raw html",
    "web search",
    "search-result",
    "browser-use tool unavailable",
    "browser unavailable",
    "unavailable in this turn",
    "curl",
    "invoke-webrequest",
    "playwright script",
    "custom playwright",
    "puppeteer",
    "selenium",
    "third-party crawler",
    "crawl4ai",
    "firecrawl",
    "singlefile",
)

GOOD_CAPTURE_FRAGMENTS = (
    "codex browser",
    "in-app browser",
    "browser plugin",
    "browser-use",
)

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
SCREENSHOT_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
IMAGE_MANIFEST_NAMES = ("images.json", "images-manifest.json", "page-assets-inventory.json")
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


def _source_dir_from_local_path(path: Path) -> Path:
    if path.name.lower() in {"article.md", "article.txt", "content.md", "article-text.md"}:
        return path.parent
    return path.parent


def _files_with_ext(directory: Path, extensions: set[str]) -> list[Path]:
    if not directory.exists():
        return []
    return [path for path in directory.rglob("*") if path.is_file() and path.suffix.lower() in extensions]


def _looks_like_screenshot(path: Path) -> bool:
    text = path.as_posix().lower()
    return any(fragment in text for fragment in SCREENSHOT_NAME_FRAGMENTS)


def _iter_manifest_entries(value: Any) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                entries.append(item)
        return entries
    if not isinstance(value, dict):
        return entries
    for key in ("images", "dom_images", "image_assets", "assets"):
        nested = value.get(key)
        if isinstance(nested, list):
            for item in nested:
                if isinstance(item, dict):
                    entries.append(item)
    return entries


def _manifest_entries(source_dir: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for name in IMAGE_MANIFEST_NAMES:
        manifest_path = source_dir / name
        if not manifest_path.exists():
            continue
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        for entry in _iter_manifest_entries(data):
            entry = dict(entry)
            entry["_manifest_path"] = str(manifest_path)
            entries.append(entry)
    return entries


def _entry_local_path(entry: dict[str, Any], source_dir: Path) -> Path | None:
    for field in ("local_path", "path", "file", "filename"):
        value = str(entry.get(field) or "").strip()
        if not value:
            continue
        path = Path(value)
        if not path.is_absolute():
            path = source_dir / path
        return path
    return None


def _entry_source_url(entry: dict[str, Any]) -> str:
    for field in ("source_url", "url", "src", "currentSrc", "href"):
        value = str(entry.get(field) or "").strip()
        if _is_http_url(value):
            return value
    candidates = entry.get("candidates")
    if isinstance(candidates, list):
        for candidate in candidates:
            value = str(candidate or "").strip()
            if _is_http_url(value):
                return value
    return ""


def _download_status_ok(entry: dict[str, Any]) -> bool:
    status = str(entry.get("download_status") or entry.get("downloadStatus") or entry.get("status") or "").strip().lower()
    return status in {"ok", "saved", "downloaded", "success", "kept", "copied"}


def _original_image_files(source_dir: Path) -> list[Path]:
    """Return downloaded webpage image assets, excluding rendered screenshots."""

    originals: list[Path] = []
    for entry in _manifest_entries(source_dir):
        local_path = _entry_local_path(entry, source_dir)
        source_url = _entry_source_url(entry)
        if not local_path or not source_url:
            continue
        if not local_path.exists() or local_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if _looks_like_screenshot(local_path):
            continue
        if _download_status_ok(entry) or local_path.stat().st_size > 0:
            originals.append(local_path)

    if originals:
        return originals

    # Backward-compatible fallback for older packages that saved original files
    # but did not record local paths in the manifest. Screenshot-like filenames
    # are deliberately excluded so a full-page screenshot cannot masquerade as
    # original webpage art.
    return [
        path
        for path in _files_with_ext(source_dir / "images", IMAGE_EXTENSIONS)
        if not _looks_like_screenshot(path)
    ]


def validate_report_data(
    data: Any,
    base_dir: Path,
    *,
    require_screenshots: bool,
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
        evidence = citation.get("browser_evidence")
        if not _is_obj(evidence):
            errors.append(f"web citation {cid} missing browser_evidence object")
            continue

        capture_method = str(evidence.get("capture_method", "")).strip()
        method_lower = capture_method.lower()
        if not any(fragment in method_lower for fragment in GOOD_CAPTURE_FRAGMENTS):
            errors.append(f"web citation {cid} capture_method must identify Codex in-app Browser / Browser plugin / browser-use capture")
        for fragment in BAD_CAPTURE_FRAGMENTS:
            if fragment in method_lower:
                errors.append(f"web citation {cid} capture_method admits non-rendered fallback: {capture_method}")
                break

        local_value = str(evidence.get("local_path") or "").strip()
        if not local_value:
            errors.append(f"web citation {cid} missing browser_evidence.local_path")
            continue
        local_path = _resolve_artifact_path(local_value, base_dir)
        if not local_path.exists():
            errors.append(f"web citation {cid} local_path does not exist: {local_value}")
            continue
        if local_path.suffix.lower() not in {".md", ".txt", ".json"}:
            errors.append(f"web citation {cid} local_path should point to rendered article text/JSON, not {local_path.name}")

        source_dir = _source_dir_from_local_path(local_path)
        run_log_text = ""
        for log_name in ("run.log", "extraction-log.txt", "capture.log"):
            log_path = source_dir / log_name
            if log_path.exists():
                run_log_text += "\n" + log_path.read_text(encoding="utf-8", errors="replace")
        if run_log_text:
            log_lower = run_log_text.lower()
            if not any(fragment in log_lower for fragment in GOOD_CAPTURE_FRAGMENTS):
                errors.append(f"web citation {cid} run log must name Codex in-app Browser / Browser plugin / browser-use capture")
            for fragment in BAD_CAPTURE_FRAGMENTS:
                if fragment in log_lower:
                    errors.append(f"web citation {cid} run log admits non-native browser capture: {fragment}")
                    break

        expected_article_json = source_dir / "article.json"
        if not expected_article_json.exists():
            alternate_jsons = list(source_dir.glob("*data.json")) + list(source_dir.glob("metadata.json"))
            if not alternate_jsons:
                errors.append(f"web citation {cid} missing structured article metadata JSON in {source_dir}")

        screenshot_values = [
            str(evidence.get("screenshot_path") or "").strip(),
            str(evidence.get("article_region_path") or "").strip(),
            str(evidence.get("fullpage_screenshot_path") or "").strip(),
        ]
        screenshots = [
            _resolve_artifact_path(value, base_dir)
            for value in screenshot_values
            if value
        ]
        screenshots.extend(_files_with_ext(source_dir / "screenshots", SCREENSHOT_EXTENSIONS))
        screenshots.extend(path for path in _files_with_ext(source_dir, SCREENSHOT_EXTENSIONS) if path.name.lower() in {"fullpage.png", "page-full.png", "article-region.png", "fullpage-screenshot.png"})
        existing_screenshots = [path for path in screenshots if path.exists()]
        if require_screenshots and not existing_screenshots:
            errors.append(f"web citation {cid} missing rendered screenshot artifact")

        original_image_files = _original_image_files(source_dir)
        image_manifest_exists = any((source_dir / name).exists() for name in IMAGE_MANIFEST_NAMES)
        if original_image_files:
            image_source_count += 1
        if require_images == "always" and not original_image_files:
            errors.append(f"web citation {cid} missing downloaded original webpage image files under images/; rendered screenshots do not satisfy this gate")
        if require_images == "when-indexed" and image_manifest_exists and not original_image_files:
            errors.append(f"web citation {cid} has image manifest but no downloaded original webpage image files")

    if min_image_sources and image_source_count < min_image_sources:
        errors.append(f"expected at least {min_image_sources} web sources with downloaded original webpage images, found {image_source_count}")

    return errors


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        review = root / "review"
        src = root / "sources" / "web" / "good"
        (src / "images").mkdir(parents=True)
        (src / "screenshots").mkdir()
        review.mkdir()
        (src / "article.md").write_text("Rendered article text", encoding="utf-8")
        (src / "article.json").write_text("{}", encoding="utf-8")
        (src / "screenshots" / "article-region.png").write_bytes(b"\x89PNG\r\n")
        (src / "images" / "hero.png").write_bytes(b"\x89PNG\r\n")
        (src / "images.json").write_text(json.dumps({
            "images": [{
                "url": "https://example.com/hero.png",
                "file": "images/hero.png",
                "downloadStatus": "ok",
            }]
        }), encoding="utf-8")

        good = {
            "citations": [{
                "id": "s1",
                "url": "https://example.com",
                "browser_evidence": {
                    "capture_method": "Codex Browser/browser-use rendered page extraction",
                    "local_path": "sources/web/good/article.md",
                    "screenshot_path": "sources/web/good/screenshots/article-region.png",
                },
            }]
        }
        bad = {
            "citations": [{
                "id": "s2",
                "url": "https://example.com",
                "browser_evidence": {
                    "capture_method": "Custom Playwright script plus raw capture; browser-use tool unavailable",
                    "local_path": "sources/web/good/article.md",
                    "screenshot_path": None,
                },
            }]
        }
        screenshot_only = {
            "citations": [{
                "id": "s3",
                "url": "https://example.com",
                "browser_evidence": {
                    "capture_method": "Codex Browser/browser-use rendered page extraction",
                    "local_path": "sources/web/good/article.md",
                    "screenshot_path": "sources/web/good/screenshots/article-region.png",
                },
            }]
        }
        screenshot_src = root / "sources" / "web" / "screenshot-only"
        (screenshot_src / "images").mkdir(parents=True)
        (screenshot_src / "screenshots").mkdir()
        (screenshot_src / "article.md").write_text("Rendered article text", encoding="utf-8")
        (screenshot_src / "article.json").write_text("{}", encoding="utf-8")
        (screenshot_src / "screenshots" / "full-page.png").write_bytes(b"\x89PNG\r\n")
        (screenshot_src / "images" / "full-page-rendered-evidence.png").write_bytes(b"\x89PNG\r\n")
        screenshot_only["citations"][0]["browser_evidence"]["local_path"] = "sources/web/screenshot-only/article.md"
        screenshot_only["citations"][0]["browser_evidence"]["screenshot_path"] = "sources/web/screenshot-only/screenshots/full-page.png"
        good_errors = validate_report_data(good, review, require_screenshots=True, require_images="always", min_image_sources=1)
        bad_errors = validate_report_data(bad, review, require_screenshots=True, require_images="never", min_image_sources=0)
        screenshot_errors = validate_report_data(screenshot_only, review, require_screenshots=True, require_images="always", min_image_sources=1)
        if good_errors:
            print("[ERROR] valid fixture failed:")
            print("\n".join(good_errors))
            return 1
        if not any("non-rendered fallback" in error for error in bad_errors):
            print("[ERROR] invalid fixture did not reject bad capture method:")
            print("\n".join(bad_errors))
            return 1
        if not any("original webpage image" in error for error in screenshot_errors):
            print("[ERROR] screenshot-only fixture passed image gate:")
            print("\n".join(screenshot_errors))
            return 1
    print("[OK] Web evidence package self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate rendered webpage evidence packages referenced by report-data.json.")
    parser.add_argument("json_file", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--require-screenshots", action="store_true", help="Require each cited webpage to have a rendered page/article screenshot.")
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
        require_screenshots=args.require_screenshots,
        require_images=args.require_images,
        min_image_sources=args.min_image_sources,
    )
    if errors:
        print("[ERROR] Web evidence package QA failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("[OK] Web evidence package QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
