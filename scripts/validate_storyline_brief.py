#!/usr/bin/env python3
"""Validate a PPT Deep Search Storyline Brief Markdown file."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_HEADINGS = [
    "# Storyline Brief",
    "## Research Frame",
    "## Source Understanding",
    "## Executive Thesis",
    "## Reader Cognitive Path",
    "## Pyramid Outline",
    "## Chapter Logic",
    "## Page Briefs",
    "## Claim Evidence Implication Table",
    "## Evidence Map",
    "## Source Usage Policy",
    "## Visual Opportunities",
    "## Assumptions and Open Questions",
    "## Recommended Deck Storyline",
    "## Approval Log",
]

TOC_FIELDS = ["目录小标题", "目录说明", "章节论点"]

RESEARCH_FRAME_FIELDS = [
    "研究问题",
    "目标读者",
    "读者当前判断",
    "希望改变的判断",
    "核心结论",
    "材料范围",
    "证据边界",
]

SOURCE_UNDERSTANDING_FIELDS = [
    "它是什么",
    "它解决了什么问题",
    "跟同类技术比有什么亮点",
]

PAGE_FIELDS = [
    "页面角色",
    "支撑的章节论点",
    "页面标题",
    "标题说明",
    "分析总结",
    "Claim / Evidence / Implication",
    "参考图片",
    "支撑信息",
    "边界提醒",
]

BANNED_RENDERING_FIELDS = [
    "visual_anchor.kind",
    "visual_anchor_renderer",
    "contentLayout",
    "renderer",
    "expected_renderer",
    "visual_strategy",
    "template:",
    "字号",
    "字体",
    "配色",
    "几栏",
    "两栏",
    "三栏",
    "四栏",
]

EVIDENCE_MARKERS = [
    "source",
    "calculation",
    "inference",
    "user_judgment",
    "needs_verification",
    "Figure",
    "Table",
    "图",
    "表",
    "http://",
    "https://",
    ".pdf",
    ".md",
    ".xml",
    ".html",
    "用户判断",
    "原文",
    "推论",
    "待验证",
]

USAGE_POLICIES = ["original", "summarize", "background", "discard", "原样", "摘要", "背景", "舍弃"]


@dataclass
class PageSection:
    title: str
    body: str
    start_line: int


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def content_char_count(text: str) -> int:
    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        stripped = re.sub(r"^[\-\*\d\.\s]+", "", stripped)
        stripped = re.sub(r"^(页面角色|支撑的章节论点|页面标题|标题说明|分析总结|Claim|Evidence|Implication|参考图片|支撑信息|边界提醒|信息密度说明)[:：]\s*", "", stripped)
        cleaned_lines.append(stripped)
    cleaned = "\n".join(cleaned_lines)
    return len(re.findall(r"[\w\u4e00-\u9fff]", cleaned, flags=re.UNICODE))


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    next_heading = re.search(r"^##\s+", text[match.end() :], re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.end() : end]


def extract_pages(text: str) -> list[PageSection]:
    page_area = extract_section(text, "## Page Briefs")
    base_offset = text.find(page_area) if page_area else -1
    if not page_area:
        return []

    matches = list(re.finditer(r"^###\s+Page\s+\d+\s*:\s+.+$", page_area, re.MULTILINE))
    pages: list[PageSection] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(page_area)
        title = match.group(0).strip()
        body = page_area[match.end() : end]
        start_line = line_number_for_offset(text, base_offset + match.start())
        pages.append(PageSection(title=title, body=body, start_line=start_line))
    return pages


def count_chapter_logic_items(text: str) -> int:
    chapter_logic = extract_section(text, "## Chapter Logic")
    return len(re.findall(r"^\d+\.\s+", chapter_logic, flags=re.MULTILINE))


def extract_chapter_logic_items(text: str) -> list[str]:
    chapter_logic = extract_section(text, "## Chapter Logic")
    matches = list(re.finditer(r"^\d+\.\s+", chapter_logic, flags=re.MULTILINE))
    items = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(chapter_logic)
        items.append(chapter_logic[match.start() : end])
    return items


def validate(
    text: str,
    min_page_content_chars: int,
    expected_pages: int | None = None,
    forbid_absolute_paths: bool = False,
) -> list[str]:
    text = text.lstrip("\ufeff")
    errors: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if not re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE):
            errors.append(f"Missing required heading: {heading}")

    research_frame = extract_section(text, "## Research Frame")
    for field in RESEARCH_FRAME_FIELDS:
        if not re.search(rf"^{re.escape(field)}[：:]\s*\S+", research_frame, flags=re.MULTILINE):
            errors.append(f"Research Frame field is missing or empty: {field}")

    source_understanding = extract_section(text, "## Source Understanding")
    for field in SOURCE_UNDERSTANDING_FIELDS:
        if not re.search(rf"^{re.escape(field)}[：:]\s*\S+", source_understanding, flags=re.MULTILINE):
            errors.append(f"Source Understanding field is missing or empty: {field}")

    for banned in BANNED_RENDERING_FIELDS:
        if banned.lower() in text.lower():
            errors.append(f"Banned rendering/layout field found: {banned}")

    pages = extract_pages(text)
    if not pages:
        errors.append("No page briefs found. Expected headings like: ### Page 1: 页面标题")
    elif expected_pages is not None and len(pages) != expected_pages:
        errors.append(f"Expected exactly {expected_pages} page brief(s), found {len(pages)}")

    for page in pages:
        for field in PAGE_FIELDS:
            if field not in page.body:
                errors.append(f"{page.title} (line {page.start_line}) missing field: {field}")

        density = content_char_count(page.body)
        if density < min_page_content_chars:
            errors.append(
                f"{page.title} (line {page.start_line}) content density too low: "
                f"{density} < {min_page_content_chars} counted characters"
            )

        if not all(token in page.body for token in ["Claim", "Evidence", "Implication"]):
            errors.append(f"{page.title} (line {page.start_line}) lacks explicit Claim/Evidence/Implication entries")

        if not any(marker in page.body for marker in EVIDENCE_MARKERS):
            errors.append(f"{page.title} (line {page.start_line}) lacks evidence source/type markers")

        summary_match = re.search(r"分析总结[：:]?\s*\n(?P<body>.*?)(?:\n(?:Claim / Evidence / Implication|参考图片|支撑信息|边界提醒)[：:]|\Z)", page.body, flags=re.S)
        if not summary_match:
            errors.append(f"{page.title} (line {page.start_line}) missing analysis summary block")
        else:
            summary_items = re.findall(r"^\s*-\s*([^：:\n]{2,12})[：:]\s*\S+", summary_match.group("body"), flags=re.MULTILINE)
            if not 1 <= len(summary_items) <= 3:
                errors.append(f"{page.title} (line {page.start_line}) analysis summary must contain 1-3 labeled bullets")

        if "边界提醒" in page.body:
            boundary_block = re.search(r"边界提醒[：:]?\s*(.*?)(?:\n\S[^-\n].*?[：:]|\Z)", page.body, flags=re.S)
            if boundary_block and len(re.findall(r"[\w\u4e00-\u9fff]", boundary_block.group(1))) < 8:
                errors.append(f"{page.title} (line {page.start_line}) has an empty or too-thin boundary reminder")

    source_policy = extract_section(text, "## Source Usage Policy")
    if not any(policy in source_policy for policy in USAGE_POLICIES):
        errors.append("Source Usage Policy must include original/summarize/background/discard usage decisions")

    cei_table = extract_section(text, "## Claim Evidence Implication Table")
    for required in ["Claim", "Evidence", "Evidence Type", "Strength", "Implication", "Boundary"]:
        if required not in cei_table:
            errors.append(f"Claim Evidence Implication Table missing column or content: {required}")

    evidence_map = extract_section(text, "## Evidence Map")
    for required in ["Source Locator", "Supports Claim", "Usage Policy", "Misread Risk"]:
        if required not in evidence_map:
            errors.append(f"Evidence Map missing column or content: {required}")

    open_questions = extract_section(text, "## Assumptions and Open Questions")
    if not re.search(r"(Assumption|假设|Open question|未决|待验证)", open_questions, flags=re.I):
        errors.append("Assumptions and Open Questions must contain assumptions or open questions")

    approval_log = extract_section(text, "## Approval Log")
    for required in ["Audience", "Source understanding", "Page count", "counting convention", "Page titles", "Baseline File"]:
        if required not in approval_log:
            errors.append(f"Approval Log missing required approval evidence: {required}")

    pyramid_outline = extract_section(text, "## Pyramid Outline")
    if not re.search(r"(顶层总结页|Top-level summary page)", pyramid_outline, flags=re.I):
        errors.append("Pyramid Outline must include a standalone top-level summary page")

    chapter_count = count_chapter_logic_items(text)
    if chapter_count > 3:
        errors.append(f"Chapter Logic has too many chapter claims: {chapter_count} > 3")
    for index, item in enumerate(extract_chapter_logic_items(text), start=1):
        for field in TOC_FIELDS:
            if field not in item:
                errors.append(f"Chapter Logic item {index} missing table-of-contents field: {field}")

    numeric_claims = re.findall(r"(?<![A-Za-z0-9])\d+(?:\.\d+)?\s*(?:%|倍|x|X|年|月|日|ms|s|GB|MB|TOPS|tokens?)?", text)
    if numeric_claims and not any(marker in text for marker in ["Figure", "Table", "Source Locator", "原文", "用户判断", "needs_verification"]):
        errors.append("Numeric claims appear without visible source locators or verification markers")

    if forbid_absolute_paths:
        absolute_paths = sorted(set(re.findall(r"[A-Za-z]:\\[^\s|,\)\]]+", text)))
        if absolute_paths:
            shown = ", ".join(absolute_paths[:3])
            if len(absolute_paths) > 3:
                shown += ", ..."
            errors.append(
                "Absolute local paths found; use portable source locators or omit "
                f"--forbid-absolute-paths when local-only paths are acceptable: {shown}"
            )

    return errors


SELF_TEST_BRIEF = """# Storyline Brief

