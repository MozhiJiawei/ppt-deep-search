---
name: ppt-deep-search
description: >-
  面向 PPT 生成前置阶段的人机协同深度研究与叙事规划。用于把论文、网页、Markdown、仓库分析、PDF、笔记或原始材料转成 PPT 可用的 Content Brief，供下游 PPT skill 制作幻灯片。
  适用于研究框定、读者认知路径设计、金字塔大纲、页面标题/标题说明/总结审批和源图使用策略。
  不用于演示文稿渲染、版式模板、字体/风格决策、导出或视觉 QA。
---

# PPT Deep Search

构建有来源支撑的 PPT 规划产物，不制作幻灯片。负责 research-to-brief 流程的编排、发现、路由和硬 gate。

最终交付文件：

- `ppt_content_brief.md`：面向下游 PPT 制作者的文案包。

## HITL 交互

- 默认用中文与用户交互。
- 向用户提问时，输出当前问题，并按gate中的回答模板整理备用答案，并等待用户回复确认。
- 必须遵循 HITL。

## 工作流程

### 1. 加载证据原则

同时加载 `references/evidence-principle.md` 和 `references/evidence-examples.md`，作为所有交付件表达的纲领和示例库。证据优先级、源图策略、补充证据时机、金字塔表达，以及所有 handoff artifact 的措辞都遵循这两个文件。

### 2. 确认受众

这是第一个 human-in-the-loop gate。确认目标读者、读者可能的当前判断、希望改变的判断、最终用途、来源集合和已知缺口。

请求受众审批时，只输出当前 gate 问题和 3 个编号受众/框架选项。使用这个精确模板：

```text
请先确认受众框架。请选择一个编号，或直接按模板改写。

1. 目标读者：<具体角色>
使用场景：<这份 brief/deck 会被拿去做什么>
当前判断：<读者现在可能怎么想>
希望改变：<看完后希望读者改成什么判断>

2. 目标读者：<具体角色>
使用场景：<这份 brief/deck 会被拿去做什么>
当前判断：<读者现在可能怎么想>
希望改变：<看完后希望读者改成什么判断>

3. 目标读者：<具体角色>
使用场景：<这份 brief/deck 会被拿去做什么>
当前判断：<读者现在可能怎么想>
希望改变：<看完后希望读者改成什么判断>
```

选项之后不要追加进度说明。

审批通过后保存：

```text
<workspace-root>/baselines/01-audience.md
```

### 3. 预留 Source Understanding 交付件

为未来 source-understanding 交付件预留。当前 runtime 不实现这一步。

### 4. 制作 PPT Content Brief

加载 `references/ppt-brief-hitl.md`，遵循其中的 human-in-the-loop 流程，产出 `ppt_content_brief.md`。

## 工作区

- 运行开始时确定一个 `workspace-root`。如果用户或父级 dispatch 提供输出目录，使用该目录；否则使用 `.tmp/ppt-deep-search/<task-name>/`。
- 将草稿笔记、source map、baselines、QA 文件和临时资产放在 `<workspace-root>/` 下。
- 最终文件必须位于 `<workspace-root>/ppt_content_brief.md`。
