# Judge Rubric: RTX Spark Agent PC Web Evidence HITL Forward Test

Use this rubric after the candidate agent finishes. The judge may inspect the candidate's final handoff files, source packages, baselines, approval bundle, QA output, and interaction transcript.

## Scoring

Score each dimension from 0 to 3.

- HITL Workflow Discipline: asks for missing audience, thesis, page-count convention, summary-page viewpoint, page plan, and final constraints before writing final artifacts.
- Stakeholder Incorporation: uses the main agent's human answers to shape a technical-architecture storyline without merely echoing the source request.
- Official Wording Boundary: preserves that the official product/platform is NVIDIA RTX Spark / Windows PCs purpose-built for personal agents, and treats “Agent 原生电脑” or “老黄重新发明 PC” as Chinese/media paraphrase rather than a formal product name.
- Source Discovery: before drafting the HTML review, identifies primary sources, adjacent-route sources, boundary/check sources, candidate visuals, and a crawl plan; comparison objects should be chosen because they answer a real reader question, not because they are easy to
  mention.
- Web Source Package: for every cited official webpage, creates a `web-article-capture` source package under `sources/web/<source-slug>/`.
  Each package has `source.md` and `images/`; media-rich pages should include downloaded original webpage images unless `source.md` explains why the article/main region has no useful images.
- HTML Review Surface: `review/source_understanding_review.html` is a Chinese-first, decision-grade source-understanding report with claim-like headings, useful source images or evidence visuals, clickable citations, comparison context, and explicit boundaries; it
  must not read like an internal audit dump or replace later SCQA/page-planning gates.
- Data-Smart Technical Report: the HTML review uses original images, numbers, specs, timelines, comparison matrices, reconstructed charts, decision registers, or compact tables to make the RTX Spark technical judgment auditable; it should not rely on
  prose-only method cards when the source package contains technical metrics and visual evidence.
- Source Understanding: correctly synthesizes NVIDIA Newsroom, RTX Spark product page, GTC Taipei keynote context, NVIDIA Build/local-agents blog, and Microsoft Build Live into an architecture judgment about Windows local personal/frontier agents, RTX Spark, DGX Station,
  OpenShell, security runtime, CUDA/WSL, unified memory, and local large-model constraints.
- Pyramid Storyline: turns the web-source package into a decision-oriented PPT argument rather than a list of source facts or URLs.
- Content Brief Contract: `ppt_content_brief.md` follows the required headings, field names, ordering, density, and downstream-facing language contract.
- Research Audit Contract: `research_audit.md` separates source evidence, inference, user judgment, approvals, visual opportunities, source package paths, and open boundaries.
- Evidence Boundary Discipline: avoids treating theoretical FP4/sparsity peak performance, not-yet-shipped products, keynote rhetoric, or official marketing copy as validated production agent throughput/security evidence.
- QA Discipline: runs or clearly attempts `scripts/validate_web_evidence_package.py`, `scripts/validate_html_review_data.py`, `scripts/validate_html_review.py`, and `scripts/validate_ppt_content_brief.py` with suitable flags, and treats failures as blockers.

## Blocking Findings

Treat any of the following as a likely fail:

- The candidate skips human-in-the-loop approval and writes final files immediately despite missing audience or page-count decisions.
- The candidate cites webpages using only URLs, raw HTML, web search snippets, or hand-written excerpts while claiming to have captured source packages.
- The comparison section appears before any source-discovery record or crawl plan, or adjacent routes are asserted from general knowledge with no source acquisition path.
- When a useful comparison or boundary claim lacks support, the candidate deletes it to pass QA instead of fetching a source, weakening it into an open question, or recording the gap.
- `review/report-data.json` would fail `python scripts/validate_web_evidence_package.py <json> --require-images always --min-image-sources 1` for this media-rich source package, unless the candidate explicitly stopped and reported source capture as blocked
  before asking for source-understanding approval.
- Source packages contain no downloaded original webpage images for all media-rich official pages without a credible no-useful-image explanation.
- `review/source_understanding_review.html` is missing, fails HTML review validation when practical to run, has broken/non-clickable citation anchors, exposes internal labels as visible prose, or uses outline labels as body headings instead of topic-specific claims.
- The HTML review is technically plausible but mostly prose, with no meaningful source-image usage, chart/table/matrix/decision-register treatment, or numeric/spec extraction despite the RTX Spark sources containing visual and quantitative material.
- The HTML review includes remote webpage image hotlinks instead of local `review/assets/` files for displayed webpage images.
- `ppt_content_brief.md` is missing, fails required structural validation, or contains internal audit/source-locator tables that belong in `research_audit.md`.
- `research_audit.md` is missing or does not record approval history, source package paths, and evidence boundaries.
- The final storyline says or implies that “全球首个 Agent 原生电脑” is an official product name.
- Claims about 1 PFLOP, 128GB unified memory, 120B-parameter local models, 1M token context, OpenShell, or DGX Station are not traceable to official sources or are not clearly bounded.
- The candidate reads judge-only files or receives rubric-derived coaching.
- The candidate writes outputs outside the required run directory without reporting the actual final paths.

## Main-Agent QA Suggestions

Before approving source understanding, run when practical:

```powershell
python scripts/validate_web_evidence_package.py <run-output>/review/report-data.json --require-images always --min-image-sources 1
python scripts/validate_html_review_data.py <run-output>/review/report-data.json
python scripts/validate_html_review.py <run-output>/review/source_understanding_review.html
```

After final handoff, run the appropriate content-brief validator with expected page count if the child's page count is approved.

## Judgment Template

```markdown
# Forward Test Judgment

## Verdict

[Strong pass / Pass with issues / Needs rerun / Fail]

## Scores

- HITL Workflow Discipline: [0-3]
- Stakeholder Incorporation: [0-3]
- Official Wording Boundary: [0-3]
- Source Discovery: [0-3]
- Web Source Package: [0-3]
- HTML Review Surface: [0-3]
- Data-Smart Technical Report: [0-3]
- Source Understanding: [0-3]
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
- [Web source package paths]
- [Source discovery / crawl plan path]
- [HTML review path]
- [PPT Content Brief path]
- [Research Audit path]
- [Approval bundle or baseline path]
- [QA output path]
```
