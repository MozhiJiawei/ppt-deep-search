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


def validate(data: Any) -> list[str]:
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
    bad = {"meta": {"title": ""}, "sections": [{"heading_claim": "结论先行", "blocks": [{}]}], "charts": [{}]}
    good_errors = validate(good)
    bad_errors = validate(bad)
    if good_errors:
        print("[ERROR] valid fixture failed:")
        print("\n".join(good_errors))
        return 1
    required = ["Missing meta.title", "outline label", "missing source_citations"]
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

    errors = validate(data)
    if errors:
        print("[ERROR] HTML review data QA failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("[OK] HTML review data QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
