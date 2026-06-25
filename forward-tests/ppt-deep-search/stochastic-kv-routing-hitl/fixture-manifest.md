---
date: 2026-06-02
fixture: stochastic-kv-routing-hitl
source_package: Stochastic KV Routing parser output
---

# Stochastic KV Routing HITL Forward Test

This fixture preserves a parser-derived paper package for `Stochastic KV Routing: Enabling Adaptive Depth-Wise Cache Sharing`.

## Goal

Validate whether `ppt-deep-search` can run its normal human-in-the-loop workflow and produce the required Source Understanding review artifacts plus one durable handoff file:

- `review/source_understanding_review.html`, screenshots, visual QA, and baseline approval for the pre-brief source-understanding gate.
- `ppt_content_brief.md`, suitable as the downstream PPT maker's slide-content source.

The test is not a one-shot paper summary. The child agent should ask the human stakeholder for missing audience, thesis, page-count, viewpoint, and constraint decisions according to `SKILL.md`. The main agent answers those questions as the human.

## Candidate-Facing Assets

Pass only this directory to the candidate agent:

- `candidate/prompt.md`
- `candidate/input/pdf_xml/final/stochastic-kv-routing.xml`
- `candidate/input/pdf_xml/final/images/*.png`
- `candidate/input/pdf_xml/source.json`
- `candidate/input/pdf_xml/stochastic-kv-routing.intermediate_parse_results.zip`

The candidate may also read the repository Skill and normal references/scripts required by `SKILL.md`, especially:

- `SKILL.md`
- `references/ppt-content-brief-format.md`
- `references/research-audit-format.md`
- `references/pyramid-principle.md`
- `scripts/validate_ppt_content_brief.py`

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
.tmp/forward-tests/stochastic-kv-routing-hitl/<run-id>/
```

Expected artifacts:

- `review/source_understanding_review.html`;
- `review/source-understanding-images/` with exported slide PNGs;
- `review/visual-qa.md` recording an independent checker verdict;
- saved source-understanding baseline under `baselines/`;
- `ppt_content_brief.md`;
- saved approval bundle or baselines when produced by the Skill;
- validation output showing `scripts/validate_source_understanding_html.py ... all ...` passed for the review HTML, or a clear blocker note explaining why it could not;
- validation output showing the brief passed the repository QA script, or a clear blocker note explaining why it could not.
