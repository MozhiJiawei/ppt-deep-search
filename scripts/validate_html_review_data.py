#!/usr/bin/env python3
"""Lightweight guardrail for source-understanding report-data.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


OUTLINE_LABELS = {
    "结论先行",
    "问题为什么重要",
    "已有做法与缺口",
    "关键机制",
    "实验信号与边界",
    "下一步验证",
    "参考资料",
}


def _is_obj(value: Any) -> bool:
    return isinstance(value, dict)


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _is_http_url(value: Any) -> bool:
    text = str(value or "").strip().lower()
    return text.startswith("http://") or text.startswith("https://")


def _resolve_artifact_path(path_value: str, base_dir: Path | None) -> Path:
    path = Path(path_value)
    if path.is_absolute() or base_dir is None:
        return path
    if path.parts and path.parts[0] in {"sources", "review", "baselines", "QA"}:
        return base_dir.parent / path
    return base_dir / path


def _browser_evidence_for(value: Any) -> dict[str, Any]:
    if _is_obj(value):
        return value
    return {}


def _has_browser_capture(value: Any) -> bool:
    text = str(value or "").lower()
    good = ("codex browser", "in-app browser", "browser plugin", "browser-use")
    bad = (
        "raw capture",
        "raw html",
        "web search",
        "search-result",
        "browser unavailable",
        "browser-use tool unavailable",
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
    return any(fragment in text for fragment in good) and not any(fragment in text for fragment in bad)


def validate(data: Any, base_dir: Path | None = None) -> list[str]:
    errors: list[str] = []
    if not _is_obj(data):
        return ["Top-level JSON value must be an object"]

    meta = data.get("meta")
    if not _is_obj(meta):
        errors.append("Missing object: meta")
    else:
        for field in ("title", "question"):
            if not str(meta.get(field, "")).strip():
                errors.append(f"Missing meta.{field}")

    citations = _as_list(data.get("citations"))
    citation_ids: set[str] = set()
    web_citation_ids: set[str] = set()
    visual_citation_ids: set[str] = set()
    for idx, citation in enumerate(citations):
        if not _is_obj(citation):
            errors.append(f"citations[{idx}] must be an object")
            continue
        cid = str(citation.get("id", "")).strip()
        if not cid:
            errors.append(f"citations[{idx}] missing id")
        elif cid in citation_ids:
            errors.append(f"Duplicate citation id: {cid}")
        else:
            citation_ids.add(cid)
        if not str(citation.get("title", "")).strip():
            errors.append(f"citation {cid or idx} missing title")
        if not str(citation.get("locator", "")).strip():
            errors.append(f"citation {cid or idx} missing locator")
        if _is_http_url(citation.get("url")):
            if cid:
                web_citation_ids.add(cid)
            evidence = _browser_evidence_for(citation.get("browser_evidence"))
            local_path = str(evidence.get("local_path") or evidence.get("path") or "").strip()
            if not local_path:
                errors.append(f"web citation {cid or idx} missing browser_evidence.local_path")
            elif not _resolve_artifact_path(local_path, base_dir).exists():
                errors.append(f"web citation {cid or idx} browser_evidence.local_path does not exist: {local_path}")
            if not _has_browser_capture(evidence.get("capture_method")):
                errors.append(f"web citation {cid or idx} browser_evidence.capture_method must identify Codex/browser-use capture")
        kind = str(citation.get("kind", "")).strip().lower()
        marker = str(citation.get("marker", "")).strip().upper()
        if kind in {"figure", "image", "screenshot", "table"} or marker.startswith(("F", "T")):
            if cid:
                visual_citation_ids.add(cid)

    assets = _as_list(data.get("assets"))
    asset_citation_ids: set[str] = set()
    for idx, asset in enumerate(assets):
        if not _is_obj(asset):
            errors.append(f"assets[{idx}] must be an object")
            continue
        label = str(asset.get("id") or idx)
        asset_path = str(asset.get("path") or asset.get("local_path") or "").strip()
        if not asset_path:
            errors.append(f"asset {label} missing path")
        elif not _resolve_artifact_path(asset_path, base_dir).exists():
            errors.append(f"asset {label} path does not exist: {asset_path}")
        source_citation = str(asset.get("source_citation", "")).strip()
        if source_citation:
            asset_citation_ids.add(source_citation)
            if citation_ids and source_citation not in citation_ids:
                errors.append(f"asset {label} cites unknown citation id: {source_citation}")
        elif _is_http_url(asset.get("source_url")) or _is_http_url(asset.get("page_url")):
            errors.append(f"web asset {label} missing source_citation")
        if _is_http_url(asset.get("source_url")) or _is_http_url(asset.get("page_url")):
            if not _is_http_url(asset.get("page_url")):
                errors.append(f"web asset {label} missing page_url")
            if not _is_http_url(asset.get("source_url")):
                errors.append(f"web asset {label} missing source_url")
            if not _has_browser_capture(asset.get("capture_method")):
                errors.append(f"web asset {label} capture_method must identify Codex/browser-use capture")

    for cid in sorted(visual_citation_ids & web_citation_ids):
        if cid not in asset_citation_ids:
            errors.append(f"web visual citation {cid} has no matching asset.source_citation")

    sections = _as_list(data.get("sections"))
    for idx, section in enumerate(sections):
        if not _is_obj(section):
            errors.append(f"sections[{idx}] must be an object")
            continue
        heading = str(section.get("heading_claim", "")).strip()
        if not heading:
            errors.append(f"sections[{idx}] missing heading_claim")
        elif heading in OUTLINE_LABELS:
            errors.append(f"sections[{idx}].heading_claim is an outline label, not a claim: {heading}")
        blocks = _as_list(section.get("blocks"))
        for bidx, block in enumerate(blocks):
            if not _is_obj(block):
                errors.append(f"sections[{idx}].blocks[{bidx}] must be an object")
                continue
            if not str(block.get("type", "")).strip():
                errors.append(f"sections[{idx}].blocks[{bidx}] missing type")

    for idx, chart in enumerate(_as_list(data.get("charts"))):
        if not _is_obj(chart):
            errors.append(f"charts[{idx}] must be an object")
            continue
        label = chart.get("id", idx)
        for field in ("id", "question", "chart_type", "caption_takeaway"):
            if not str(chart.get(field, "")).strip():
                errors.append(f"chart {label} missing {field}")
        if not _as_list(chart.get("source_citations")):
            errors.append(f"chart {label} missing source_citations")
        if not _as_list(chart.get("units")):
            errors.append(f"chart {label} missing units")
        if not _as_list(chart.get("data")):
            errors.append(f"chart {label} missing data rows")
        for cid in _as_list(chart.get("source_citations")):
            if citation_ids and str(cid) not in citation_ids:
                errors.append(f"chart {label} cites unknown citation id: {cid}")

    for idx, method in enumerate(_as_list(data.get("comparison_methods"))):
        if not _is_obj(method):
            errors.append(f"comparison_methods[{idx}] must be an object")
            continue
        label = method.get("id", idx)
        for field in ("name", "positioning", "mechanism", "representative_evidence", "boundary", "relationship"):
            if not str(method.get(field, "")).strip():
                errors.append(f"comparison method {label} missing {field}")

    return errors


def self_test() -> int:
    good = {
        "meta": {"title": "标题", "question": "是否值得复测？"},
        "citations": [{"id": "t4", "title": "Table 4", "locator": "paper Table 4"}],
        "sections": [{"heading_claim": "8K 容量信号支持复测", "blocks": [{"type": "chart_with_aside"}]}],
        "charts": [{
            "id": "kv", "question": "省多少？", "chart_type": "bar", "caption_takeaway": "约 4x",
            "source_citations": ["t4"], "units": ["MB"], "data": [{"x": 1}]
        }],
        "comparison_methods": [{
            "id": "h2o", "name": "H2O", "positioning": "token axis", "mechanism": "evict tokens",
            "representative_evidence": "primary source result", "boundary": "not layer axis", "relationship": "orthogonal"
        }],
    }
    bad = {
        "meta": {"title": ""},
        "citations": [{
            "id": "f1",
            "kind": "figure",
            "title": "Web figure",
            "locator": "web page hero",
            "url": "https://example.com/article",
            "browser_evidence": {"capture_method": "curl", "local_path": "missing.md"},
        }],
        "sections": [{"heading_claim": "结论先行", "blocks": [{}]}],
        "charts": [{}],
    }
    good_errors = validate(good)
    bad_errors = validate(bad)
    if good_errors:
        print("[ERROR] valid fixture failed:")
        print("\n".join(good_errors))
        return 1
    required = [
        "Missing meta.title",
        "outline label",
        "missing source_citations",
        "browser_evidence.capture_method",
        "web visual citation f1 has no matching asset.source_citation",
    ]
    if not all(any(fragment in err for err in bad_errors) for fragment in required):
        print("[ERROR] invalid fixture did not produce expected errors:")
        print("\n".join(bad_errors))
        return 1
    print("[OK] HTML review data self-test passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate source-understanding report-data.json.")
    parser.add_argument("json_file", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
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

    errors = validate(data, args.json_file.parent)
    if errors:
        print("[ERROR] HTML review data QA failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("[OK] HTML review data QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
