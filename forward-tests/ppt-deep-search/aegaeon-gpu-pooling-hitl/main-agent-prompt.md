# Main Agent Prompt: Run Aegaeon GPU Pooling HITL Forward Test

Run the forward test at:

```text
forward-tests/ppt-deep-search/aegaeon-gpu-pooling-hitl
```

Your job is to orchestrate the test and act as the human stakeholder. Do not solve the PPT deep-search task yourself.

## Files To Read First

Read these judge-side files before dispatch:

- `forward-tests/ppt-deep-search/aegaeon-gpu-pooling-hitl/fixture-manifest.md`
- `forward-tests/ppt-deep-search/aegaeon-gpu-pooling-hitl/judge/rubric.md`

Confirm the candidate-facing input exists:

- `forward-tests/ppt-deep-search/aegaeon-gpu-pooling-hitl/candidate/prompt.md`
- `forward-tests/ppt-deep-search/aegaeon-gpu-pooling-hitl/candidate/input/pdf_xml/final/Aegaeon Effective GPU Pooling for Concurrent LLMServing on the Market.xml`
- `forward-tests/ppt-deep-search/aegaeon-gpu-pooling-hitl/candidate/input/pdf_xml/final/images/`
- `forward-tests/ppt-deep-search/aegaeon-gpu-pooling-hitl/candidate/input/pdf_xml/Aegaeon Effective GPU Pooling for Concurrent LLMServing on the Market.intermediate_parse_results.zip`

## Candidate Dispatch

Start an interactive child-agent session with a prompt equivalent to:

```text
请使用仓库 `SKILL.md` 完成以下 ppt-deep-search forward test：

- Candidate Prompt: forward-tests/ppt-deep-search/aegaeon-gpu-pooling-hitl/candidate/prompt.md
- Candidate Input: forward-tests/ppt-deep-search/aegaeon-gpu-pooling-hitl/candidate/input/

请自行读取并遵循仓库 `SKILL.md` 的完整 human-in-the-loop 流程。

请将产物写入：

`.tmp/forward-tests/aegaeon-gpu-pooling-hitl/<run-id>/`

`<run-id>` 必须是新的、未存在的目录，不能覆盖或复用历史 forward 结果。
```

Do not fork the full main-agent conversation into the child. The child prompt must not include judge-side context, previous run critiques, or the main agent's current theory about how to improve the Skill.

If subagents are unavailable in the current runtime, stop and report that this forward test requires a child-agent run to preserve validation integrity. Do not run the candidate task yourself in the same context.
Use a child-agent mechanism that can receive follow-up input from the main agent. Do not use a fire-and-forget worker mode for this case.

## Interactive Run Protocol

After dispatch, wait for the child agent's first substantive response.

- If it asks about audience, use, thesis, page count, viewpoint, page plan, or final constraints, answer as the stakeholder.
- If it requests approval, approve only when the proposal preserves the handoff contract; otherwise ask for a concrete adjustment.
- If it writes final `ppt_content_brief.md` or `research_audit.md` before any stakeholder answer, stop the child agent and record a HITL workflow failure.
- If the source-understanding HTML uses outline labels as body headings instead of claim-like section conclusions, request a revision before approval. Navigation labels may remain logical and fixed; body headings must be topic-specific claims.
- When the child provides `review/source_understanding_review.html`, also inspect
  `review/report-data.json`, then run `python scripts/validate_html_review_data.py <report-data.json>`
  and `python scripts/validate_html_review.py <html>` before approving Stage 1.5 when practical.
  If either fails, request a revision. Do not force a specific visual component pattern
  if the report communicates the evidence well.
- If the runtime cannot send follow-up input to the child agent, stop before dispatch. This case is invalid without interactive child-agent control.
- Do not fix this by adding strategy, rubric, or approval instructions to `candidate/prompt.md`.

## Human Stakeholder Tendencies

When the child agent asks questions, answer as a realistic PPT requester:

- Target reader: technical product / infrastructure leaders evaluating whether token-level GPU pooling is worth adapting for multi-model LLM serving.
- Desired use: a pre-PPT content brief for an internal serving architecture evaluation deck.
- Page count: prefer 6-7 total PPT pages; cover and contents count if the child agent asks.
- Thesis direction: Aegaeon looks production-relevant because it attacks long-tail model-market waste with token-level auto-scaling, but the deck must separate beta-deployment evidence from transfer assumptions about another serving stack.
- Evidence taste: prefer production workload statistics, SLO/TTFT/TBT framing, GPU saving numbers, goodput comparisons, and source figures before generic system diagrams.
- Tone: decision-oriented Chinese, with English system/model/metric names preserved.

Approve stage outputs only when the child agent states enough to preserve the final handoff contract. Do not mention the judge rubric or expected scoring categories to the child agent.

## After Candidate Finishes

Collect the candidate's output directory and inspect:

- `ppt_content_brief.md`;
- `research_audit.md`;
- any saved baselines or approval bundle;
- QA validation output, if present.

Use `forward-tests/ppt-deep-search/aegaeon-gpu-pooling-hitl/judge/rubric.md` to judge the output.

Write judgment to:

```text
.tmp/forward-tests/aegaeon-gpu-pooling-hitl/<run-id>/judgment.md
```
