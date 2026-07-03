# Source Understanding HTML PPT

本文件规定如何编排multi-agent，完成内容解析与source Understanding制作
multi-agent原则：必须按照prompt模板，启动子agent，你需要将prompt里的占位符具象化，但不允许添加任何额外说明

## 来源准备 HITL（主Agent完成）

先根据用户输入的信源、主题和已知缺口判断输入类型。所有场景都写入 `<workspace-root>/sources/source-selection.md`。
  - 输入类型：`web` 或 `paper`。
  - 原始来源清单。
  - 对照研究/同类方案清单。

```text
请先确认 Source Understanding 的信息来源。。

原始页面（最多 3 个）：
1. <标题> — <URL>
   选择理由：<为什么它是原始/高相关来源>
2. <标题> — <URL>
   选择理由：<为什么它是原始/高相关来源>
3. <标题> — <URL>
   选择理由：<为什么它是原始/高相关来源>

同类方案（2 个）：
1. <方案/研究名> — <URL 或路径>
   对照角色：<它和主题相比用于说明什么>
2. <方案/研究名> — <URL 或路径>
   对照角色：<它和主题相比用于说明什么>

1. 批准
```

## 信息爬取（委派子Agent完成）

### 网页

来源按页面分别委派给子 agent 使用 workspace skill `web-article-capture` 抓取。每个子 agent 只处理一个网页，产出独立 source package，并运行页面 validator。

给子agnet的Prompt：
```text
请加载并使用 `web-article-capture` 抓取单个网页来源。

网页：
- 标题：<title>
- URL：<url>
- Source slug：<source-slug>

输出目录：
<workspace-root>/sources/web/<source-slug>/
```

### 论文

来源按论文分别委派给子 agent 使用 workspace skill `grobid-docling-pdf` 抓取。每个子 agent 只处理一篇论文

给子agnet的Prompt：
```text
请加载并使用 `grobid-docling-pdf` 将论文下载下来，并完成解析。若运行环境无法按 skill 名触发，则读取 `skills/grobid_pdf_skill/SKILL.md`。

论文：
- 标题：<title>
- URL：<url>
- Source slug：<source-slug>

输出目录：
<workspace-root>/sources/papers/<source-slug>/
```

## 制作 HTML PPT（委派子Agent完成）

委派子agnet根据 workspace skill `hw-ppt-gen-html` 制作 Source Understanding HTML deck。

要根据同类研究的数量启动多个子agnet并行制作

最终交付：主报告 + 最多两份同类报告

给子agnet的Prompt：
```text
请根据信息源和要求，加载并使用 `hw-ppt-gen-html` 制作 Source Understanding HTML deck。 允许使用子agent

信息源： <path1>, <path2>, <path3>, ...

听众：“不了解该技术的技术小白”
目标：让听众快速建立技术心智模型。内容应结论先行，并解释问题背景、关键机制、效果；重要判断必须有脚注或引用可追溯。

请根据内容选择合适的主题、模板、布局和页数。视觉偏好是白底、冷静、工程化、高信息密度，可优先考虑 swiss-grid / engineering-whiteprint / academic-paper 等风格。

高信息密度指：用机制图、对比矩阵、指标表、证据截图标注、引用链呈现可验证关系；不要用营销式大标题或低信息密度留白。证据图表必须可读，必要时拆页、局部放大、重绘或做表格化摘要。

主视觉材料必须优先服务“读懂”，而不是堆材料。图、表、截图、机制图、架构图或代码片段只要承载页面判断，就必须配套解释，让读者不用猜画面元素和判断之间的关系。若一个视觉材料承载独立判断，默认一页只放一个主视觉材料；不要把多个高信息密度材料压在同一页里让读者自行拼接。每个主视觉材料必须解释：

- 图中关键字：例如组件名、流程阶段、方法名、任务名、数据集名、指标名、横纵轴、图例、缩写和特殊符号。
- 证据条件：模型、场景、输入输出、上下文长度、硬件、batch、baseline、训练/推理阶段、阈值、配置或数据来源等影响口径的条件。
- 读图方法：先看哪里、怎样比较、箭头/颜色/数字/层级代表什么，以及如何从图中推出页面判断。
- 结论边界：该证据只能支持什么，不能外推到什么；不同口径的数字和概念不要混写。

如果主视觉材料缩小后仍能“看见”但不能“读懂”，应拆页、放大、局部裁切、重绘、标注或重建摘要；不要只满足图片渲染成功。

作为主证据使用的图片，页面渲染尺寸不得低于原图宽高的 80%。如果放不下，优先拆页、裁切/放大关键子图、重建表格或减少旁边内容。

输出目录：
<workspace-root>/<report-name>/source_understanding_review.html

```

## 审批 Gate（主Agent完成）

HTML 生成后，请用户审阅是否批准作为后续证据基线：

```text
请审阅 source-understanding HTML：
<workspace-root>/<main-report>/source_understanding_review.html
<workspace-root>/<reference-report>/source_understanding_review.html
<workspace-root>/<reference-report>/source_understanding_review.html

是否批准这些来源理解作为后续 PPT Content Brief 的证据基线？

1. 批准
```
