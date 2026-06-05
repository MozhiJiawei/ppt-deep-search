#!/usr/bin/env python3
"""Validate a temporary source-understanding HTML review page."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path


OUTLINE_LABELS = {
    "结论先行",
    "问题为什么重要",
    "已有做法与缺口",
    "关键机制",
    "实验信号与边界",
    "下一步验证",
}

BANNED_VISIBLE_TOKENS = [
    "Executive Abstract",
    "Problem Domain",
    "Current State",
    "References",
    "当前理解",
    "我现在的判断",
    "证据状态",
    "source understanding",
    "approval bundle",
    "QA passed",
    "needs_verification",
    "paper evidence",
    "source-original",
    "source-cropped",
    "agent-diagram",
    "agent-chart",
    "source-derived",
    "Claim / Evidence",
    "Source Locator",
]


class ReviewHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.hrefs: list[str] = []
        self.headings: list[tuple[str, str]] = []
        self.nav_texts: list[str] = []
        self.references_text = ""
        self.figcaptions: list[str] = []
        self.classes: list[str] = []
        self.images: list[tuple[str, str]] = []
        self._tag_stack: list[str] = []
        self._capture_heading: str | None = None
        self._heading_parts: list[str] = []
        self._in_nav = False
        self._nav_parts: list[str] = []
        self._in_refs = False
        self._refs_parts: list[str] = []
        self._in_figcaption = False
        self._figcaption_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {name: value or "" for name, value in attrs}
        self._tag_stack.append(tag)
        if attr.get("id"):
            self.ids.append(attr["id"])
            if attr["id"] in {"refs", "references"} or attr["id"].startswith("ref-"):
                self._in_refs = True
        if attr.get("href", "").startswith("#"):
            self.hrefs.append(attr["href"][1:])
        if attr.get("class"):
            self.classes.extend(part for part in attr["class"].split() if part)
        if tag == "img":
            self.images.append((attr.get("src", ""), attr.get("alt", "")))
        if tag in {"h1", "h2", "h3"}:
            self._capture_heading = tag
            self._heading_parts = []
        if tag == "nav" or "toc" in attr.get("class", "") or "review-toc" in attr.get("class", ""):
            self._in_nav = True
        if tag == "figcaption":
            self._in_figcaption = True
            self._figcaption_parts = []

    def handle_endtag(self, tag: str) -> None:
        if self._capture_heading == tag:
            text = normalize_text("".join(self._heading_parts))
            if text:
                self.headings.append((tag, text))
            self._capture_heading = None
            self._heading_parts = []
        if tag == "nav":
            if self._nav_parts:
                self.nav_texts.append(normalize_text("".join(self._nav_parts)))
            self._in_nav = False
            self._nav_parts = []
        if tag == "figcaption":
            text = normalize_text("".join(self._figcaption_parts))
            if text:
                self.figcaptions.append(text)
            self._in_figcaption = False
            self._figcaption_parts = []
        if self._in_refs and tag in {"section", "ol", "ul"}:
            self.references_text += " " + normalize_text("".join(self._refs_parts))
            self._in_refs = False
            self._refs_parts = []
        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._capture_heading:
            self._heading_parts.append(data)
        if self._in_nav:
            self._nav_parts.append(data)
        if self._in_refs:
            self._refs_parts.append(data)
        if self._in_figcaption:
            self._figcaption_parts.append(data)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def strip_tags(html: str) -> str:
    text = re.sub(r"<script\b.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return normalize_text(text)


def line_for(text: str, needle: str) -> int:
    index = text.find(needle)
    if index < 0:
        return 1
    return text.count("\n", 0, index) + 1


def _is_remote_url(value: str) -> bool:
    text = value.strip().lower()
    return text.startswith("http://") or text.startswith("https://")


def _is_data_url(value: str) -> bool:
    return value.strip().lower().startswith("data:")


def _load_report_asset_paths(base_dir: Path | None) -> set[str]:
    if base_dir is None:
        return set()
    data_path = base_dir / "report-data.json"
    if not data_path.exists():
        return set()
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    assets = data.get("assets") if isinstance(data, dict) else []
    if not isinstance(assets, list):
        return set()
    paths: set[str] = set()
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        path_value = str(asset.get("path") or asset.get("local_path") or "").strip()
        if not path_value:
            continue
        paths.add(path_value.replace("\\", "/"))
        asset_path = Path(path_value)
        resolved = asset_path if asset_path.is_absolute() else (base_dir / asset_path)
        paths.add(str(resolved.resolve()).replace("\\", "/"))
    return paths


def validate_html_review(html: str, base_dir: Path | None = None) -> list[str]:
    parser = ReviewHTMLParser()
    parser.feed(html)
    visible_text = strip_tags(html)
    errors: list[str] = []
    report_asset_paths = _load_report_asset_paths(base_dir)

    id_counts: dict[str, int] = {}
    for id_value in parser.ids:
        id_counts[id_value] = id_counts.get(id_value, 0) + 1
    duplicates = sorted(id_value for id_value, count in id_counts.items() if count > 1)
    if duplicates:
        errors.append(f"Duplicate HTML ids: {', '.join(duplicates[:8])}")

    id_set = set(parser.ids)
    missing = sorted(href for href in parser.hrefs if href and href not in id_set)
    if missing:
        errors.append(f"Broken anchor href targets: {', '.join(missing[:8])}")

    body_headings = [
        (tag, text)
        for tag, text in parser.headings
        if text not in {"阅读路径", "目录", "Contents"}
    ]
    bad_headings = [text for tag, text in body_headings if tag in {"h1", "h2"} and text in OUTLINE_LABELS]
    if bad_headings:
        errors.append(
            "Body headings use outline labels instead of claim-like conclusions: "
            + ", ".join(bad_headings)
            + ". Keep these labels in side navigation only."
        )

    for token in BANNED_VISIBLE_TOKENS:
        if token in visible_text:
            errors.append(f"Visible report contains banned internal/default token `{token}` near line {line_for(html, token)}")

    bracket_chain = re.search(r"(?:\[[SFTRE]\d+\]){3,}", visible_text)
    if bracket_chain:
        errors.append(f"Visible report contains dense bracket citation chain `{bracket_chain.group(0)}`")

    citation_ids = [id_value for id_value in parser.ids if id_value.startswith("cite-ref-")]
    reference_ids = [id_value for id_value in parser.ids if id_value.startswith("ref-")]
    if citation_ids and not reference_ids:
        errors.append("Citation markers exist but no reference entries with id `ref-*` were found")
    if reference_ids and not citation_ids:
        errors.append("Reference entries exist but no body citation markers with id `cite-ref-*` were found")
    for href in parser.hrefs:
        if href.startswith("ref-") and href not in id_set:
            errors.append(f"Citation link points to missing reference `{href}`")

    reference_backlinks = [href for href in parser.hrefs if href.startswith("cite-ref-")]
    if reference_ids and not reference_backlinks:
        errors.append("Reference section lacks backlinks to body citation markers")

    has_reconstructed = any(word in visible_text for word in ["重构图", "重绘", "reconstructed"])
    if has_reconstructed and not any(word in visible_text for word in ["原始证据", "原始表格", "原图", "source figure", "source table"]):
        errors.append("Reconstructed visual appears without nearby original evidence wording")

    for src, alt in parser.images:
        if not src.strip():
            errors.append("Image tag missing src")
            continue
        if _is_remote_url(src):
            errors.append(f"Image uses remote src instead of a local review asset: {src}")
            continue
        if _is_data_url(src):
            errors.append("Image uses data: URL; save browser-captured evidence images under review/assets/ and reference local files")
            continue
        if src.startswith("#"):
            continue
        if base_dir is not None:
            image_path = (base_dir / src).resolve() if not Path(src).is_absolute() else Path(src)
            if not image_path.exists():
                errors.append(f"Image local src does not exist: {src}")
            if report_asset_paths and src.replace("\\", "/") not in report_asset_paths and str(image_path).replace("\\", "/") not in report_asset_paths:
                errors.append(f"Image local src is not listed in report-data.json assets: {src}")

    return errors


def run_self_test() -> int:
    valid = """
