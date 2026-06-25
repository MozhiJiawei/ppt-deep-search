# 能力展示

`ppt-deep-search` 的作用不是直接画 PPT，而是在做 PPT 之前，把“材料很多、观点不稳、证据容易说过头”的问题先梳理清楚。
它会和用户一起确认来源理解、读者、判断口径、故事线和证据边界，最后交给下游 PPT 制作环节一份可直接使用的内容简报。

本页只展示当前仓库本地最新 forward-test 结果。
旧 showcase 叙述不再作为能力展示入口；历史可发布素材仍保留在 `docs/showcase/` 供追溯。

## 最新结果

最新完整 forward-test 运行是 2026-06-25 的 `20260625-forward-test-1`。
最新 Source Understanding 专项运行是 2026-06-25 的 `20260625-source-html-navcheck-1`。

| Case | 最新完整 forward | 最新 Source Understanding 专项 | 结论 |
| --- | --- | --- | --- |
| Aegaeon GPU Pooling | `Pass with issues` | `Pass with issues` | 完整 brief 无阻塞；Source Understanding 通过，但视觉 QA 修了五轮，说明复杂论文图表仍需要更早识别拥挤/截断问题。 |
| RTX Spark Agent PC Web Evidence | `Pass with issues` | `Pass` | 官方措辞边界和网页证据链处理较稳；完整 brief 的 QA 报告需要明确 `--allow-absolute-paths`。 |
| Stochastic KV Routing | `Pass with issues` | `Pass` | R-CLA 技术定位和证据边界清楚；完整 brief 同样需要明确本地图片路径的 QA 口径。 |

## 这轮验证了什么

完整 forward 运行验证：

- child agent 能按 HITL 流程完成 Source Understanding、PPT brief 受众/SCQA/页数/目录/页面观点确认。
- `ppt_content_brief.md` 能通过结构 QA；含本地图片绝对路径时，需要用 `--allow-absolute-paths` 明确声明工作区绑定。
- 最新 rubrics 已把 `review/source_understanding_review.html`、导出截图、`review/visual-qa.md` 和 source-understanding baseline 列为 judge-side 必查产物。

Source Understanding 专项运行验证：

- `scripts/validate_source_understanding_html.py` 能重新渲染 HTML deck，导出 PNG，并验证 ArrowRight / ArrowLeft 导航。
- RTX Spark 导出 8 页，Stochastic KV Routing 导出 9 页，Aegaeon 导出 12 页。
- 三个 case 都产出了 `review/source_understanding_review.html`、`review/source-understanding-images-maincheck/` 和 `review/visual-qa.md`。
- 独立视觉 QA 的 FAIL -> repair -> PASS 循环在复杂材料上有效，但 Aegaeon 的五轮修复提示后续还应继续降低图表可读性返工成本。

## 最新运行路径

这些路径是本地 forward-test 结果，不是发布资产：

| Case | 完整 forward judgment | Source Understanding judgment |
| --- | --- | --- |
| Aegaeon GPU Pooling | `.tmp/forward-tests/aegaeon-gpu-pooling-hitl/20260625-forward-test-1/judgment.md` | `.tmp/forward-tests/aegaeon-gpu-pooling-hitl/20260625-source-html-navcheck-1/judgment.md` |
| RTX Spark Agent PC Web Evidence | `.tmp/forward-tests/rtx-spark-agent-pc-web-evidence-hitl/20260625-forward-test-1/judgment.md` | `.tmp/forward-tests/rtx-spark-agent-pc-web-evidence-hitl/20260625-source-html-navcheck-1/judgment.md` |
| Stochastic KV Routing | `.tmp/forward-tests/stochastic-kv-routing-hitl/20260625-forward-test-1/judgment.md` | `.tmp/forward-tests/stochastic-kv-routing-hitl/20260625-source-html-navcheck-1/judgment.md` |

## 仍需改进

- HITL 选项必须在同一条 child response 中自包含；只说“请选择 1/2/3”会削弱 stakeholder 判断。
- 当 brief 使用本地绝对图片路径时，QA 报告必须显式说明 `--allow-absolute-paths`。
- Source Understanding 视觉 QA 已能拦住拥挤和不可读证据，但复杂论文图表仍可能需要多轮 repair。

## 刷新规则

刷新本页时，先找每个 case 下最新的 `.tmp/forward-tests/<case-id>/<run-id>/judgment.md`。
只有在 judgment 存在、路径位于正确 run 目录、且相关产物存在时，才把结果写入本页。

不要把 judge-only rubric、hidden fixtures、交互策略或未清理的工作区绝对路径复制进发布素材。
