# Research Audit

## Research Frame

Task: prepare a PPT-ready content brief for an internal serving architecture evaluation deck about Aegaeon token-level GPU pooling.

Workspace root: `docs/showcase/published-run`

Target reader: technical product / infrastructure leadership evaluating whether token-level GPU pooling is worth adapting to their multi-model LLM serving stack.

Reader's likely starting belief: GPU pooling is attractive for OPEX, but serving stack migration carries scheduler, SLO, memory, KV cache, and runtime lifecycle risk.

Desired belief change: Aegaeon is worth bounded architecture evaluation and local retesting, but Alibaba Cloud's beta deployment saving must not be treated as guaranteed benefit for our stack.

Final use: pre-PPT content brief for an internal serving architecture evaluation deck.

Approved page count: 7 total PPT pages, including cover, summary page, and contents page.

Primary source package:

- `forward-tests/ppt-deep-search\aegaeon-gpu-pooling-hitl\candidate\input\pdf_xml\final\Aegaeon Effective GPU Pooling for Concurrent LLMServing on the Market.xml`
- `forward-tests/ppt-deep-search\aegaeon-gpu-pooling-hitl\candidate\input\pdf_xml\final\images\`

## Source Understanding

Approved source-understanding review:

- `docs/showcase/published-run`
- `docs/showcase/published-run`

Key understanding approved by the user:

- Aegaeon targets production-like multi-model LLM serving on a model marketplace, where long-tail low-frequency models and bursty hot models create GPU waste.
- The mechanism is token-level auto-scaling, with prefill/decoding disaggregation, TTFT/TBT-aware scheduling, component reuse, explicit memory management, and fine-grained KV cache synchronization.
- Strong source numbers include 94.1% of 779 models accounting for 1.35% of 167.6M requests while using 17.7% of 30K GPUs; 2-2.5x higher request arrival rates or 1.5-9x more goodput; beta deployment serving tens of models from 1.8B to 72B and reducing GPUs from 1,192 to 213.
- Non-negotiable boundary: Alibaba Cloud beta deployment and 82% GPU saving are strong signals, not guaranteed savings for our serving stack.

Important source figures/tables inspected:

- Figure 1 / `picture_002.png`: concurrent LLM serving workloads, long-tail CDF and hot-model burst.
- Figure 2 / `picture_003.png`: request-level auto-scaling vs token-level auto-scaling.
- Figure 4 / `picture_005.png`: active model count over time, estimated E[m] = 46.55.
- Figure 7 / `picture_008.png`: preemptive scaling process and inference engine initialization breakdown.
- Figure 9 / `picture_010.png`: explicitly managed memory in Aegaeon and unified KV cache operation.
- Figure 10 / `picture_011.png`: fine-grained KV cache synchronization.
- Figure 11 / `picture_013.png`: end-to-end SLO attainment under varying RPS with ShareGPT.
- Figure 13 / `picture_012.png`: SLO attainment under varying model count and arrival rate.
- Figure 18 / `picture_017.png`: GPU utilization before and after Aegaeon deployment.

## Executive Thesis

Approved thesis: "先评估，再承诺收益."

The deck should argue that Aegaeon is relevant enough for bounded architecture evaluation because it connects production workload statistics, token-level scale decision, SLO-aware scheduling, and beta deployment evidence. It should also make clear that the Alibaba Cloud beta
deployment result is not directly transferable to our stack without local workload, SLO, KV cache, engine lifecycle, model mix, and switching-cost validation.

## Reader Cognitive Path

1. Start from the reader's decision: whether to invest in adapting token-level GPU pooling.
2. Establish workload fit before mechanism: if our model market is not long-tail and bursty, Aegaeon's upside weakens.
3. Explain mechanism as testable components: token boundary scale decision, prefill/decoding split, TTFT/TBT scheduling, switching-cost optimizations.
4. Weigh evidence: SLO curves and beta deployment justify retesting priority, not production commitment.
5. End with local gates: SLO definition, KV cache movement/sync, engine lifecycle/reuse, model mix, switching latency, SLO violation, GPU utilization, fallback cost.

## Pyramid Outline

Top-level summary page:

- Page 2: 先评估，再承诺收益

Supporting chapter claims:

- 长尾浪费是真问题: workload fit determines whether evaluation is relevant.
- 可试点在 token boundary: mechanism is concrete and decomposable, but switching cost is the hard part.
- 证据足够支持复测: source evidence is enough to prioritize retesting, but not enough to promise savings.
- 迁移要过本地 gate: adaptation should proceed only after local serving gates pass.

## Chapter Logic

Chapter 01: 长尾浪费是真问题

- Uses production workload statistics and burst behavior to decide whether the Aegaeon problem applies to our environment.
- Does not discuss implementation yet.

Chapter 02: 可试点在 token boundary

- Explains the mechanism at the level needed for architecture evaluation.
- Makes token boundary, prefill/decoding split, TTFT/TBT, and switching-cost components explicit.

Chapter 03: 证据足够支持复测

- Uses controlled SLO/capacity curves and beta deployment numbers to justify retesting priority.
- Separates Alibaba Cloud results from our expected benefit.

Chapter 04: 迁移要过本地 gate

- Converts the previous pages into local evaluation gates and next-step decision criteria.
- Keeps the recommendation bounded: approve retest, not direct migration.

## Page Logic Audit

Page 2

- Role: top-level answer for leadership.
- Approved visible viewpoint: `先评估，再承诺收益`; the local serving gate must validate cost/benefit before any commitment.
- Supported decision: approve architecture evaluation and local retest, not guaranteed adoption.

Page 4

- Role: help the reader judge workload match.
- Approved visible viewpoint: `先判定 workload 像不像`.
- Supported chapter claim: Aegaeon matters only if our multi-model serving has long-tail residency and bursty hot models.
- Boundary: do not move to benefits before workload similarity is tested.

Page 5

- Role: help the reader judge whether the mechanism is testable.
- Approved visible viewpoint: `机制可试，难点在切换`.
- Supported chapter claim: token boundary, prefill/decoding split, and TTFT/TBT scheduling are concrete; switching cost is the gating risk.
- Boundary: do not present token-level pooling as a scheduler-only change.

Page 6

- Role: help the reader judge whether evidence is enough for retest.
- Approved visible viewpoint: `证据够复测，不够承诺`.
- Supported chapter claim: SLO curves, arrival-rate/goodput claims, and beta deployment numbers justify priority.
- Boundary: 82% GPU saving belongs to Alibaba Cloud Model Studio and must not become our forecast.

Page 7

- Role: help the reader judge migration gates and next steps.
- Approved visible viewpoint: `过 gate，再谈适配`.
- Supported chapter claim: local workload, SLO, KV cache, engine lifecycle, model mix, switching cost, SLO violation, GPU utilization, and fallback cost must be measured before adaptation.
- Boundary: next action is bounded evaluation, not production rollout.

## Claim Evidence Implication Table

| Claim | Evidence | Implication |
| --- | --- | --- |
| The workload problem is production-relevant when long-tail models occupy GPU despite low request share. | Aegaeon Figure 1 and introduction: 94.1% of 779 models, 1.35% of 167.6M requests, 17.7% of 30K GPUs. | Page 4 should start with workload similarity, not mechanism
enthusiasm. |
| Request-level auto-scaling is bounded by active model count. | Aegaeon introduction and Figure 4: at total arrival rate 3.7 req/s, estimated active models = 46.55 out of 100. | Token-level preemption is worth considering only if our request duration also keeps models active for
long windows. |
| Aegaeon offers a concrete testable mechanism. | Figure 2 shows request-level vs token-level auto-scaling; text describes prefill grouped FCFS and decoding weighted round-robin; Figure 7/9/10 show switching and KV cache optimizations. | Page 5 should decompose the mechanism into
scheduler, SLO, and engineering gates. |
| Aegaeon has capacity evidence under SLO framing. | Abstract/conclusion report 2-2.5x higher request arrival rates or 1.5-9x more goodput; Figure 11/13 show SLO attainment curves. | Page 6 can justify retest priority with capacity/SLO evidence. |
| Aegaeon has production-related deployment evidence. | Abstract/evaluation/conclusion: beta deployed over three months in Alibaba Cloud Model Studio, serving tens of models from 1.8B to 72B, GPU count 1,192 to 213; Figure 18 shows utilization. | Page 6 can show strong production
signal. |
| Alibaba Cloud's 82% saving is not our guaranteed saving. | Deployment result is tied to Alibaba Cloud stack and workload; no source evidence validates our stack. | Page 6 and Page 7 must preserve non-extrapolation language. |
| Local adaptation depends on concrete serving gates. | Mechanism depends on TTFT/TBT definitions, KV cache movement/sync, engine lifecycle/reuse, model mix, and switching latency. | Page 7 should end with a retest plan and pass/fail gates. |

## Audit Appendix

Detailed evidence map, source usage policy, supplemental research, open questions, and approval log are kept in `research_audit_appendix.md`.