<!doctype html><html lang="zh-CN"><body>
<div class="review-layout">
<nav class="review-toc"><a href="#conclusion">结论先行</a><a href="#problem">问题为什么重要</a></nav>
<main>
<h1>R-CLA 值得进入受控 serving 实验</h1>
<section id="conclusion"><h2>论文给出容量信号，但还不是上线结论</h2>
<p>8K 输入下 KV cache 从 1170 MB 降到 293 MB。<sup id="cite-ref-t4-1"><a href="#ref-t4">4</a></sup></p>
<div class="method-card"><h3>KV 量化是正交路线</h3><p>它压缩每个 KV 的 bit 数。</p></div>
<div class="evidence-pair"><figure><figcaption>读图结论：capacity 是核心收益。</figcaption></figure><aside>口径：单卡实验。</aside></div>
<div class="rebuild-block"><figure><svg></svg><figcaption>重构图：展示 KV cache 降幅。</figcaption></figure><figure><figcaption>原始表格：Table 4。</figcaption></figure></div>
</section>
<section id="problem"><h2>KV cache 已经成为长上下文容量约束</h2><p>这里解释问题域。</p></section>
<section id="refs"><h2>参考资料</h2><ol><li id="ref-t4">[T4] Table 4. <a href="#cite-ref-t4-1">↩</a></li></ol></section>
</main></div>
</body></html>
"""
    invalid = """
<!doctype html><html lang="zh-CN"><body>
<nav class="review-toc"><a href="#missing">结论先行</a></nav>
<main>
<h1>报告</h1>
<h2>结论先行</h2>
<p>当前理解：这里是 source understanding。[S1][T4][R2]</p>
<p>重构图显示提升。</p>
<img src="https://example.com/remote.png" alt="远程图">
</main>
</body></html>
"""
    valid_errors = validate_html_review(valid)
    invalid_errors = validate_html_review(invalid)
    if valid_errors:
        print("[ERROR] HTML Review self-test valid fixture failed:")
        for error in valid_errors:
            print(f"  - {error}")
        return 1
    expected_fragments = [
        "Body headings use outline labels",
        "Broken anchor href targets",
        "banned internal/default token",
        "dense bracket citation chain",
        "Reconstructed visual appears without nearby original evidence",
        "remote src",
    ]
    missing = [fragment for fragment in expected_fragments if not any(fragment in error for error in invalid_errors)]
    if missing:
        print("[ERROR] HTML Review self-test invalid fixture did not trigger expected failures:")
        for fragment in missing:
            print(f"  - {fragment}")
        print("Actual errors:")
        for error in invalid_errors:
            print(f"  - {error}")
        return 1
    print("[OK] HTML Review self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a source-understanding HTML review page.")
    parser.add_argument("html_file", type=Path, nargs="?")
    parser.add_argument("--self-test", action="store_true", help="Run built-in validator regression tests.")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if args.html_file is None:
        parser.error("html_file is required unless --self-test is used")

    html_path = args.html_file
    if not html_path.exists():
        print(f"[ERROR] HTML file not found: {html_path}")
        return 1
    html = html_path.read_text(encoding="utf-8", errors="replace")
    errors = validate_html_review(html, html_path.parent)
    if errors:
        print("[ERROR] HTML Review QA failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("[OK] HTML Review QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
