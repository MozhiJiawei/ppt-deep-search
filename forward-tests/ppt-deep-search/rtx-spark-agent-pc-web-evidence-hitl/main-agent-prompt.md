# Main Agent Prompt: Run RTX Spark Agent PC Web Evidence HITL Forward Test

Run the forward test at:

```text
forward-tests/ppt-deep-search/rtx-spark-agent-pc-web-evidence-hitl
```

Your job is to orchestrate the test and act as the human stakeholder. Do not solve the PPT deep-search task yourself.

## Files To Read First

Read these judge-side files before dispatch:

- `forward-tests/ppt-deep-search/rtx-spark-agent-pc-web-evidence-hitl/fixture-manifest.md`
- `forward-tests/ppt-deep-search/rtx-spark-agent-pc-web-evidence-hitl/judge/rubric.md`

Confirm the candidate-facing input exists:

- `forward-tests/ppt-deep-search/rtx-spark-agent-pc-web-evidence-hitl/candidate/prompt.md`
- `forward-tests/ppt-deep-search/rtx-spark-agent-pc-web-evidence-hitl/candidate/input/source-request.md`

## Candidate Dispatch

Start an interactive child-agent session. The child prompt must be this minimal shape only:

```text
请使用仓库 `SKILL.md` 完成 ppt-deep-search forward test：

- Candidate Prompt: forward-tests/ppt-deep-search/rtx-spark-agent-pc-web-evidence-hitl/candidate/prompt.md
- Candidate Input: forward-tests/ppt-deep-search/rtx-spark-agent-pc-web-evidence-hitl/candidate/input/
- Output: .tmp/forward-tests/rtx-spark-agent-pc-web-evidence-hitl/<run-id>/

你已经是 candidate child；不要再 spawn 子 agent。
```

Do not fork the full main-agent conversation into the child. The child prompt must not include judge-side context, previous run critiques, expected evidence-package failures, or the main agent's current theory about how to improve the Skill.

If subagents are unavailable in the current runtime, stop and report that this forward test requires a child-agent run to preserve validation integrity. Do not run the candidate task yourself in the same context.
Use a child-agent mechanism that can receive follow-up input from the main agent. Do not use a fire-and-forget worker mode for this case.

## Interactive Run Protocol

After dispatch, wait for the child agent's first substantive response.

- If it asks about audience, use, thesis, page count, viewpoint, page plan, or final constraints, answer as the stakeholder.
- If it requests approval, approve only when the proposal preserves the handoff contract; otherwise ask for a concrete adjustment.
- If it writes final `ppt_content_brief.md` or `research_audit.md` before any stakeholder answer, stop the child agent and record a HITL workflow failure.
- If the source-understanding HTML uses outline labels as body headings instead of claim-like section conclusions, request a revision before approval. Navigation labels may remain logical and fixed; body headings must be topic-specific claims.
- When the child provides `review/report-data.json` and `review/source_understanding_review.html`, run the evidence-package and HTML QA commands before approving Stage 1.5 when practical. For this media-rich case, the evidence-package QA must require downloaded original webpage images from `web-article-capture`, not rendered screenshots. Treat failures as revision requests or blockers.
- If rendered browser evidence capture or original webpage image download is genuinely unavailable to the child, it should stop and report a blocker before asking for source-understanding approval. Do not accept raw HTML, web search snippets, hand-written excerpts, or full-page screenshots as an equivalent substitute for article/main-region original image assets.
- If the runtime cannot send follow-up input to the child agent, stop before dispatch. This case is invalid without interactive child-agent control.
- Do not fix this by adding strategy, rubric, or approval instructions to `candidate/prompt.md`.

## Human Stakeholder Tendencies

When the child agent asks questions, answer as a realistic PPT requester:

- Target reader: technical architecture / AI engineering leaders evaluating whether RTX Spark represents a new local-agent PC platform category or mainly a marketing/spec update.
- Desired use: a pre-PPT content brief for an internal architecture evaluation deck.
- Page count: prefer 6 total PPT pages; cover and contents count if the child agent asks.
- Thesis direction: RTX Spark is best explained as a Windows local personal-agent stack anchor, not just a high-TOPS AI PC; however, the deck must keep official wording separate from Chinese media paraphrase.
- Evidence taste: prefer official NVIDIA/Microsoft source pages, original product/article images, exact spec numbers, runtime/security-stack descriptions, and explicit boundary notes before generic agentic-AI hype.
- Tone: decision-oriented Chinese, with English product/model/runtime/metric names preserved.

Approve stage outputs only when the child agent states enough to preserve the final handoff contract. Do not mention the judge rubric or expected scoring categories to the child agent.

## After Candidate Finishes

Collect the candidate's output directory and inspect:

- `review/report-data.json`;
- `review/source_understanding_review.html`;
- `sources/web/` evidence packages;
- `ppt_content_brief.md`;
- `research_audit.md`;
- any saved baselines or approval bundle;
- QA validation output, if present.

Use `forward-tests/ppt-deep-search/rtx-spark-agent-pc-web-evidence-hitl/judge/rubric.md` to judge the output.

Write judgment to:

```text
.tmp/forward-tests/rtx-spark-agent-pc-web-evidence-hitl/<run-id>/judgment.md
```