## Research Frame
研究问题：Memory Intelligence Agent 的汇报应如何说服技术负责人？
目标读者：技术负责人
读者当前判断：记忆机制可能只是工程增强。
希望改变的判断：记忆机制可以成为 Agent 长程任务能力的核心基础设施。
核心结论：MIA 的价值在于把记忆从上下文堆叠变成可管理的认知资产。
材料范围：论文正文、Figure 2、Table 1、用户判断。
证据边界：实验结论仅限论文给定 benchmark。

## Source Understanding
它是什么：MIA 是面向长程 Agent 任务的记忆管理方法，把历史经验组织成可检索、可更新的记忆资产。
它解决了什么问题：它缓解上下文堆叠在多轮任务中的成本、噪声和经验复用问题。
跟同类技术比有什么亮点：它强调记忆治理与评估，而不是只依赖更长上下文窗口或临时检索。

## Executive Thesis
MIA 的核心不是增加提示词长度，而是建立可检索、可更新、可评估的记忆层。

## Reader Cognitive Path
1. 先建立长程任务瓶颈。
2. 再解释记忆层机制。
3. 最后收束到落地边界。

## Pyramid Outline
0. 顶层总结页：记忆层是 Agent 长程任务能力的基础设施。
   页面标题：长程任务需要可治理的记忆层
   标题说明：把记忆从上下文堆叠升级为认知资产。
   分析总结：
   - 结构升级：长程任务需要可治理、可检索、可更新的记忆层。
