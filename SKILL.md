---
name: ppt-deep-search
description: >-
  面向 PPT 生成前置阶段的人机协同深度研究与叙事规划。用于把论文、网页、Markdown、仓库分析、PDF、笔记或原始材料转成 PPT 可用的 Content Brief，供下游 PPT skill 制作幻灯片。
  适用于研究框定、读者认知路径设计、金字塔大纲、页面标题/标题说明/总结审批和源图使用策略。
  不用于演示文稿终稿渲染。
---

# PPT Deep Search

构建有来源支撑的 PPT 规划产物，不制作幻灯片。负责 research-to-brief 流程的编排、发现、路由和硬 gate。

最终交付文件：

- `ppt_content_brief.md`：面向下游 PPT 制作者的文案包。
- `source_understanding_review.html`：对“不了解该技术的技术小白”解释技术原理。

## HITL 交互

- 默认用中文与用户交互。
- 向用户提问时，输出当前问题，并按gate中的回答模板整理备用答案，并等待用户回复确认。
- 必须遵循 HITL。

## Workspace Skill 索引

- 这些SKILL都是配套委派子agent使用的，主agent禁止加载查阅细节
- 网页来源抓取使用 workspace skill：`web-article-capture`。
- Source Understanding HTML deck 生成使用 workspace skill：`hw-ppt-gen-html`。
- 论文解析使用 workspace skill：`grobid-docling-pdf`（仓库路径：`skills/grobid_pdf_skill/SKILL.md`）。
- 优先使用工作区中的现有文件，无法在工作区中找到些SKILL时，通过git将子skill clone到 .tmp目录下来使用
  - https://github.com/MozhiJiawei/web-article-capture
  - https://github.com/MozhiJiawei/hw-ppt-gen-html
  - https://github.com/MozhiJiawei/grobid_pdf_skill

## 工作流程

### 1. 加载证据原则

同时加载 `references/evidence-principle.md` 和 `references/evidence-examples.md`，作为所有交付件表达的纲领和示例库。证据优先级、源图策略、补充证据时机、金字塔表达，以及所有 handoff artifact 的措辞都遵循这两个文件。

### 2. 制作 Source Understanding 审阅 deck

加载 `references/source-understanding-html-ppt.md`，委派子agent做内容解析，委派子agnet制作 `source_understanding_review.html`
未经用户批准，不得进入 `ppt-brief-hitl.md`。

### 3. 制作 PPT Content Brief

加载 `references/ppt-brief-hitl.md`，遵循其中的 human-in-the-loop 流程，产出 `ppt_content_brief.md`。

## 工作区

- 运行开始时确定一个 `workspace-root`。如果用户或父级 dispatch 提供输出目录，使用该目录；否则使用 `.tmp/ppt-deep-search/<task-name>/`。
- 将草稿笔记、source map、baselines、QA 文件和临时资产放在 `<workspace-root>/` 下。
- 最终文件必须位于 `<workspace-root>/ppt_content_brief.md`。
