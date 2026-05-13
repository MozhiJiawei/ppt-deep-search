#!/usr/bin/env python3
"""Validate a downstream-facing PPT Content Brief Markdown file."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REQUIRED_HEADINGS = [
    "# PPT Content Brief",
    "## Deck Metadata",
    "## Table of Contents",
    "## Page Content",
]

DECK_METADATA_FIELDS = [
    "主题",
    "目标读者",
    "页数口径",
    "核心结论",
    "内容来源",
    "关联审计文件",
]

PAGE_FIELDS = [
    "页面标题",
    "标题说明",
    "分析总结",
    "正文内容",
    "参考图片",
]

BANNED_INTERNAL_FIELDS = [
    "Claim",
    "Evidence",
    "Implication",
    "Evidence Map",
    "Source Locator",
    "Source Usage Policy",
    "Approval Log",
    "needs_verification",
    "user_judgment",
    "supplemental research",
    "primary source",
    "inference",
    "页面角色",
    "支撑的章节论点",
    "Claim / Evidence / Implication",
    "边界提醒",
    "证据边界",
    "证据状态",
    "误读风险",
    "信息密度说明",
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


@dataclass
class PageSection:
    title: str
    body: str
    start_line: int


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def content_char_count(text: str) -> int:
    cleaned_lines = []
    field_pattern = r"^(页面标题|标题说明|分析总结|正文内容|参考图片|备注)[:：]\s*"
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        stripped = re.sub(r"^[\-\*\d\.\s]+", "", stripped)
        stripped = re.sub(field_pattern, "", stripped)
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
    page_area = extract_section(text, "## Page Content")
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

    metadata = extract_section(text, "## Deck Metadata")
    for field in DECK_METADATA_FIELDS:
        if not re.search(rf"^{re.escape(field)}[：:]\s*\S+", metadata, flags=re.MULTILINE):
            errors.append(f"Deck Metadata field is missing or empty: {field}")

    toc = extract_section(text, "## Table of Contents")
    toc_items = re.findall(r"^\d{2}\s+小标题[：:]\s*\S+", toc, flags=re.MULTILINE)
    if not toc_items:
        errors.append("Table of Contents must contain items like: 01 小标题：...")
    if len(toc_items) > 3:
        errors.append(f"Table of Contents has too many chapter items: {len(toc_items)} > 3")
    if "说明" not in toc:
        errors.append("Table of Contents items must include concise 说明 lines")

    for banned in BANNED_INTERNAL_FIELDS + BANNED_RENDERING_FIELDS:
        if banned.lower() in text.lower():
            errors.append(f"Banned internal/layout token found in PPT Content Brief: {banned}")

    pages = extract_pages(text)
    if not pages:
        errors.append("No page content blocks found. Expected headings like: ### Page 1: 页面标题")
    elif expected_pages is not None and len(pages) != expected_pages:
        errors.append(f"Expected exactly {expected_pages} page content block(s), found {len(pages)}")

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

        summary_match = re.search(
            r"分析总结[：:]?\s*\n(?P<body>.*?)(?:\n(?:正文内容|参考图片|备注)[：:]|\Z)",
            page.body,
            flags=re.S,
        )
        if not summary_match:
            errors.append(f"{page.title} (line {page.start_line}) missing analysis summary block")
        else:
            summary_items = re.findall(
                r"^\s*-\s*([^：:\n]{2,12})[：:]\s*\S+",
                summary_match.group("body"),
                flags=re.MULTILINE,
            )
            if not 1 <= len(summary_items) <= 3:
                errors.append(f"{page.title} (line {page.start_line}) analysis summary must contain 1-3 labeled bullets")

        body_match = re.search(r"正文内容[：:]?\s*(.*?)(?:\n参考图片[：:]|\n备注[：:]|\Z)", page.body, flags=re.S)
        body_chars = content_char_count(body_match.group(1) if body_match else "")
        if body_chars < max(500, min_page_content_chars // 2):
            errors.append(f"{page.title} (line {page.start_line}) 正文内容 is too thin for PPT body material")

    if forbid_absolute_paths:
        absolute_paths = sorted(set(re.findall(r"[A-Za-z]:\\[^\s|,\)\]]+", text)))
        if absolute_paths:
            shown = ", ".join(absolute_paths[:3])
            if len(absolute_paths) > 3:
                shown += ", ..."
            errors.append(
                "Absolute local paths found; use portable locators or omit "
                f"--forbid-absolute-paths when local-only paths are acceptable: {shown}"
            )

    return errors


SELF_TEST_BRIEF = """# PPT Content Brief