1. 章节论点：长程任务需要结构化记忆。
   二级支撑：
   - 上下文窗口无法稳定承载跨任务经验。
   证据状态：
   - Figure 2 source strong。
   边界：
   - 不外推到所有 Agent 场景。

## Chapter Logic
1. 目录小标题：问题重构
   目录说明：把读者从上下文长度问题带到经验资产问题。
   章节论点：长程任务需要结构化记忆。
   章节角色：建立问题
   本章必须讲清：为什么上下文堆叠不是长期解法。
   关键证据：Figure 2。

## Page Briefs

### Page 1: 长程任务瓶颈来自经验不可管理
页面角色：frame
支撑的章节论点：顶层总结页
页面标题：长程任务瓶颈来自经验不可管理
标题说明：Agent 在多轮任务中真正缺失的是可沉淀、可检索、可更新的经验结构，而不只是更长上下文。
分析总结：
- 问题重构：长程任务的瓶颈不是上下文长度，而是经验无法沉淀为可治理资产。
- 证据锚定：Figure 2 展示记忆模块在论文 benchmark 中改善连续任务表现。
- 表达边界：该结论只能用于论文设置下的长程任务，不外推到全部 Agent 场景。
Claim / Evidence / Implication：
- Claim：长程任务需要结构化记忆层，而不是单纯扩展上下文窗口。
  Evidence：Figure 2 source strong，论文展示记忆模块在长程任务 benchmark 上改善连续任务表现；用户判断指出听众关心工程落地。
  Implication：PPT 应先把问题从“上下文长度”重构为“经验资产管理”，再介绍机制。
参考图片：
- Figure 2：original，必须保留 benchmark 名称、坐标轴和方法名，因为它直接支撑 C1；误读风险是外推为所有任务都提升。
支撑信息：
- 可解释上下文堆叠的三个限制：成本上升、检索噪声、经验无法复用。
- 可补充工程视角：记忆层把历史交互转化为可治理对象，便于审计、更新和迁移。
- 页面正文应围绕“经验资产管理”展开，而不是复述所有模型组件。
- 正文可以先解释为什么长上下文不是长期解法：随着任务轮次增加，历史信息会变成高噪声输入，模型需要反复在旧对话、工具结果和新目标之间做筛选，成本和误检风险都会上升。
- 然后补充 MIA 的具体内容价值：把历史经验拆成可检索、可更新、可评估的记忆对象，PPT Maker 可以据此写出“经验沉淀、按需调用、持续修正”三段正文。
- 最后给读者一个落地判断：如果团队只需要一次性问答，记忆层收益有限；如果任务跨多轮、多工具、多目标，结构化记忆才可能成为基础设施，而不是提示词技巧。
边界提醒：
- 不能说 MIA 已证明所有 Agent 场景有效，只能说在论文给定 benchmark 和设置下体现了长程任务收益。
信息密度说明：本页提供问题定义、证据依据、工程含义和边界，足以支持一页内容页。

