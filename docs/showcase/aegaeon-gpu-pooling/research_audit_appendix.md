# Research Audit Appendix

Continuation of `research_audit.md` for the Aegaeon GPU pooling showcase.

## Evidence Map

| Evidence item | Source locator | Type | Strength | Boundary / uncertainty | PPT relevance |
| --- | --- | --- | --- | --- | --- |
| 94.1% of 779 models contribute 1.35% of 167.6M requests but use 17.7% of 30K GPUs. | Primary XML introduction; Figure 1; `picture_002.png`. | source | strong | Alibaba Cloud Model Studio workload; our distribution unknown. | Must use as source figure or rebuilt statistic. |
| Hot 270B top model has burst above reserved line. | Figure 1(b); `picture_002.png`. | source | strong | Specific model / cluster sample; burst pattern may differ locally. | Use to show long-tail plus burst, not just cold models. |
| 46.55 active models out of 100 at total arrival rate 3.7 req/s. | Primary XML introduction; Figure 4; appendix active model analysis; `picture_005.png`. | source/calculation from paper | medium-strong | Depends on Poisson/request-duration assumptions. | Use as body support, not
necessarily a headline. |
| Token-level auto-scaling can preempt active model between tokens. | Figure 2; primary XML Aegaeon overview. | source | strong | Diagrammatic mechanism; implementation cost must be tested. | Must use or summarize on Page 5. |
| Prefill and decoding scheduled separately around TTFT and TBT. | Primary XML Aegaeon overview / token-level scheduling. | source | strong | Local SLO definitions may differ. | Use on Page 5 and Page 7. |
| Autoscaling overhead reduced by 97%. | Primary XML abstract/contribution text; Figure 7/9/10 support optimization path. | source | medium | Summary number needs local decomposition; not enough alone for migration. | Use as engineering signal with caveat. |
| 2-2.5x higher request arrival rates or 1.5-9x goodput. | Primary XML abstract/evaluation/conclusion. | source | strong for paper claim | Controlled setup; local stack unknown. | Use on Page 6. |
| SLO attainment curves under ShareGPT and model-count/RPS variation. | Figure 11 / Figure 13; `picture_013.png`, `picture_012.png`. | source | strong | Benchmark/workload-specific. | Use at least one on Page 6. |
| Beta deployment over three months, tens of models, 1.8B-72B parameters, 1,192 to 213 GPUs. | Primary XML evaluation and abstract/conclusion. | source | strong for Alibaba Cloud | Does not prove our benefit. | Use on Page 6 with explicit non-extrapolation. |
| Figure 18 deployment utilization over 70 hours. | Figure 18; `picture_017.png`. | source | medium-strong | Utilization graph does not alone prove SLO preservation. | Use as production signal. |
| vLLM/PagedAttention is memory-management oriented and reports 2-4x throughput. | arXiv:2309.06180. | supplemental | medium | Adjacent context only. | Use only in source review/audit, not necessary in final PPT body. |
| MuxServe reports up to 1.8x throughput or 2.9x more requests within 99% SLO. | PMLR ICML 2024 page. | supplemental | medium | Adjacent baseline/context; not the deck's proof. | Use only as background if needed. |
| DistServe separates prefill/decoding and reports 7.4x more requests or 12.6x tighter SLO. | arXiv:2401.09670. | supplemental | medium | Adjacent phase-disaggregation context. | Use only as background if needed. |
| HydraServe reduces cold-start latency and improves SLO attainment. | arXiv:2502.15524. | supplemental | medium | Serverless cold-start context; not direct token-level pooling proof. | Use only as comparison context. |

## Source Usage Policy

Figures/tables:

