# Judge Rubric: TiDAR HITL Forward Test

Use this rubric after the candidate agent finishes. The judge may inspect the candidate's final handoff files, baselines, approval bundle, QA output, and interaction transcript.

## Scoring

Score each dimension from 0 to 3.

- HITL Workflow Discipline: asks for missing audience, thesis, page-count convention, summary-page viewpoint, page plan, and final constraints before writing final artifacts.
- Stakeholder Incorporation: uses the main agent's human answers to shape the final storyline without merely echoing them.
- Source Understanding: identifies TiDAR's free-token-slot motivation, diffusion drafting plus autoregressive sampling architecture, structured attention-mask design, training/evaluation setup, throughput-quality evidence, and limits versus speculative decoding and diffusion baselines with concrete source locators.
- HTML Review Surface: `review/source_understanding_review.html` is a Chinese-first, decision-grade source-understanding report with claim-like headings, useful visuals/source evidence, clickable citations, prior-art context, and explicit boundaries; it must not read like an internal audit dump or replace later SCQA/page-planning gates.
- Pyramid Storyline: turns the paper into a decision-oriented PPT argument rather than a section-by-section summary.
- Content Brief Contract: `ppt_content_brief.md` follows the required headings, field names, ordering, density, and downstream-facing language contract.
- Research Audit Contract: `research_audit.md` separates source evidence, inference, user judgment, approvals, visual opportunities, and open boundaries.
- Evidence Boundary Discipline: avoids overstating deployability or quality parity and preserves uncertainty around training cost, benchmark coverage, custom-kernel/system optimization needs, and output equivalence versus exact speculative decoding.
- QA Discipline: runs or clearly attempts `scripts/validate_ppt_content_brief.py` with suitable page-count and density settings, and treats failures as blockers.

## Blocking Findings

Treat any of the following as a likely fail:

- The candidate skips human-in-the-loop approval and writes final files immediately despite missing audience or page-count decisions.
- `review/source_understanding_review.html` is missing, fails HTML review validation when the validator is practical to run, has broken/non-clickable citation anchors, exposes internal labels as visible prose, or uses outline labels as body headings instead of topic-specific claims.
- `ppt_content_brief.md` is missing, fails required structural validation, or contains internal audit/source-locator tables that belong in `research_audit.md`.
- `research_audit.md` is missing or does not record approval history and evidence boundaries.
- The final storyline is a generic paper summary with no decision-oriented top-level thesis.
- Claims about AR-level quality, diffusion speed, exact KV support, tokens per second, or benchmark superiority are not traceable to paper evidence or explicitly marked as inference.
- The candidate reads judge-only files or receives rubric-derived coaching.
- The candidate writes outputs outside the required run directory without reporting the actual final paths.

## Judgment Template

```markdown
# Forward Test Judgment

## Verdict

[Strong pass / Pass with issues / Needs rerun / Fail]

## Scores

- HITL Workflow Discipline: [0-3]
- Stakeholder Incorporation: [0-3]
- Source Understanding: [0-3]
- HTML Review Surface: [0-3]
- Pyramid Storyline: [0-3]
- Content Brief Contract: [0-3]
- Research Audit Contract: [0-3]
- Evidence Boundary Discipline: [0-3]
- QA Discipline: [0-3]

## Blocking Findings

- [Finding or "None"]

## Notable Strengths

- [Strength]

## Improvement Targets

- [Target]

## Evidence Reviewed

- [Interaction transcript or summary]
- [HTML review path]
- [PPT Content Brief path]
- [Research Audit path]
- [Approval bundle or baseline path]
- [QA output path]
```