## Deck Metadata
主题：Memory Intelligence Agent 的技术汇报
目标读者：技术负责人
页数口径：1 页内容页，不包含封面和目录页
核心结论：MIA 的价值在于把记忆从上下文堆叠升级为可治理的认知资产。
内容来源：论文正文、Figure 2、Table 1、用户补充判断
关联审计文件：research_audit.md

## Table of Contents
01 小标题：问题重构
说明：把读者从上下文长度问题带到经验资产治理问题。

## Page Content

### Page 1: 长程任务瓶颈来自经验不可管理
页面标题：长程任务瓶颈来自经验不可管理
标题说明：Agent 在多轮任务中真正缺失的是可沉淀、可检索、可更新的经验结构，而不只是更长上下文。
分析总结：
- 问题重构：长程任务的瓶颈不是上下文长度，而是经验无法沉淀为可治理资产。
- 机制升级：记忆层把历史交互转化为可检索、可更新、可评估的任务资产。
- 落地判断：只有跨多轮、多工具、多目标的任务，才真正需要把记忆当成基础设施。
正文内容：
- 长程任务会持续产生跨轮经验，包括用户偏好、工具调用结果、失败路径、已验证假设和中间产物。如果这些信息只留在上下文窗口里，模型每轮都要在旧对话、新目标和工具结果之间重新筛选，成本会随轮次上升，噪声也会持续积累。
- 单纯扩大上下文窗口只能缓解“放不下”的问题，不能解决“哪些经验值得保留、什么时候应该检索、错误经验如何淘汰”的治理问题。对技术负责人来说，真正的问题不是模型是否看过更多历史，而是团队能否管理历史经验的生命周期。
- MIA 这类记忆机制的表达重点应该放在经验资产化：任务执行过程中沉淀可复用经验，下一轮任务按需检索相关记忆，任务结束后再更新或淘汰旧记忆。这样才能把一次性对话中的信息转化为可持续复用的能力。
- 页面正文可以按“问题、机制、采用边界”三段展开。第一段解释上下文堆叠带来的成本和噪声；第二段解释记忆对象如何被组织、检索和更新；第三段说明并非所有场景都需要完整记忆层，短任务或一次性问答可能只需要摘要。
- 如果给技术负责人看，还应补充工程检查项：记忆对象如何切分，检索命中如何评估，错误记忆如何回滚，哪些数据需要权限控制，哪些记忆只适合 session 级保存。这些内容能把“记忆层是基础设施”支撑成可讨论的工程判断。
- 这一页的正文不应停留在“效果更好”的泛泛表述，而要讲清为什么记忆层比长上下文更可治理：它能记录来源、更新时间、适用范围和删除条件，也能让团队审计哪些历史经验影响了后续决策。
- 对 PPT 制作来说，可以把核心正文压成三组信息：上下文堆叠的问题，结构化记忆的能力，工程落地的判断标准。这样读者先理解痛点，再理解机制，最后知道什么时候值得采用。
- 采用建议可以写得更克制：先在高价值长程任务中试点记忆层，例如代码迁移、复杂数据分析、跨系统运维排障，再观察检索命中、错误记忆污染和人工修正成本。
参考图片：
- 使用论文中的记忆机制图或任务循环图，突出历史经验如何进入记忆、任务执行时如何检索、任务结束后如何更新。若没有合适原图，可重绘为“任务执行 -> 经验沉淀 -> 记忆检索 -> 结果更新”的简洁流程图。
备注：
- 不要把记忆层包装成所有 Agent 场景的默认答案；这页只强调长程、多轮、跨工具任务中的治理价值。
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a PPT Deep Search PPT Content Brief.")
    parser.add_argument("brief", nargs="?", help="Path to PPT Content Brief Markdown.")
    parser.add_argument("--min-page-content-chars", type=int, default=900, help="Minimum counted content characters per page.")
    parser.add_argument("--expected-pages", type=int, help="Require an exact number of Page Content sections.")
    parser.add_argument("--forbid-absolute-paths", action="store_true", help="Fail when absolute local paths appear.")
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
        print(f"[ERROR] PPT Content Brief QA failed ({len(errors)} issue(s)):")
        for error in errors:
            print(f"  - {error}")
        return 1

    pages = extract_pages(text)
    print("[OK] PPT Content Brief QA passed.")
    print(f"[OK] Page content blocks checked: {len(pages)}")
    print(f"[OK] Minimum page content density: {args.min_page_content_chars}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