## Claim Evidence Implication Table
| ID | Claim | Evidence | Evidence Type | Strength | Implication | Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 长程任务需要结构化记忆层 | Figure 2 | source | strong | 先重构问题 | 不外推全部任务 |

## Evidence Map
| Evidence ID | Source Locator | Supports Claim | Usage Policy | Must Preserve | Misread Risk |
| --- | --- | --- | --- | --- | --- |
| E1 | Figure 2 | C1 | original | benchmark、坐标轴、方法名 | 不代表所有任务 |

## Source Usage Policy
- Must use original: Figure 2。
- May summarize or rebuild: Table 1。
- Background only: 引言中的泛化表述。
- Discard: 与主线无关的实现细节。

## Visual Opportunities
- Figure 2 可作为证据图。

## Assumptions and Open Questions
- Assumption: 目标读者偏技术负责人。
- Open question: 是否需要补充竞品记忆机制对比？

## Recommended Deck Storyline
先问题重构，再机制解释，再证据证明，最后落地边界。

## Approval Log
| Stage | Approved Constraint | User Approval Summary | Baseline File |
| --- | --- | --- | --- |
| 1 | Audience and belief change | 用户确认目标读者为技术负责人，目标是把记忆层定位为基础设施。 | .tmp/ppt-deep-search/demo/baselines/01-audience.md |
| 1.5 | Source understanding: what it is, solved problem, distinctive亮点 | 用户确认 MIA 是长程任务记忆管理方法，重点解决经验不可管理问题，亮点是记忆治理与评估。 | .tmp/ppt-deep-search/demo/baselines/01-source-understanding.md |
| 1.6 | SCQA, big logic, top-level summary page | 用户确认顶层总结页标题、标题说明和分析总结。 | .tmp/ppt-deep-search/demo/baselines/01-audience-thesis.md |
| 2 | Page count and counting convention | 用户确认做 1 页内容页，不包含封面和目录页。 | .tmp/ppt-deep-search/demo/baselines/02-page-count.md |
| 2.5 | Table-of-contents small titles, descriptions, order, chapter claims | 用户确认 1 页输出不需要独立目录页，页内节奏为问题、机制、证据、边界。 | .tmp/ppt-deep-search/demo/baselines/02-table-of-contents.md |
| 3 | Page titles, title subtitles, analysis summaries, page roles, source usage, boundaries | 用户确认 Page 1 标题、标题说明、分析总结、Figure 2 原样使用和不可外推边界。 | .tmp/ppt-deep-search/demo/baselines/03-page-plan.md |
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a PPT Deep Search Storyline Brief.")
    parser.add_argument("brief", nargs="?", help="Path to Storyline Brief Markdown.")
    parser.add_argument("--min-page-content-chars", type=int, default=600, help="Minimum counted content characters per Page Brief.")
    parser.add_argument("--expected-pages", type=int, help="Require an exact number of Page Brief sections.")
    parser.add_argument("--forbid-absolute-paths", action="store_true", help="Fail when absolute local paths appear in source locators.")
    parser.add_argument("--self-test", action="store_true", help="Run validator against an embedded valid brief.")
    args = parser.parse_args()

    if args.self_test:
        errors = validate(
            SELF_TEST_BRIEF,
            args.min_page_content_chars,
            expected_pages=args.expected_pages,
            forbid_absolute_paths=args.forbid_absolute_paths,
        )
        if errors:
            print("[ERROR] Self-test failed:")
            for error in errors:
                print(f"  - {error}")
            return 1
        print("[OK] Self-test passed.")
        return 0

    if not args.brief:
        parser.error("brief is required unless --self-test is used")

    path = Path(args.brief)
    if not path.exists():
        print(f"[ERROR] Brief not found: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    errors = validate(
        text,
        args.min_page_content_chars,
        expected_pages=args.expected_pages,
        forbid_absolute_paths=args.forbid_absolute_paths,
    )
    if errors:
        print(f"[ERROR] Storyline Brief QA failed ({len(errors)} issue(s)):")
        for error in errors:
            print(f"  - {error}")
        return 1

    pages = extract_pages(text)
    print("[OK] Storyline Brief QA passed.")
    print(f"[OK] Page briefs checked: {len(pages)}")
    print(f"[OK] Minimum page content density: {args.min_page_content_chars}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