- Figure 1 / `picture_002.png`: must use or summarize/rebuild. It is the strongest source figure for workload fit.
- Figure 2 / `picture_003.png`: must use or summarize. It explains the request-level versus token-level decision shift.
- Figure 4 / `picture_005.png`: may use as supporting evidence for active-model bottleneck.
- Figure 7 / `picture_008.png`: may use for switching-cost and engine lifecycle discussion.
- Figure 9 / `picture_010.png`: may use for explicit memory management and unified KV cache.
- Figure 10 / `picture_011.png`: may use for fine-grained KV cache synchronization.
- Figure 11 / `picture_013.png`: should use for SLO/capacity evidence if space permits.
- Figure 13 / `picture_012.png`: should use for SLO attainment under model-count / arrival-rate variation if space permits.
- Figure 18 / `picture_017.png`: should use or summarize for deployment signal.
- Figure 5 system overview: background only. Avoid making it a central visual because the user requested less generic system diagram usage.

Numeric claims:

- Production workload numbers can be used as source-backed facts for Alibaba Cloud Model Studio.
- 82% GPU saving can be used only as Alibaba Cloud beta deployment result.
- Any local expected saving must be omitted or marked as a future forecast requiring local validation.

## Supplemental Research

Supplemental sources used to position adjacent serving approaches:

- vLLM / PagedAttention: `https://arxiv.org/abs/2309.06180`. Used to distinguish KV memory management from token-level multi-model scale decisions.
- MuxServe: `https://proceedings.mlr.press/v235/duan24a.html`. Used to compare spatial-temporal multiplexing and multi-model colocation.
- DistServe: `https://arxiv.org/abs/2401.09670`. Used to contextualize prefill/decoding disaggregation and TTFT/TPOT framing.
- HydraServe: `https://arxiv.org/abs/2502.15524`. Used to contextualize serverless LLM cold-start acceleration and scale-up latency.

These sources are not primary evidence for the Aegaeon claims. They support the source-understanding comparison section and help avoid mispositioning Aegaeon as a replacement for all serving optimizations.

## Assumptions and Open Questions

Assumptions:

- The target team has a multi-model LLM serving environment where workload skew and burstiness may matter.
- The downstream PPT will be used for leadership architecture evaluation, not a paper reading group.
- The reader needs a bounded decision path: evaluate, retest, then consider adaptation.

Open questions for local evaluation:

- Does our model market have a comparable long-tail distribution?
- Do our top models have burst patterns that create reserved-capacity waste?
- What are our exact TTFT, TBT/TPOT, end-to-end latency, and SLO violation definitions?
- Can our runtime support safe token-boundary preemption?
- What is the measured KV cache movement/sync cost in our engine?
- Which engine lifecycle components can be reused or cached?
- What is our model switching latency budget relative to TBT?
- What fallback policy protects SLO if preemption or switching fails?
- What goodput/arrival-rate capacity improvement is meaningful enough to justify implementation work?

Claims that should be softened:

- Any statement implying the 82% GPU saving transfers to our stack.
- Any statement implying token-level pooling is superior for all multi-model serving.
- Any statement implying implementation is only a scheduler change.

## Approval Log

1. User selected audience option 1 with refinement: technical product / infrastructure leadership evaluating token-level GPU pooling adaptation. Baseline saved at `baselines/01-audience.md`.
2. Source-understanding HTML approved as basis for SCQA and storyline. User emphasized the Alibaba Cloud beta deployment boundary. Baseline saved at `baselines/01-source-understanding.md`.
3. User selected top-level summary option B: `先评估，再承诺收益`. Baseline saved at `baselines/01-audience-thesis.md`.
4. User selected 7 total pages including cover, summary, and contents. Baseline saved at `baselines/02-page-count.md`.
5. User approved table of contents order and four titles. Baseline saved at `baselines/02-table-of-contents.md`.
6. User approved Page 4 viewpoint layer. Baseline saved at `baselines/03-chapter-1-page-plan.md`.
7. User approved Page 5 viewpoint layer. Baseline saved at `baselines/03-chapter-2-page-plan.md`.
8. User approved Page 6 viewpoint layer. Baseline saved at `baselines/03-chapter-3-page-plan.md`.
9. User approved Page 7 viewpoint layer. Baseline saved at `baselines/03-chapter-4-page-plan.md`.
10. Consolidated page plan with content layer saved at `baselines/03-page-plan.md`.
11. Final approval bundle saved at `QA/approval_bundle.md` and passed `--approval-bundle-check`.
12. User approved final hard constraints and requested handoff writing plus PPT content brief QA.
