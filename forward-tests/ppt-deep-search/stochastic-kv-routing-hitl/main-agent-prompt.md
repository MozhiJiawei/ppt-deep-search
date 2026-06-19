# Main Agent Prompt: Run Stochastic KV Routing HITL Forward Test

Run the forward test at:

```text
forward-tests/ppt-deep-search/stochastic-kv-routing-hitl
```

Your job is to orchestrate the test and act as the human stakeholder. Do not solve the PPT deep-search task yourself.

## Files To Read First

Read these judge-side files before dispatch:

- `forward-tests/ppt-deep-search/stochastic-kv-routing-hitl/fixture-manifest.md`
- `forward-tests/ppt-deep-search/stochastic-kv-routing-hitl/judge/rubric.md`

Confirm the candidate-facing input exists:

- `forward-tests/ppt-deep-search/stochastic-kv-routing-hitl/candidate/prompt.md`
- `forward-tests/ppt-deep-search/stochastic-kv-routing-hitl/candidate/input/pdf_xml/final/stochastic-kv-routing.xml`
- `forward-tests/ppt-deep-search/stochastic-kv-routing-hitl/candidate/input/pdf_xml/final/images/`
- `forward-tests/ppt-deep-search/stochastic-kv-routing-hitl/candidate/input/pdf_xml/source.json`
- `forward-tests/ppt-deep-search/stochastic-kv-routing-hitl/candidate/input/pdf_xml/stochastic-kv-routing.intermediate_parse_results.zip`

## Candidate Dispatch

Start an interactive child-agent session with a prompt equivalent to:

```text
请使用仓库 `SKILL.md` 完成以下 ppt-deep-search forward test：

- Candidate Prompt: forward-tests/ppt-deep-search/stochastic-kv-routing-hitl/candidate/prompt.md
- Candidate Input: forward-tests/ppt-deep-search/stochastic-kv-routing-hitl/candidate/input/

请自行读取并遵循仓库 `SKILL.md` 的完整 human-in-the-loop 流程。

请将产物写入：

`.tmp/forward-tests/stochastic-kv-routing-hitl/<run-id>/`

`<run-id>` 必须是新的、未存在的目录，不能覆盖或复用历史 forward 结果。
```

Do not fork the full main-agent conversation into the child. The child prompt must not include judge-side context, previous run critiques, or the main agent's current theory about how to improve the Skill.

If subagents are unavailable in the current runtime, stop and report that this forward test requires a child-agent run to preserve validation integrity. Do not run the candidate task yourself in the same context.
Use a child-agent mechanism that can receive follow-up input from the main agent. Do not use a fire-and-forget worker mode for this case.

## Interactive Run Protocol

After dispatch, wait for the child agent's first substantive response.

- If it asks about audience, use, thesis, page count, viewpoint, page plan, or final constraints, answer as the stakeholder.
- If it requests intermediate approval, approve it and let the workflow continue.
- If it writes final `ppt_content_brief.md` before any stakeholder answer, stop the child agent and record a HITL workflow failure.
- If the runtime cannot send follow-up input to the child agent, stop before dispatch. This case is invalid without interactive child-agent control.
- Do not fix this by adding strategy, rubric, or approval instructions to `candidate/prompt.md`.

## Human Stakeholder Tendencies

When the child agent asks questions, answer as a realistic PPT requester:

- Target reader: technical product / infrastructure decision makers evaluating whether this paper's cache-sharing idea is worth a deeper serving experiment.
- Desired use: a pre-PPT content brief for an internal technical evaluation deck.
- Page count: prefer 6-7 total PPT pages; cover and contents count if the child agent asks.
- Thesis direction: depth-wise KV sharing looks strategically interesting because it attacks cache memory along a different axis than temporal eviction, but deployment value depends on training/fine-tuning cost, TTFT/throughput tradeoffs, and whether the retained-quality evidence
  transfers to the reader's serving environment.
- Evidence taste: prefer source figures and named metrics first; accept mechanism diagrams only when the paper figures are insufficient for the argument.
- Tone: decision-oriented Chinese, with English method/model/dataset names preserved.

Approve intermediate stage outputs so the candidate can finish. Do not mention the judge rubric or expected scoring categories to the child agent.

## After Candidate Finishes

Collect the candidate's output directory and inspect:

- `ppt_content_brief.md`;
- any saved baselines or approval bundle;
- QA validation output, if present.

Use `forward-tests/ppt-deep-search/stochastic-kv-routing-hitl/judge/rubric.md` to judge the output.

Write judgment to:

```text
.tmp/forward-tests/stochastic-kv-routing-hitl/<run-id>/judgment.md
```
