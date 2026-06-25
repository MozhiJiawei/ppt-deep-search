# Aegaeon GPU Pooling 内容简报

## Deck Metadata

主题：Aegaeon: Effective GPU Pooling for Concurrent LLM Serving on the Market

目标读者：云厂商推理平台负责人、GPU 资源池架构负责人

页数口径：7 页，包含 cover、summary、contents 和 4 页正文

核心结论：Aegaeon 的关键不是单纯加速模型冷启动，而是把 autoscaling 的控制点前移到 token 边界；它用 broker、prefill/decoding 分池、显式内存治理和 KV cache 同步，让多模型市场的 GPU pooling 从 2-3 个 active model 上限继续向前推进。

## Summary Page

页码：Page 2

页面标题：Aegaeon 突破 3 模型上限

页面意图：用一页说明 GPU 浪费来自“低频长尾 + 热门突发”的组合，而 Aegaeon 的答案是 token 级 autoscaling。

作者提示：

- 第一屏不要只写“97% overhead reduction”。先解释为什么 request-level autoscaling 要等完整请求结束，导致 head-of-line blocking。
- 摘要页允许一页完成，但要分层：左侧讲负载问题，中间讲 token-level autoscaling，右侧讲系统落地约束。
- “3 模型上限”是论文语境下 multiplexing/request-level autoscaling 的效果瓶颈，不是硬件物理定律。

参考图片：

![Workload skew and bursts](brief-assets/picture_002.png)

![Request-level versus token-level autoscaling](brief-assets/picture_003.png)

![Aegaeon system overview](brief-assets/picture_006.png)

## 目录结构

| 页码 | 页面标题 | 作者任务 |
| --- | --- | --- |
| Page 4 | 长尾模型吃掉 17.7% GPU | 建立 GPU pooling 必要性，证明 dedicated GPU 与峰值冗余不匹配。 |
| Page 5 | active model 锁住池化效率 | 对比 multiplexing、request-level autoscaling 与 token-level autoscaling 的控制粒度。 |
| Page 6 | broker 把 token 变成调度点 | 展示 broker、client app、GPU worker、prefill/decoding pool 如何协同。 |
| Page 7 | 收益来自切换成本被压低 | 用实验和生产 beta 说明收益，同时保留 SLO、低延迟场景和生产冗余边界。 |

## Page 4: 长尾模型吃掉 17.7% GPU

核心表达：模型市场不是单模型服务，779 个模型中 94.1% 低频模型只贡献 1.35% 请求，却占用 17.7% GPU；热门模型又会短时超过 reserved capacity。两类负载共同把平台推向过量配置。

制作建议：

- 用 workload skew 和 top model burst 两张图做左右对照。
- 图注明确“长尾造成长期保留，热门突发造成峰值冗余”。
- 不在这一页提前展开 token-level autoscaling，只建立问题。

参考图片：

![Workload skew and hot model burst](brief-assets/picture_002-2.png)

## Page 5: active model 锁住池化效率

核心表达：multiplexing 受 GPU 显存里的 active model count 限制，request-level autoscaling 虽可换入模型，但必须等当前请求结束。LLM 的长 prefill 与多轮 decoding 会放大等待时间，导致 request-level 调度仍难承接高并发市场负载。

制作建议：

- 画三列：dedicated GPU、multiplexing、request-level autoscaling。
- 每列只保留一个关键瓶颈：冗余、显存上限、请求边界阻塞。
- 结尾引出 Aegaeon：真正变化是把调度边界从 request 变成 token。

## Page 6: broker 把 token 变成调度点

核心表达：Aegaeon 用 broker 管理模型状态和调度决策；client app 提供请求入口；GPU worker 执行 prefill 与 decoding；KV cache 在 CPU 与 GPU 之间同步。它不是一个单点优化，而是调度、内存和状态恢复的组合系统。

制作建议：

- 主图用系统架构图，突出 broker 与两个 GPU pool。
- 用编号标出 “prefill arrival -> decoding iteration -> token boundary preemption -> KV cache sync”。
- 注意把“token-level autoscaling”解释成可抢占点，不要写成每个 token 都必然换模型。

参考图片：

![Aegaeon system overview](brief-assets/picture_006-2.png)

## Page 7: 收益来自切换成本被压低

核心表达：token 级 autoscaling 只有在切换成本足够低时才成立。Aegaeon 通过 component reuse、显式 GPU/host memory management、model cache、统一 CPU KV cache 和 fine-grained KV cache synchronization，将 autoscaling overhead 降低 97%，实验报告 2-2.5x higher request arrival rates 或 1.5-9x more goodput。

制作建议：

- 将收益数字与前置条件绑定展示。
- 生产 beta 的 H20 GPU 从 1,192 降到 213 可作为强记忆点，但要注明这是生产部署口径。
- 边界页必须保留：低延迟强约束、SLO 配置、冗余策略和模型切换成本都影响可采用性。

参考图片：

![Performance comparison](brief-assets/picture_017.png)
