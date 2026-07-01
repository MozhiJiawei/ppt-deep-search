# 架构设计

本文是 `ppt-deep-search` 的开发期维护契约。
`SKILL.md` 面向运行时 agent；本文说明维护者改动运行行为时，哪些文档、引用、脚本和 forward test 必须同步。

## 运行契约

`ppt-deep-search` 负责下游 PPT 生成前的研究对齐，不负责渲染最终 HTML 演示文稿。

运行流程分两段：

1. Source Understanding 审阅 gate。
   agent 生成 `review/source_understanding_review.html`，导出截图，在 `review/visual-qa.md` 记录独立视觉 QA，并保存已批准的 source-understanding baseline。
2. PPT Content Brief HITL。
   agent 确认最终 PPT 的受众、SCQA、页数口径、目录和页面观点，然后写入 `ppt_content_brief.md`。

Source Understanding gate 不是可选步骤。
在 Source Understanding 产物获批或记录明确 blocker 之前，`SKILL.md` 不得进入 `references/ppt-brief-hitl.md`。

## 产物归属

一次运行只使用一个 task root，通常是 `.tmp/ppt-deep-search/<task-name>/` 或 `.tmp/forward-tests/<case-id>/<run-id>/`。

Source Understanding 必需产物：

- `review/source_understanding_review.html`
- `review/source-understanding-images/`
- `review/visual-qa.md`
- `baselines/015-source-understanding.md`

最终 handoff：

- `ppt_content_brief.md`

最终 handoff 面向下游 PPT 制作者。
它不能包含 judge 记录、审计痕迹、approval log 或作者侧 source-locator 表格。
这些记录应留在 `review/`、`sources/`、`baselines/` 或 QA 日志中。

## 引用文件

`SKILL.md` 保持短小，只放路由、硬 gate、工作区契约和最终交付物。

详细行为放在 references：

- `references/evidence-principle.md` 和 `references/evidence-examples.md` 定义表达质量、证据优先级、图片使用和金字塔式主张。
- `references/source-understanding-html-ppt.md` 定义 Source Understanding HTML deck、截图导出、独立视觉 QA 和审批 gate。
- `references/ppt-brief-hitl.md` 定义最终 PPT brief HITL、JSON 形态、骨架生成、可见文案检查和最终 brief QA。

运行规则变化时，必须更新对应 reference。
如果规则能被机器检查，应新增或调整可执行 gate，而不是只写 prose。

## 脚本 gate

仓库级依赖和契约检查入口是 `verify_dependencies.py`。

当前脚本职责：

- `scripts/validate_markdown_size.py` 检查 Markdown size budget。
- `scripts/validate_source_understanding_html.py` 用 Playwright 把 Source Understanding HTML 渲染成 PNG，检查翻页导航，并执行图片缩放硬 gate。
- `scripts/hitl_json_to_brief_skeleton.py` 把已批准的 HITL JSON 转成 `ppt_content_brief.md` 骨架；支持一页 summary-only brief，此时 TOC 和内容页可以为空。
- `scripts/validate_ppt_content_brief.py` 检查最终 brief 的结构、可见文案、密度和预期页数。

产物是否存在、baseline 是否已批准、HTML 是否可渲染，不应只依赖文字说明。
能写 validator 的规则应写成 validator。

## Forward Tests

Forward test 是 main-agent 编排流程，candidate 必须在隔离 child agent 中运行。
main agent 扮演 human stakeholder，并写入 `judgment.md`。

Forward-test 指令必须保持 judge-side：

- candidate dispatch 保持最小化，不得包含 rubric 或预期失败模式。
- judge rubric 和 fixture manifest 必须要求 Source Understanding 审阅产物，之后才能接受最终 brief。
- web-source case 还必须要求 `sources/web/<source-slug>/` 抓取包和 capture validator 证据。

截至 2026-06-25 的最新本地 forward-test 证据：

- `20260625-forward-test-1` 完成了 `aegaeon-gpu-pooling-hitl`、`rtx-spark-agent-pc-web-evidence-hitl` 和 `stochastic-kv-routing-hitl` 的完整运行。三者都是 `Pass with issues`，没有剩余 blocking finding。
- `20260625-source-html-navcheck-1` 完成了同三组 case 的 Source Understanding-only 运行。RTX Spark 和 Stochastic KV Routing 是 `Pass`；Aegaeon 是 `Pass with issues`，原因是视觉 QA 需要五轮修复。
- 最新 source-only 运行验证了 Source Understanding HTML 渲染路径、PNG 导出、独立视觉 QA 记录和键盘翻页 gate。

刷新发布展示文档时，先读取 `.tmp/forward-tests/<case-id>/` 下最新 run 的 `judgment.md`。
只把可发布、安全的产物复制进 `docs/showcase/` 或 `docs/assets/forward-tests/`。

## 变更纪律

运行行为变化必须同步更新相关运行文档、references、脚本和 forward-test judge expectations。

提交前至少运行：

```powershell
python scripts/validate_markdown_size.py .
python verify_dependencies.py --skip-services
```

如果改动 validator 或 generator，还要运行对应的 targeted self-test。
如果改动 Source Understanding 或 brief-HITL 行为，还要运行或检查相关 forward-test 结果，并记录验证了什么。
