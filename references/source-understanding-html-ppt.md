# Source Understanding HTML PPT

本文件规定如何根据 `html-ppt-skill` 和信息源，制作 Source Understanding HTML PPT。

## 输出目标

- 产出 `<workspace-root>/review/source_understanding_review.html`。
- 批准后记录 `<workspace-root>/baselines/015-source-understanding.md`。

## 来源准备 HITL

先根据用户输入的信源、主题和已知缺口判断输入类型。所有场景都写入 `<workspace-root>/sources/source-selection.md`。
  - 输入类型：`web` 或 `paper`。
  - 原始来源清单。
  - 对照研究/同类方案清单。

### 场景 A：输入是网页

网页抓取前必须先让用户确认来源。最多选择 3 个最相关原始页面和 2 个同类/相邻/竞品方案；不足时说明原因，不用低相关材料凑数。

```text
请先确认 Source Understanding 的信息来源。确认后进入网页抓取。

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

### 场景 B：输入是论文

跳过来源准备 HITL gate。

## 来源获取

网页来源按页面分别委派给子 agent 抓取。每个子 agent 只处理一个网页，产出独立 source package，并运行页面 validator。

```text
请使用仓库 `web-article-capture/SKILL.md` 抓取单个网页来源。

网页：
- 标题：<title>
- URL：<url>
- Source slug：<source-slug>

输出目录：
<workspace-root>/sources/web/<source-slug>/

要求：
- 只处理这个网页，不处理其他来源
- 写出 source package：`source.md` + `images/`
- 保留正文阅读顺序、原始图片、图片来源 URL、caption 或附近文本
- 完成后运行：
  python web-article-capture/scripts/validate_capture_package.py <workspace-root>/sources/web/<source-slug> --require-images when-referenced
```

## 制作 HTML PPT

根据已确认/已抓取的信息源，使用 html-ppt-skill 制作 Source Understanding HTML deck。

听众：“不了解该技术的技术小白”
目标：让听众快速建立技术心智模型。内容应结论先行，并解释问题背景、同类路线、关键机制、效果证据与证据边界；重要判断必须有脚注或引用可追溯。

请由 html-ppt-skill 根据内容选择合适的主题、模板、布局和页数。视觉偏好是白底、冷静、工程化、高信息密度，可优先考虑 swiss-grid / engineering-whiteprint / academic-paper 等风格。

高信息密度指：用机制图、对比矩阵、指标表、证据截图标注、引用链呈现可验证关系；不要用营销式大标题或低信息密度留白。证据图表必须可读，必要时拆页、局部放大、重绘或做表格化摘要。

主视觉材料必须优先服务“读懂”，而不是堆材料。图、表、截图、机制图、架构图或代码片段只要承载页面判断，就必须配套解释，让读者不用猜画面元素和判断之间的关系。若一个视觉材料承载独立判断，默认一页只放一个主视觉材料；不要把多个高信息密度材料压在同一页里让读者自行拼接。每个主视觉材料必须解释：

- 图中关键字：例如组件名、流程阶段、方法名、任务名、数据集名、指标名、横纵轴、图例、缩写和特殊符号。
- 证据条件：模型、场景、输入输出、上下文长度、硬件、batch、baseline、训练/推理阶段、阈值、配置或数据来源等影响口径的条件。
- 读图方法：先看哪里、怎样比较、箭头/颜色/数字/层级代表什么，以及如何从图中推出页面判断。
- 结论边界：该证据只能支持什么，不能外推到什么；不同口径的数字和概念不要混写。

如果主视觉材料缩小后仍能“看见”但不能“读懂”，应拆页、放大、局部裁切、重绘、标注或重建摘要；不要只满足图片渲染成功。

作为主证据使用的图片，页面渲染尺寸不得低于原图宽高的 80%。如果放不下，优先拆页、裁切/放大关键子图、重建表格或减少旁边内容。

必须使用 html-ppt-skill 标准 runtime；导出截图供视觉审阅，检查翻页能力、破图、横向溢出、遮挡、标题可见、证据可读和引用完整。

### 截图导出

生成后运行：
  `python scripts/validate_source_understanding_html.py <workspace-root>/review/source_understanding_review.html all <workspace-root>/review/source-understanding-images`

如果命令非 0 或输出 `[ERROR]`，请修复问题后重跑。

#### 视觉 QA checker

命令通过后，必须委派独立视觉 QA checker 子 agent。生成者不得自己看脚本输出后自判通过。

启动 checker 前，主 agent 不要在主流程中展开 checker 细则；应让 checker 子 agent 读取并执行独立 rubric：

checker prompt：

```text
你是 Source Understanding HTML PPT 的独立视觉 QA checker。只审查，不改文件。

请按校验规则，完成任务：
skills/ppt-deep-search/references/source-understanding-checker-rubric.md

```

checker 返回 `PASS` 后，生成者再进入审批 Gate。checker 返回 `FAIL` 时，修复 HTML，重新运行`validate_source_understanding_html.py`命令刷新导出图并重新委派 checker。

将视觉 QA 记录写入 `<workspace-root>/review/visual-qa.md`，并明确记录 checker agent 的 Verdict 和关键原始意见；不要把生成者自己的截图观察写成独立 QA 结论。

## 审批 Gate

HTML 生成后，请用户审阅是否批准作为后续证据基线：

```text
请审阅 source-understanding HTML：
<workspace-root>/review/source_understanding_review.html

是否批准这份来源理解作为后续 PPT Content Brief 的证据基线？

1. 批准
```
