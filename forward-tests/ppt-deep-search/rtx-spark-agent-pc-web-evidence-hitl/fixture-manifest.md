---
date: 2026-06-04
fixture: rtx-spark-agent-pc-web-evidence-hitl
source_package: NVIDIA/Microsoft official web sources
---

# RTX Spark Agent PC Web Evidence HITL Forward Test

This fixture preserves a media-rich official-web-source task for `ppt-deep-search`.

## Goal

Validate whether `ppt-deep-search` can run its normal human-in-the-loop workflow on official web sources and produce two durable handoff files:

- `ppt_content_brief.md`, suitable as the downstream PPT maker's slide-content source;
- `research_audit.md`, preserving source grounding, approvals, boundaries, and evidence policy.

The test is not a one-shot web summary. The child agent should ask the human stakeholder for missing audience, thesis, page-count, viewpoint, and constraint decisions according to `SKILL.md`. During source understanding, it must use `web-article-capture` source packages rather than
raw HTML or search snippets.

## Candidate-Facing Assets

Pass only this directory to the candidate agent:

- `candidate/prompt.md`
- `candidate/input/source-request.md`

The candidate may also read the repository Skill and normal references/scripts required by `SKILL.md`.

## Judge-Facing Assets

Use after the candidate finishes:

- `judge/rubric.md`

Do not pass `judge/` to the candidate agent.

## Contamination Rules

- Do not pass `fixture-manifest.md`, `judge/`, or this case's `main-agent-prompt.md` to the child agent.
- Do not tell the child agent the desired scores, judge rubric, known failure mode, or expected source-package contents.
- Do not summarize a complete deck outline to the child agent before it asks for human decisions.
- The main agent may answer child-agent questions with stakeholder preferences and approvals.

## Expected Candidate Output Shape

The candidate should write final artifacts under a run-specific workspace such as:

```text
.tmp/forward-tests/rtx-spark-agent-pc-web-evidence-hitl/<run-id>/
```

Expected artifacts:

- `sources/source-discovery.md` or equivalent source-discovery record listing primary sources, adjacent-route sources, boundary/check sources, candidate visuals, and crawl plan;
- `review/source_understanding_review.html`;
- `review/report-data.json`;
- `sources/web/<source-slug>/` source packages with `source.md` and `images/` for media-rich sources;
- `ppt_content_brief.md`;
- `research_audit.md`;
- saved approval bundle or baselines when produced by the Skill;
- validation output showing the source package mapping, HTML review, and final brief passed repository QA scripts, or a clear blocker note explaining why source capture could not be completed.
