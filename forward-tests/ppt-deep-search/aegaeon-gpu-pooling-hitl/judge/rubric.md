# Judge Rubric: Aegaeon GPU Pooling HITL Forward Test

Use this rubric after the candidate agent finishes. The judge may inspect the candidate's final handoff files, baselines, approval bundle, QA output, and interaction transcript.

## Scoring

Score each dimension from 0 to 3.

- HITL Workflow Discipline: asks for missing audience, thesis, page-count convention, summary-page viewpoint, page plan, and final constraints before writing final artifacts.
- Stakeholder Incorporation: uses the main agent's human answers to shape the final storyline without merely echoing them.
- Source Understanding: identifies Aegaeon's model-market workload motivation, token-level auto-scaling idea, prefill/decoding scheduling split, auto-scaling cost optimizations, beta deployment evidence, and transfer limits with concrete source locators.
- Pyramid Storyline: turns the paper into a decision-oriented PPT argument rather than a section-by-section summary.
- Content Brief Contract: `ppt_content_brief.md` follows the required headings, field names, ordering, density, and downstream-facing language contract.
- Evidence Boundary Discipline: avoids overstating portability of Alibaba Cloud beta-deployment results and preserves uncertainty around workload mix, SLO definitions, infrastructure assumptions, and engineering integration cost.
- QA Discipline: runs or clearly attempts `scripts/validate_ppt_content_brief.py` with suitable page-count and density settings, and treats failures as blockers.

## Blocking Findings

Treat any of the following as a likely fail:

- The candidate skips human-in-the-loop approval and writes final files immediately despite missing audience or page-count decisions.
- `ppt_content_brief.md` is missing, fails required structural validation, or contains author-facing audit/source-locator tables.
- The final storyline is a generic paper summary with no decision-oriented top-level thesis.
- Claims about GPU savings, SLO preservation, goodput, arrival-rate capacity, or production readiness are not traceable to paper evidence or explicitly marked as inference.
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
- Pyramid Storyline: [0-3]
- Content Brief Contract: [0-3]
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
- [PPT Content Brief path]
- [Approval bundle or baseline path]
- [QA output path]
```
