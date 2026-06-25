# ppt-deep-search 效果展示

`ppt-deep-search` 是一个面向“深度检索型 PPT 生成”的 Skill：它先做来源理解和可视证据审查，再进入可交付的演示文稿内容组织。这个页面展示最近一轮 forward-test 的公开样例，重点看三件事：

- 候选 agent 是否能把来源证据读透，而不是只摘关键词。
- HIL 审批、来源理解审查、视觉 QA 是否形成闭环。
- 最终 `ppt_content_brief.md` 是否像给作者用的制作简报，而不是给观众看的演讲稿。

## 展示方式

本页只引用 `docs/showcase/latest/` 下的发布副本。forward-test 的运行目录只作为刷新来源，文档中不直接依赖临时运行产物。

每个样例只归档两类最终交付件：来源理解 HTML 和最终 `ppt_content_brief.md`。过程记录、检查记录和临时运行文件不进入展示目录。

| 样例 | 任务主题 | 最新结论 | 最终交付件 |
| --- | --- | --- | --- |
| Aegaeon GPU Pooling | 云 GPU 池化与 broker 架构 | 通过，仍需压缩摘要页信息密度 | [HTML](showcase/latest/aegaeon-gpu-pooling/source_understanding.html) / [内容简报](showcase/latest/aegaeon-gpu-pooling/ppt_content_brief.md) |
| RTX Spark Agent PC | NVIDIA DGX Spark 与 Agent PC | 通过，官方来源边界更清楚 | [HTML](showcase/latest/rtx-spark-agent-pc/source_understanding.html) / [内容简报](showcase/latest/rtx-spark-agent-pc/ppt_content_brief.md) |
| Stochastic KV Routing | Moonshot AI 的随机 KV 路由 | 通过，技术链路与图表复建更稳定 | [HTML](showcase/latest/stochastic-kv-routing/source_understanding.html) / [内容简报](showcase/latest/stochastic-kv-routing/ppt_content_brief.md) |

## Aegaeon GPU Pooling

这个样例要求 agent 将 Aegaeon 论文与项目材料重构成 PPT 作者可用的简报。最新结果已经能把“broker 协调、GPU worker、客户端应用、基准曲线”放进同一条叙事链，并保留来源图表证据。

可继续改进的是摘要页的一页承载量：forward judge 认为候选输出能覆盖关键概念，但第 2 页等 summary 页仍偏拥挤，需要把读者结论和图表证据进一步分层。

最终交付件：

- [来源理解 HTML](showcase/latest/aegaeon-gpu-pooling/source_understanding.html)
- [内容简报](showcase/latest/aegaeon-gpu-pooling/ppt_content_brief.md)

## RTX Spark Agent PC

这个样例检查 agent 面对厂商网页、平台介绍和生态材料时，能否区分“官方确定信息”和“行业解读”。最新结果把 DGX Spark、RTX PRO、Blackwell、AI Workbench、NVIDIA Blueprint 等材料归入清晰的证据层级，避免把网页营销语直接写成无来源判断。

可继续改进的是互动表达：候选 agent 的选择题需要在同一条消息里完整列出选项文本，减少主 agent 作为 stakeholder 时需要回看上下文的成本。

最终交付件：

- [来源理解 HTML](showcase/latest/rtx-spark-agent-pc/source_understanding.html)
- [内容简报](showcase/latest/rtx-spark-agent-pc/ppt_content_brief.md)

## Stochastic KV Routing

这个样例围绕 Moonshot AI 的随机 KV 路由论文，要求 agent 把算法动机、公式、表格和实验图重新组织为技术型 PPT。最新结果已经能把 `distributional equality`、随机路由器、容量受限调度、chunk prefill 与 Decode-Context Parallelism 之间的关系讲清楚。

可继续改进的是密集证据页的阅读节奏：技术表格和公式引用已经保留，但仍需要控制每页的说明字数，让核心结论先于证据细节出现。

最终交付件：

- [来源理解 HTML](showcase/latest/stochastic-kv-routing/source_understanding.html)
- [内容简报](showcase/latest/stochastic-kv-routing/ppt_content_brief.md)

## 最新验证结论

- 来源理解审查已经能稳定暴露“只读摘要、不读图表”的弱点，并通过 HTML 与截图保留可复查证据。
- 内容简报可以保留一页 summary，但 summary 页必须服务 PPT 作者：先给页面意图和观众要带走的判断，再给图表、引用和重建建议。
- HIL 交互还需要更严格：候选 agent 问选择题时，应在同一条消息里列出完整选项文本。
- 文档展示区必须是发布副本。刷新时先定位最新 forward-test 结果，再只把最终 HTML、最终 `ppt_content_brief.md` 及其必要图片/CSS/JS 依赖复制进 `docs/showcase/latest/`，最后更新本页链接。

## 刷新规则

刷新本页时只替换 `docs/showcase/latest/` 的内容，不恢复旧样例目录，也不让文档链接到运行缓存。若新增样例，需要同时更新本页表格、样例章节、来源理解 HTML、内容简报和它们的必要静态资源；不要归档内部过程产物。
