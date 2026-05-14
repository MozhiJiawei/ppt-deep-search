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
    "## Summary Page",
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
    "所属章节",
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
    field_pattern = r"^(页码|所属章节|页面标题|标题说明|分析总结|正文内容|参考图片|备注)[:：]\s*"
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


def toc_titles(text: str) -> list[str]:
    toc = extract_section(text, "## Table of Contents")
    return re.findall(r"^\d{2}\s+小标题[：:]\s*(\S.+?)\s*$", toc, flags=re.MULTILINE)


def extract_field(body: str, field: str) -> str:
    match = re.search(rf"^{re.escape(field)}[：:]\s*(.+?)\s*$", body, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def validate_summary_block(text: str, min_summary_content_chars: int, expected_summary_page: int | None) -> list[str]:
    errors: list[str] = []
    summary = extract_section(text, "## Summary Page")
    if not summary.strip():
        return ["Summary Page section is empty"]

    for field in ["页码", "页面标题", "标题说明", "分析总结", "正文内容", "参考图片"]:
        if field not in summary:
            errors.append(f"Summary Page missing field: {field}")

    page_match = re.search(r"^页码[：:]\s*(?:Page\s*)?(\d+)\s*$", summary, flags=re.MULTILINE)
    if not page_match:
        errors.append("Summary Page must include an actual page number in 页码")
    elif expected_summary_page is not None and int(page_match.group(1)) != expected_summary_page:
        errors.append(f"Summary Page 页码 must be Page {expected_summary_page}")

    summary_match = re.search(
        r"分析总结[：:]?\s*\n(?P<body>.*?)(?:\n(?:正文内容|参考图片|备注)[：:]|\Z)",
        summary,
        flags=re.S,
    )
    if not summary_match:
        errors.append("Summary Page missing analysis summary block")
    else:
        summary_items = re.findall(
            r"^\s*-\s*([^：:\n]{2,12})[：:]\s*\S+",
            summary_match.group("body"),
            flags=re.MULTILINE,
        )
        if not 1 <= len(summary_items) <= 3:
            errors.append("Summary Page analysis summary must contain 1-3 labeled bullets")

    density = content_char_count(summary)
    if density < min_summary_content_chars:
        errors.append(f"Summary Page content density too low: {density} < {min_summary_content_chars} counted characters")

    return errors


def validate(
    text: str,
    min_page_content_chars: int,
    min_summary_content_chars: int,
    expected_pages: int | None = None,
    allow_absolute_paths: bool = False,
) -> list[str]:
    text = text.lstrip("\ufeff")
    errors: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if not re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE):
            errors.append(f"Missing required heading: {heading}")

    has_toc = bool(re.search(r"^## Table of Contents\s*$", text, flags=re.MULTILINE))
    has_page_content = bool(re.search(r"^## Page Content\s*$", text, flags=re.MULTILINE))
    if expected_pages is not None and expected_pages < 1:
        errors.append("--expected-pages must be total PPT pages and must be >= 1")
    summary_only = expected_pages == 1
    contents_only = expected_pages == 3
    requires_chapter_pages = expected_pages is None or expected_pages >= 4
    expected_content_pages = expected_pages - 3 if expected_pages is not None and expected_pages >= 4 else None
    if requires_chapter_pages or contents_only:
        required_later_headings = ["## Table of Contents", "## Page Content"] if requires_chapter_pages else ["## Table of Contents"]
        for heading in required_later_headings:
            if not re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE):
                errors.append(f"Missing required heading for multi-page brief: {heading}")
    elif summary_only and (has_toc or has_page_content):
        errors.append("For expected-pages 1, omit Table of Contents and Page Content")
    if contents_only and has_page_content:
        errors.append("For expected-pages 3, omit Page Content because there are no chapter content pages")

    metadata = extract_section(text, "## Deck Metadata")
    for field in DECK_METADATA_FIELDS:
        if not re.search(rf"^{re.escape(field)}[：:]\s*\S+", metadata, flags=re.MULTILINE):
            errors.append(f"Deck Metadata field is missing or empty: {field}")

    if has_toc:
        toc = extract_section(text, "## Table of Contents")
        toc_items = re.findall(r"^\d{2}\s+小标题[：:]\s*\S+", toc, flags=re.MULTILINE)
        if not toc_items:
            errors.append("Table of Contents must contain items like: 01 小标题：...")
        if len(toc_items) > 3:
            errors.append(f"Table of Contents has too many chapter items: {len(toc_items)} > 3")
        if "说明" not in toc:
            errors.append("Table of Contents items must include concise 说明 lines")

    summary_index = text.find("## Summary Page")
    toc_index = text.find("## Table of Contents")
    page_index = text.find("## Page Content")
    if requires_chapter_pages and not (summary_index != -1 and toc_index != -1 and page_index != -1 and summary_index < toc_index < page_index):
        errors.append("PPT Content Brief must be ordered as Summary Page, Table of Contents, then Page Content")
    if not requires_chapter_pages and not (summary_index != -1 and (toc_index == -1 or summary_index < toc_index) and (page_index == -1 or summary_index < page_index)):
        errors.append("Summary-only PPT Content Brief must place Summary Page after Deck Metadata and omit later sections")

    expected_summary_page = 1 if summary_only else 2
    errors.extend(validate_summary_block(text, min_summary_content_chars=min_summary_content_chars, expected_summary_page=expected_summary_page))

    for banned in BANNED_INTERNAL_FIELDS + BANNED_RENDERING_FIELDS:
        if banned.lower() in text.lower():
            errors.append(f"Banned internal/layout token found in PPT Content Brief: {banned}")

    pages = extract_pages(text) if has_page_content else []
    if not pages and requires_chapter_pages:
        errors.append("No page content blocks found. Expected headings like: ### Page 1: 页面标题")
    elif expected_content_pages is not None and len(pages) != expected_content_pages:
        errors.append(
            f"Expected exactly {expected_content_pages} chapter Page Content block(s) for {expected_pages} total PPT pages, found {len(pages)}"
        )

    allowed_chapters = toc_titles(text) if has_toc else []

    for page in pages:
        for field in PAGE_FIELDS:
            if field not in page.body:
                errors.append(f"{page.title} (line {page.start_line}) missing field: {field}")

        chapter = extract_field(page.body, "所属章节")
        if chapter and allowed_chapters and chapter not in allowed_chapters:
            errors.append(
                f"{page.title} (line {page.start_line}) 所属章节 must match a Table of Contents 小标题: {chapter}"
            )

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

    absolute_paths = sorted(
        set(re.findall(r"[A-Za-z]:\\[^\r\n|,\)\]]+|(?:/mnt|/home|/Users)/[^\r\n|,\)\]]+", text))
    )
    if absolute_paths and not allow_absolute_paths:
        shown = ", ".join(absolute_paths[:3])
        if len(absolute_paths) > 3:
            shown += ", ..."
        errors.append(
            "Absolute local paths found in PPT Content Brief; put exact source paths in research_audit.md instead: "
            f"{shown}"
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

## Summary Page
页码：Page 2
页面标题：长程任务需要可治理的记忆层
标题说明：MIA 的价值在于把记忆从上下文堆叠升级为可检索、可更新、可评估的认知资产。
分析总结：
- 结构升级：长程任务需要把历史经验沉淀成可治理资产。
- 机制价值：记忆层让经验能够被检索、更新、淘汰和审计。
- 采用判断：跨多轮、多工具、多目标任务最值得优先评估记忆层。
正文内容：
- 这一页作为顶层总结页，应先回答技术负责人最关心的问题：为什么这不是又一种提示词技巧，而是长程任务基础设施的一部分。核心表达是，长程任务会不断产生跨轮经验，如果这些经验只存在于上下文窗口或临时摘要中，就会随任务轮次增加而变得难以管理。
- PPT 正文可以围绕三层逻辑展开：第一，上下文堆叠只能让模型看见更多历史，不能决定哪些历史值得保留；第二，结构化记忆把历史经验转化为可检索、可更新、可评估的对象；第三，团队只有能治理记忆对象，才可能在长程任务里持续复用成功路径并降低错误经验污染。
- 对读者来说，顶层判断不是“所有 Agent 都需要记忆层”，而是“当任务跨多轮、多工具、多目标，且历史经验会影响后续决策时，记忆层才从功能增强变成基础设施能力”。这个判断为后续章节留下清晰问题：为什么上下文不够、记忆机制怎么工作、落地时如何治理风险。
- 高密总结页还应该给 PPT Maker 足够的页面材料：可以把信息组织为“当前做法的问题、记忆层的机制、架构判断、采用边界”四块。当前做法的问题是长程任务中的经验会被上下文窗口、摘要策略和人工复制粘贴切碎；记忆层的机制是把经验变成有来源、有更新时间、有适用范围的对象；架构判断是记忆是否可治理决定它能否进入生产工作流；采用边界是短任务、一次性问答和低风险闲聊通常不需要完整记忆基础设施。
- 这一页的正文还要能支撑图文排版：左侧可以放任务循环或记忆生命周期图，右侧用三条高密标签句总结“为什么需要、怎么实现、何时采用”，底部用一行谨慎备注说明不外推到所有 Agent 场景。这样下游 PPT Agent 不需要读取内部审计文件，也能直接写出完整总结页。
- 总结页可以加入更具体的决策语言：如果团队的 Agent 任务需要跨会话延续、复用工具经验、保留用户长期偏好或沉淀失败教训，就应该评估记忆层；如果任务只是一次性问答，简单上下文摘要通常更轻。这个判断能帮助技术负责人把“记忆能力”从功能清单转成路线选择。
- 还可以给出一条可执行的采用路径：先在高价值长程任务中试点，定义记忆对象、更新时间、删除条件和访问权限，再观察任务完成率、错误记忆污染、人工修正成本和隐私合规压力。这样总结页不只是观点页，也能直接承接后续章节的机制、治理和落地讨论。
- 为避免页面空泛，正文应保留至少一个反向提醒：记忆层不是越多越好，错误记忆、过期偏好和权限不清的数据都会污染后续决策。真正值得投入的不是“让 Agent 记住更多”，而是让 Agent 知道哪些经验应该被保留、何时应该被调用、何时必须被删除。
- 这一页最终要让读者带走一个完整判断：记忆层的价值不在存储本身，而在把跨轮经验变成可管理、可复用、可纠错的工程资产。
- 因此总结页的信息密度应高于普通章节页，承担结论、结构、判断和行动入口四个任务。
参考图片：
- 可用任务循环图表达“任务执行 -> 经验沉淀 -> 记忆检索 -> 结果更新”的主线。
备注：
- 不把记忆层包装成所有 Agent 场景的默认答案，保持技术评审语气。

## Table of Contents
01 小标题：问题重构
说明：把读者从上下文长度问题带到经验资产治理问题。

## Page Content

### Page 4: 长程任务瓶颈来自经验不可管理
所属章节：问题重构
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


SELF_TEST_SUMMARY_ONLY_BRIEF = """# PPT Content Brief

## Deck Metadata
主题：Memory Intelligence Agent 的一页技术汇报
目标读者：技术负责人
页数口径：1 页总结页，不包含封面和目录页
核心结论：MIA 的价值在于把记忆从上下文堆叠升级为可治理的认知资产。
内容来源：论文正文、Figure 2、Table 1、用户补充判断
关联审计文件：research_audit.md

## Summary Page
页码：Page 1
页面标题：长程任务需要可治理的记忆层
标题说明：MIA 的价值在于把记忆从上下文堆叠升级为可检索、可更新、可评估的认知资产。
分析总结：
- 结构升级：长程任务需要把历史经验沉淀成可治理资产。
- 机制价值：记忆层让经验能够被检索、更新、淘汰和审计。
- 采用判断：跨多轮、多工具、多目标任务最值得优先评估记忆层。
正文内容：
- 这一页作为唯一交付页，需要同时承担结论、结构、判断和行动入口。它先回答技术负责人最关心的问题：为什么记忆层不是提示词技巧，而是长程任务基础设施的一部分。长程任务会持续产生跨轮经验，如果这些经验只存在于上下文窗口、摘要策略或人工复制粘贴里，就会随任务轮次增加而变得难以管理、难以复用，也难以纠错。
- 页面正文可以压成四块：当前做法的问题、记忆层的机制、架构判断、采用边界。当前做法的问题是历史经验会被上下文窗口切碎；记忆层的机制是把经验变成有来源、有更新时间、有适用范围的对象；架构判断是记忆是否可治理决定它能否进入生产工作流；采用边界是短任务、一次性问答和低风险闲聊通常不需要完整记忆基础设施。
- 这一页还应给出可执行的采用路径：先在高价值长程任务中试点，定义记忆对象、更新时间、删除条件和访问权限，再观察任务完成率、错误记忆污染、人工修正成本和隐私合规压力。真正值得投入的不是“让 Agent 记住更多”，而是让 Agent 知道哪些经验应该被保留、何时应该被调用、何时必须被删除。
- 如果做成高密排版，左侧可以放任务循环或记忆生命周期图，右侧用三条高密标签句总结“为什么需要、怎么实现、何时采用”，底部用一句谨慎备注说明不外推到所有 Agent 场景。
- 一页模式下不需要目录和后续内容页，因此总结页必须自己讲完整故事：先用标题和标题说明给出顶层结论，再用三条分析总结压缩问题、机制和判断，正文则补足原因、采用路径、风险边界和视觉组织建议。这样 PPT Maker 即使只消费这一页，也能生成一张信息密度足够高的高管判断页，而不是只有口号和几条空泛结论。
- 页面还可以加入一句反向判断：如果团队无法记录记忆来源、无法删除过期记忆、无法解释某次任务为何调用某段历史经验，那么记忆层会从资产变成污染源。这个反向判断能让总结页同时具备说服力和谨慎边界。
- 为了让一页内容真正可用，正文还应给出落地检查清单：记忆对象是否有清晰粒度，检索命中是否可评估，错误记忆是否能回滚，用户隐私和权限是否能隔离，记忆更新是否有人工审核或自动淘汰机制。这些检查项能直接变成 PPT 的下半部分内容，帮助读者判断是否进入试点。
- 如果需要更偏决策表达，可以把页面结论写成“先试点、再平台化”：先选一个跨多轮、多工具、失败代价较高的任务池验证记忆层收益，再决定是否沉淀为平台能力。这样总结页同时覆盖技术价值、试点路径和投资节奏。
- 这一页还应避免只讲收益：记忆层会引入存储成本、权限治理、错误传播和解释性压力。只有当这些治理成本小于长期任务中的重复探索、人工修正和上下文噪声成本时，记忆层才值得从功能增强升级为基础设施。
- 最终页面应该让读者能立即做判断：是否值得试点、试点看什么指标、什么情况下暂停推进，以及谁负责治理。
参考图片：
- 可用任务循环图表达“任务执行 -> 经验沉淀 -> 记忆检索 -> 结果更新”的主线。
备注：
- 不把记忆层包装成所有 Agent 场景的默认答案，保持技术评审语气。
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a PPT Deep Search PPT Content Brief.")
    parser.add_argument("brief", nargs="?", help="Path to PPT Content Brief Markdown.")
    parser.add_argument("--min-page-content-chars", type=int, default=900, help="Minimum counted content characters per page.")
    parser.add_argument("--min-summary-content-chars", type=int, default=1200, help="Minimum counted content characters for Summary Page.")
    parser.add_argument("--expected-pages", type=int, help="Require an exact total PPT page count. 1 means Summary Page only; 7 means cover + Summary Page + contents + 4 chapter pages.")
    parser.add_argument("--allow-absolute-paths", action="store_true", help="Allow local absolute paths in the PPT content brief.")
    parser.add_argument("--self-test", action="store_true", help="Run validator against an embedded valid brief.")
    args = parser.parse_args()

    if args.self_test:
        errors = validate(
            SELF_TEST_BRIEF,
            args.min_page_content_chars,
            args.min_summary_content_chars,
            expected_pages=4,
            allow_absolute_paths=args.allow_absolute_paths,
        )
        one_page_errors = validate(
            SELF_TEST_SUMMARY_ONLY_BRIEF,
            args.min_page_content_chars,
            args.min_summary_content_chars,
            expected_pages=1,
            allow_absolute_paths=args.allow_absolute_paths,
        )
        errors.extend([f"summary-only: {error}" for error in one_page_errors])
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
        args.min_summary_content_chars,
        expected_pages=args.expected_pages,
        allow_absolute_paths=args.allow_absolute_paths,
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
    print(f"[OK] Minimum summary content density: {args.min_summary_content_chars}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
