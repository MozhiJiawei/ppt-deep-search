#!/usr/bin/env python3
"""Build a PPT Content Brief skeleton from approved HITL JSON."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def require_mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def require_list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")
    return value


def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def non_empty(value: Any, name: str) -> str:
    result = text(value)
    if not result:
        raise ValueError(f"{name} is required")
    return result


def bullet_lines(items: list[Any]) -> list[str]:
    return [f"- {text(item)}" for item in items if text(item)] or ["- 待补充"]


def analysis_support_todos(items: list[Any]) -> list[str]:
    lines = []
    for item in items:
        value = text(item)
        if not value:
            continue
        label = value.split("：", 1)[0].split(":", 1)[0].strip()
        if label:
            lines.append(f"- {label}：TODO：扩写支撑该分析总结的机制、事实、比较、影响或边界。")
    return lines or ["- TODO：扩写正文内容。"]


def validate(data: dict[str, Any]) -> None:
    scqa = require_mapping(data.get("scqa"), "scqa")
    page_count = require_mapping(data.get("page_count"), "page_count")
    summary = require_mapping(data.get("summary_page"), "summary_page")
    toc = require_list(data.get("table_of_contents"), "table_of_contents")
    pages = require_list(data.get("content_pages"), "content_pages")

    for field in ("situation", "complication", "question", "answer"):
        non_empty(scqa.get(field), f"scqa.{field}")
    non_empty(page_count.get("counting_rule"), "page_count.counting_rule")
    if not isinstance(page_count.get("total_pages"), int):
        raise ValueError("page_count.total_pages must be an integer")
    require_list(page_count.get("page_structure"), "page_count.page_structure")
    for field in ("page_number", "title", "subtitle"):
        non_empty(summary.get(field), f"summary_page.{field}")
    require_list(summary.get("analysis"), "summary_page.analysis")
    if not toc:
        raise ValueError("table_of_contents must not be empty")
    if len(toc) > 3:
        raise ValueError("table_of_contents must have at most 3 chapter items")
    toc_titles: set[str] = set()
    for index, item in enumerate(toc, 1):
        item = require_mapping(item, f"table_of_contents[{index}]")
        non_empty(item.get("index"), f"table_of_contents[{index}].index")
        toc_titles.add(non_empty(item.get("title"), f"table_of_contents[{index}].title"))
        non_empty(item.get("description"), f"table_of_contents[{index}].description")
    total_pages = page_count.get("total_pages")
    expected_content_pages = total_pages - 3 if isinstance(total_pages, int) and total_pages >= 4 else 0
    if len(pages) != expected_content_pages:
        raise ValueError(f"content_pages must contain exactly {expected_content_pages} item(s) for {total_pages} total pages")
    for index, page in enumerate(pages, 1):
        page = require_mapping(page, f"content_pages[{index}]")
        for field in ("page_number", "section", "title", "subtitle"):
            non_empty(page.get(field), f"content_pages[{index}].{field}")
        section = non_empty(page.get("section"), f"content_pages[{index}].section")
        if section not in toc_titles:
            raise ValueError(f"content_pages[{index}].section must match a table_of_contents title: {section}")
        require_list(page.get("analysis"), f"content_pages[{index}].analysis")


def run_visible_copy_check(title: str, subtitle: str, analysis: list[Any], *, summary_page: bool) -> None:
    validator = Path(__file__).with_name("validate_ppt_content_brief.py")
    command = [
        sys.executable,
        str(validator),
        "--visible-copy-check",
        "--title",
        title,
        "--subtitle",
        subtitle,
    ]
    if summary_page:
        command.append("--summary-page")
    for item in analysis:
        value = text(item)
        if value:
            command.extend(["--analysis-bullet", value])
    result = subprocess.run(command, text=True, encoding="utf-8", errors="replace", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise ValueError((result.stdout + result.stderr).strip())


def validate_visible_copy_from_json(data: dict[str, Any]) -> None:
    summary = require_mapping(data["summary_page"], "summary_page")
    run_visible_copy_check(
        non_empty(summary.get("title"), "summary_page.title"),
        non_empty(summary.get("subtitle"), "summary_page.subtitle"),
        require_list(summary.get("analysis"), "summary_page.analysis"),
        summary_page=True,
    )
    for index, page in enumerate(require_list(data["content_pages"], "content_pages"), 1):
        page = require_mapping(page, f"content_pages[{index}]")
        run_visible_copy_check(
            non_empty(page.get("title"), f"content_pages[{index}].title"),
            non_empty(page.get("subtitle"), f"content_pages[{index}].subtitle"),
            require_list(page.get("analysis"), f"content_pages[{index}].analysis"),
            summary_page=False,
        )


def audience_from_baseline(path: Path | None) -> str:
    if not path:
        return "待补充"
    if not path.exists():
        raise ValueError(f"audience baseline not found: {path}")
    content = path.read_text(encoding="utf-8")
    for line in content.splitlines():
        stripped = line.strip()
        for label in ("目标读者：", "目标读者:", "target_reader:", "target_reader："):
            if stripped.startswith(label):
                return stripped[len(label) :].strip() or "待补充"
    for line in content.splitlines():
        if line.strip():
            return line.strip()
    return "待补充"


def build_markdown(data: dict[str, Any], audience_text: str = "待补充") -> str:
    scqa = require_mapping(data["scqa"], "scqa")
    page_count = require_mapping(data["page_count"], "page_count")
    summary = require_mapping(data["summary_page"], "summary_page")
    toc = require_list(data["table_of_contents"], "table_of_contents")
    pages = require_list(data["content_pages"], "content_pages")

    topic = text(data.get("topic")) or text(scqa.get("answer")) or "待定主题"
    source_set = require_list(data.get("source_set", []), "source_set")
    source_text = "；".join(text(item) for item in source_set if text(item)) or "待补充"

    lines: list[str] = [
        "# PPT Content Brief",
        "",
        "## Deck Metadata",
        f"主题：{topic}",
        f"目标读者：{audience_text or '待补充'}",
        f"页数口径：{page_count['total_pages']} 页；{non_empty(page_count.get('counting_rule'), 'page_count.counting_rule')}",
        f"核心结论：{non_empty(scqa.get('answer'), 'scqa.answer')}",
        f"内容来源：{source_text}",
        "",
        "## Summary Page",
        f"页码：{non_empty(summary.get('page_number'), 'summary_page.page_number')}",
        f"页面标题：{non_empty(summary.get('title'), 'summary_page.title')}",
        f"标题说明：{non_empty(summary.get('subtitle'), 'summary_page.subtitle')}",
        "分析总结：",
        *bullet_lines(require_list(summary.get("analysis"), "summary_page.analysis")),
        "正文内容：",
        *analysis_support_todos(require_list(summary.get("analysis"), "summary_page.analysis")),
        f"- 情境：{non_empty(scqa.get('situation'), 'scqa.situation')}",
        f"- 冲突：{non_empty(scqa.get('complication'), 'scqa.complication')}",
        f"- 问题：{non_empty(scqa.get('question'), 'scqa.question')}",
        f"- 答案：{non_empty(scqa.get('answer'), 'scqa.answer')}",
        "参考图片：",
        "- 待补充",
        "备注：",
        f"- {text(summary.get('notes')) or '待补充'}",
    ]

    if toc:
        lines.extend(["", "## Table of Contents"])
        for item in toc:
            item = require_mapping(item, "table_of_contents item")
            lines.append(f"{non_empty(item.get('index'), 'toc.index')} 小标题：{non_empty(item.get('title'), 'toc.title')}")
            lines.append(f"说明：{non_empty(item.get('description'), 'toc.description')}")
            lines.append("")
        if lines[-1] == "":
            lines.pop()

    if pages:
        lines.extend(["", "## Page Content"])
        for page in pages:
            page = require_mapping(page, "content_pages item")
            page_number = non_empty(page.get("page_number"), "page.page_number")
            title = non_empty(page.get("title"), "page.title")
            lines.extend(
                [
                    "",
                    f"### {page_number}: {title}",
                    f"所属章节：{non_empty(page.get('section'), 'page.section')}",
                    f"页面标题：{title}",
                    f"标题说明：{non_empty(page.get('subtitle'), 'page.subtitle')}",
                    "分析总结：",
                    *bullet_lines(require_list(page.get("analysis"), "page.analysis")),
                    "正文内容：",
                    *analysis_support_todos(require_list(page.get("analysis"), "page.analysis")),
                    *bullet_lines(require_list(page.get("claims_to_support", []), "page.claims_to_support")),
                    *[f"- 边界：{text(item)}" for item in require_list(page.get("boundaries", []), "page.boundaries") if text(item)],
                    "参考图片：",
                    "- 待补充",
                    "备注：",
                    f"- {text(page.get('notes')) or '待补充'}",
                ]
            )

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build ppt_content_brief.md skeleton from approved HITL JSON.")
    parser.add_argument("input_json", nargs="?", type=Path)
    parser.add_argument("output_md", nargs="?", type=Path)
    parser.add_argument("--audience-baseline", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        sample = {
            "topic": "示例主题",
            "source_set": ["paper.xml"],
            "scqa": {
                "situation": "已有方案成本上升",
                "complication": "现有证据仍有边界",
                "question": "是否值得复测",
                "answer": "可复测，不可直上",
            },
            "page_count": {
                "total_pages": 4,
                "counting_rule": "包含 cover、summary、contents",
                "page_structure": ["Page 1 cover", "Page 2 summary", "Page 3 contents", "Page 4 content"],
            },
            "summary_page": {
                "page_number": "Page 2",
                "title": "可复测，不可直上",
                "subtitle": "证据支持进入受控验证，但不能外推上线收益。",
                "analysis": ["立项判断：先做小规模复测"],
                "notes": "保持审慎语气",
            },
            "table_of_contents": [{"index": "01", "title": "复测理由", "description": "说明为什么值得验证"}],
            "content_pages": [
                {
                    "page_number": "Page 4",
                    "section": "复测理由",
                    "title": "收益先看端到端",
                    "subtitle": "原型必须同时验证质量、延迟、吞吐、显存和边界，不能只看单项指标。",
                    "analysis": ["验证口径：同测质量、延迟和成本"],
                    "claims_to_support": ["端到端指标优先"],
                    "boundaries": ["不外推线上收益"],
                    "notes": "",
                }
            ],
        }
        validate(sample)
        validate_visible_copy_from_json(sample)
        output = build_markdown(sample, "技术负责人")
        if "# PPT Content Brief" not in output or "## Page Content" not in output:
            print("[ERROR] Self-test output missing required headings")
            return 1
        print("[OK] HITL JSON to brief skeleton self-test passed.")
        return 0

    if not args.input_json or not args.output_md:
        parser.error("input_json and output_md are required unless --self-test is used")

    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    data = require_mapping(data, "root")
    validate(data)
    validate_visible_copy_from_json(data)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(data, audience_from_baseline(args.audience_baseline)), encoding="utf-8", newline="\n")
    print(f"[OK] Wrote skeleton: {args.output_md}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        raise SystemExit(1)
