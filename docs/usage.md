# 使用方式

`ppt-deep-search` 不是一轮总结器，而是生成 PPT 前的研究对齐流程。它先让人审阅 source understanding，再确认最终 PPT 的读者、问题、证据边界和故事线，最后输出下游 PPT skill 可消费的内容包。

## 适用场景

使用这个 skill 处理以下任务：

- 从论文、网页、Markdown、仓库分析、PDF、笔记或原始材料中整理 PPT 观点。
- 在正式生成 HTML 演示文稿之前，先确认读者认知路径、SCQA、章节逻辑和页面观点。
- 把来源证据、推理边界、用户审批和 QA 记录保存在工作过程或 baselines 中，避免下游 PPT 文案混入内部工作记录。

不要用它做演示文稿视觉渲染、版式模板、字体配色、导出或视觉 QA。这些属于下游 PPT 制作 skill。

## 标准流程

默认走 human-in-the-loop：

1. 做 source understanding，让用户先审研究理解、证据、比较对象和边界。此阶段读者固定为“想要系统性了解该技术原理的人”。
2. 确认最终 PPT 的目标读者、读者当前判断、希望改变的判断、最终用途和来源集合，并写入 `ppt_brief_hitl.json`。
3. 确认 SCQA 和顶层 summary page 表达，包括 `页面标题`、`标题说明`、`分析总结`。
4. 单独确认页数口径，不提前生成目录。
5. 确认 Table of Contents，目录最多 3 个章节项，目录项是导航文案，不是证据地图。
6. 按章节逐步确认页面观点层：页面标题、标题说明、分析总结、正文支撑和参考图片策略。
7. 写入 `ppt_content_brief.md`，并运行最终 brief QA。

每个阶段都有两个门：先获得用户 approval，再把该阶段基线保存到 `<workspace-root>/baselines/`。已批准的基线不能被静默重写；如果后续证据要求调整，需要重新请用户确认并记录在 `Approval Log`。

## 工作目录

一次运行只使用一个 `workspace-root`：

- 默认路径：`.tmp/ppt-deep-search/<task-name>/`
- forward-test 路径：`.tmp/forward-tests/<case-id>/<run-id>/`
- 用户指定输出目录时，以用户指定目录为准

所有临时笔记、baseline、资产和 QA 输出都放在这个目录下。最终交付物固定为：

- `<workspace-root>/ppt_content_brief.md`

Source Understanding 阶段还必须产生这些中间评审产物：

- `<workspace-root>/review/source_understanding_review.html`
- `<workspace-root>/review/source-understanding-images/`
- `<workspace-root>/review/visual-qa.md`
- `<workspace-root>/baselines/015-source-understanding.md`

## 交付物

`ppt_content_brief.md` 是下游 PPT 文案包，只放可直接引用、改写或放进页面的内容：

- Deck Metadata
- Summary Page
- Table of Contents
- Page Content

不该进入 PPT 文案的内部信息应留在工作过程或 baselines 中，不写进 `ppt_content_brief.md`：

- 读者和信念变化
- source understanding
- pyramid outline
- Claim/Evidence/Implication
- source locators 和 usage policy
- supplemental research
- assumptions/open questions
- approval log

如果任务需要网页来源，优先使用可信来源包或仓库内 `web-article-capture/SKILL.md` 获取网页正文和图片证据。不要用搜索摘要、raw HTML、`curl` 抓取结果或手写网页摘录替代可追溯来源。

## 校验命令

最终 brief 写完后，按页数口径运行：

```powershell
python scripts/validate_ppt_content_brief.py <workspace-root>/ppt_content_brief.md --expected-pages <total-pages>
```

如果 brief 中的 `参考图片` 使用本地绝对路径，测试或 forward judgment 可加：

```powershell
python scripts/validate_ppt_content_brief.py <workspace-root>/ppt_content_brief.md --expected-pages <total-pages> --allow-absolute-paths
```

Source Understanding HTML 写完后，运行：

```powershell
python scripts/validate_source_understanding_html.py <workspace-root>/review/source_understanding_review.html all <workspace-root>/review/source-understanding-images
```

仓库级依赖与契约检查：

```powershell
python verify_dependencies.py
```
