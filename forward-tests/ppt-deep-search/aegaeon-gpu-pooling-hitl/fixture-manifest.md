---
date: 2026-06-03
fixture: aegaeon-gpu-pooling-hitl
source_package: Aegaeon parser output
---

# Aegaeon GPU Pooling HITL Forward Test

This fixture preserves a parser-derived paper package for `Aegaeon: Effective GPU Pooling for Concurrent LLM Serving on the Market`.

## Goal

Validate whether `ppt-deep-search` can run its normal human-in-the-loop workflow and produce one durable handoff file:

- `ppt_content_brief.md`, suitable as the downstream PPT maker's slide-content source.

The test is not a one-shot paper summary. The child agent should ask the human stakeholder for missing audience, thesis, page-count, viewpoint, and constraint decisions according to `SKILL.md`. The main agent answers those questions as the human.

## Candidate-Facing Assets

Pass only this directory to the candidate agent:

- `candidate/prompt.md`
- `candidate/input/pdf_xml/final/Aegaeon Effective GPU Pooling for Concurrent LLMServing on the Market.xml`
- `candidate/input/pdf_xml/final/images/*.png`
- `candidate/input/pdf_xml/Aegaeon Effective GPU Pooling for Concurrent LLMServing on the Market.intermediate_parse_results.zip`

The candidate may also read the repository Skill and normal references/scripts required by `SKILL.md`.

## Judge-Facing Assets

Use after the candidate finishes:

- `judge/rubric.md`

Do not pass `judge/` to the candidate agent.

## Contamination Rules

- Do not pass `fixture-manifest.md`, `judge/`, or this case's `main-agent-prompt.md` to the child agent.
- Do not tell the child agent the desired scores, judge rubric, or expected findings.
- Do not summarize a complete deck outline to the child agent before it asks for human decisions.
- The main agent may answer child-agent questions with stakeholder preferences and approvals.

## Expected Candidate Output Shape

The candidate should write final artifacts under a run-specific workspace such as:

```text
.tmp/forward-tests/aegaeon-gpu-pooling-hitl/<run-id>/
```

Expected artifacts:

- `ppt_content_brief.md`;
- saved approval bundle or baselines when produced by the Skill;
- validation output showing the brief passed the repository QA script, or a clear blocker note explaining why it could not.
