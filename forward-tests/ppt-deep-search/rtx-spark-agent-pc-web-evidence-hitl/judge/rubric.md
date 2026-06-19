# Judge Rubric: RTX Spark Agent PC Web Evidence HITL Forward Test

Use this rubric after the candidate agent finishes. The judge may inspect the candidate's final handoff files, baselines, approval bundle, QA output, and interaction transcript.

## Scoring

Score each dimension from 0 to 3.

- HITL Workflow Discipline: asks for missing audience, thesis, page-count convention, summary-page viewpoint, page plan, and final constraints before writing final artifacts.
- Stakeholder Incorporation: uses the main agent's human answers to shape a technical-architecture storyline without merely echoing the source request.
- Official Wording Boundary: preserves that the official product/platform is NVIDIA RTX Spark / Windows PCs purpose-built for personal agents, and treats “Agent 原生电脑” or “老黄重新发明 PC” as Chinese/media paraphrase rather than a formal product name.
- Source Understanding: correctly synthesizes NVIDIA Newsroom, RTX Spark product page, GTC Taipei keynote context, NVIDIA Build/local-agents blog, and Microsoft Build Live into an architecture judgment about Windows local personal/frontier agents, RTX Spark, DGX Station,
  OpenShell, security runtime, CUDA/WSL, unified memory, and local large-model constraints.
- Pyramid Storyline: turns the official web sources into a decision-oriented PPT argument rather than a list of source facts or URLs.
- Content Brief Contract: `ppt_content_brief.md` follows the required headings, field names, ordering, density, and downstream-facing language contract.
- Evidence Boundary Discipline: avoids treating theoretical FP4/sparsity peak performance, not-yet-shipped products, keynote rhetoric, or official marketing copy as validated production agent throughput/security evidence.
- QA Discipline: runs or clearly attempts `scripts/validate_ppt_content_brief.py` with suitable flags, and treats failures as blockers.

## Blocking Findings

Treat any of the following as a likely fail:

- The candidate skips human-in-the-loop approval and writes final files immediately despite missing audience or page-count decisions.
- `ppt_content_brief.md` is missing, fails required structural validation, or contains author-facing audit/source-locator tables.
- The final storyline says or implies that “全球首个 Agent 原生电脑” is an official product name.
- Claims about 1 PFLOP, 128GB unified memory, 120B-parameter local models, 1M token context, OpenShell, or DGX Station are not traceable to official sources or are not clearly bounded.
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
- Official Wording Boundary: [0-3]
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
