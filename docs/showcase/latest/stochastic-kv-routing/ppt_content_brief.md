# Stochastic KV Routing / R-CLA 内容简报

## Deck Metadata

主题：Stochastic KV Routing: Enabling Adaptive Depth-Wise Cache Sharing

目标读者：负责大模型推理成本优化的技术负责人

页数口径：6 页，包含 cover、summary、contents 和 3 页正文

核心结论：R-CLA 值得进入小规模受控复测。它把 cache 缺层变成训练期扰动，证据显示低 retention 下质量更稳、长上下文下显存和吞吐受益；但上线判断必须受训练成本、任务覆盖和业务评测限制。

## Summary Page

页码：Page 2

页面标题：R-CLA 值得复测，不宜直上

页面意图：给技术负责人一个决策口径：这不是立刻上线的推理侧开关，而是值得复现验证的训练期鲁棒化路线。

作者提示：

- 先解释 KV cache 成本的深度轴，再讲随机路由。
- “g=4 约四分之一 cache” 要绑定 Table 4 的实验条件。
- 保留边界：需要训练资源，QA 任务不能代表所有业务任务。

参考图片：

![R-CLA behavior](brief-assets/picture_005.png)

![Inference efficiency table](brief-assets/table_004.png)

![QA retention table](brief-assets/table_002.png)

## 目录结构

| 页码 | 页面标题 | 作者任务 |
| --- | --- | --- |
| Page 4 | KV 成本还在深度轴 | 区分时间轴裁剪与深度轴共享，说明 R-CLA 的问题切入。 |
| Page 5 | 随机路由让缺层变可学 | 解释训练期随机跨层读 KV，部署时固定共享为何更稳。 |
| Page 6 | 复测要同时看质量和系统账 | 把质量、显存、TTFT、吞吐、训练成本和任务覆盖放进同一决策表。 |

## Page 4: KV 成本还在深度轴

核心表达：KV cache 随 batch size、sequence length 和 model depth 线性增长。现有方法多沿时间轴判断哪些 token 可丢，R-CLA 换到深度轴，问是否每一层都必须保留自己的 K/V states。

制作建议：

- 用 “时间轴裁剪 / 深度轴共享” 做路线矩阵。
- 说明深度共享不是直接删除上下文 token，因此可与量化、GQA、调度类方法组合。
- 不要在这一页暗示 R-CLA 已经可以上线。

参考图片：

![KV cache framing](brief-assets/picture_002.png)

## Page 5: 随机路由让缺层变可学

核心表达：R-CLA 在训练时让每层以概率读取自己或前层 KV，让模型习惯“本层 KV 不可用”的结构扰动。部署时再固定分组共享，例如 g=4 让连续四层共享一份 cache。

制作建议：

- 主图展示训练期 stochastic routing 与部署期 grouped sharing。
- 把 distributional equality 作为关键理论直觉：训练和推理看到的 KV 来源分布要对齐。
- Table 2 只摘最能说明低 retention 鲁棒性的行，不要整表塞满。

参考图片：

![R-CLA training and inference behavior](brief-assets/picture_005-2.png)

![QA quality under retention](brief-assets/table_002-2.png)

## Page 6: 复测要同时看质量和系统账

核心表达：R-CLA 的价值必须同时看质量与系统收益。Table 4 显示在 Qwen3-8B、单张 80GB GPU、bfloat16 等条件下，g=4 能显著降低 KV cache；但这仍是论文条件下的结果，内部复测需要覆盖业务任务、长上下文、训练成本和回退策略。

制作建议：

- 用一张决策表列出：质量、显存、TTFT、吞吐、训练成本、任务覆盖、回退策略。
- 结论写成“进入受控复测”，不要写成“直接上线”。
- 对比 CLA、R-CLA、基线时，强调不同 retention 点的表现会变化。

参考图片：

![Inference efficiency table](brief-assets/table_004-2.png)
