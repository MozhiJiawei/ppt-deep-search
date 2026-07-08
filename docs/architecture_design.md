# 架构设计

本文是 `ppt-deep-search` 的开发期维护契约。
`SKILL.md` 面向运行时 agent；本文说明维护者改动运行行为时，哪些文档、引用、脚本和 forward test 必须同步。

## 运行契约

`ppt-deep-search` 负责下游 PPT 生成前的来源理解审阅，不负责生成 PPT、不负责规划故事主线，也不产出内容简报。

运行流程只有一段：

1. Source Understanding 审阅 gate。
   agent 生成 `review/source_understanding_review.html`，导出截图，在 `review/visual-qa.md` 记录独立视觉 QA，并保存已批准的 source-understanding baseline。

Source Understanding gate 不是可选步骤。用户批准 `source_understanding_review.html` 后，本 skill 的职责结束。

## 子 Agent 分层

`ppt-deep-search` 使用两层子 agent 编排：

- 本 skill 子仓 `.codex/agents/*.toml` 保存原子 agent 的稳定静态 prompt。
- `references/source-understanding-html-ppt.md` 保存运行时调度规则，包括何时调用哪个 custom agent，以及每次 spawn 时必须补充的动态占位内容。

不要把本次 URL、PDF、source slug、输出目录或来源列表固化进 agent TOML。主 agent 必须根据当前任务动态补全 reference 中的占位符。

当前 Source Understanding 相关 custom agents：

- `web_source_capturer`
- `paper_source_parser`
- `source_understanding_deck_maker`

## 产物归属

一次运行只使用一个 task root，通常是 `.tmp/ppt-deep-search/<task-name>/` 或 `.tmp/forward-tests/<case-id>/<run-id>/`。

必需产物：

- `review/source_understanding_review.html`
- `review/source-understanding-images/`
- `review/visual-qa.md`
- `baselines/015-source-understanding.md`
- `sources/**`

不要新增额外交接文件、PPT 内容简报、页数规划、目录规划、SCQA 或逐页观点产物。后续 PPT-GEN 可以直接读取已批准的 review 和 sources，但该动作不属于本 skill。

## 引用文件

`SKILL.md` 保持短小，只放路由、硬 gate、工作区契约和最终交付物。

详细行为放在 references：

- `references/source-understanding-html-ppt.md` 定义 Source Understanding HTML deck、截图导出、独立视觉 QA 和审批 gate。

运行规则变化时，必须更新对应 reference。
如果规则能被机器检查，应新增或调整可执行 gate，而不是只写 prose。

## 脚本 gate

仓库级依赖和契约检查入口是 `verify_dependencies.py`。

当前脚本职责：

- 检查本 skill 子仓 `.codex/agents/*.toml` 的必需 custom agent 文件存在。
- `scripts/validate_markdown_size.py` 检查 Markdown size budget。
- `scripts/validate_source_understanding_html.py` 用 Playwright 把 Source Understanding HTML 渲染成 PNG，检查翻页导航，并执行图片缩放硬 gate。

产物是否存在、baseline 是否已批准、HTML 是否可渲染，不应只依赖文字说明。
能写 validator 的规则应写成 validator。

## Forward Tests

Forward test 是 main-agent 编排流程，candidate 必须在隔离 child agent 中运行。
main agent 扮演 human stakeholder，并写入 `judgment.md`。

Forward-test 指令必须保持 judge-side：

- candidate dispatch 保持最小化，不得包含 rubric 或预期失败模式。
- judge rubric 和 fixture manifest 必须要求 Source Understanding 审阅产物。
- web-source case 还必须要求 `sources/web/<source-slug>/` 抓取包和 capture validator 证据。
- 不得要求内容简报、简报 QA、PPT 页级故事线或下游 PPT 生成产物。

截至 2026-06-25 的最新本地 forward-test 证据：

- `20260625-source-html-navcheck-1` 完成了 `aegaeon-gpu-pooling-hitl`、`rtx-spark-agent-pc-web-evidence-hitl` 和 `stochastic-kv-routing-hitl` 的 Source Understanding-only 运行。RTX Spark 和 Stochastic KV Routing 是 `Pass`；Aegaeon 是 `Pass with issues`，原因是视觉 QA 需要五轮修复。
- 最新 source-only 运行验证了 Source Understanding HTML 渲染路径、PNG 导出、独立视觉 QA 记录和键盘翻页 gate。

刷新发布展示文档时，先读取 `.tmp/forward-tests/<case-id>/` 下最新 run 的 `judgment.md`。
只把可发布、安全的 Source Understanding HTML、截图和必要静态资源复制进 `docs/showcase/` 或 `docs/assets/forward-tests/`。

## 变更纪律

运行行为变化必须同步更新相关运行文档、references、脚本和 forward-test judge expectations。

提交前至少运行：

```powershell
python scripts/validate_markdown_size.py .
python verify_dependencies.py --skip-services
```

如果改动 validator，还要运行对应的 targeted self-test。
如果改动 Source Understanding 行为，还要运行或检查相关 forward-test 结果，并记录验证了什么。
