---
date: 2026-06-03
fixture: tidar-hitl
source_package: TiDAR parser output
---

# TiDAR HITL Forward Test

This fixture preserves a parser-derived paper package for `TiDAR: Think in Diffusion, Talk in Autoregression`.

## Goal

Validate whether `ppt-deep-search` can run its normal human-in-the-loop workflow and produce two durable handoff files:

- `ppt_content_brief.md`, suitable as the downstream PPT maker's slide-content source;
- `research_audit.md`, preserving source grounding, approvals, boundaries, and evidence policy.

The test is not a one-shot paper summary. The child agent should ask the human stakeholder for missing audience, thesis, page-count, viewpoint, and constraint decisions according to `SKILL.md`. The main agent answers those questions as the human.

## Candidate-Facing Assets

Pass only this directory to the candidate agent:

- `candidate/prompt.md`
- `candidate/input/pdf_xml/final/tidar.xml`
- `candidate/input/pdf_xml/final/images/*.png`
- `candidate/input/pdf_xml/tidar.intermediate_parse_results.zip`
- `candidate/input/pdf_xml/tidar.pdf`

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
.tmp/forward-tests/tidar-hitl/<run-id>/
```

Expected artifacts:

- `ppt_content_brief.md`;
- `research_audit.md`;
- saved approval bundle or baselines when produced by the Skill;
- validation output showing the brief passed the repository QA script, or a clear blocker note explaining why it could not.
