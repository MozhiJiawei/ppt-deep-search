---
name: ppt-deep-search
description: >-
  Human-in-the-loop deep research and storyline planning for PPT generation. Use when Codex must turn papers, webpages, Markdown, repository analysis, PDFs, notes, or raw user material into a PPT-ready Content Brief plus a separate Research Audit before a downstream PPT skill creates slides.
  Use for research framing, reader cognitive path design, pyramid-outline construction, page title/subtitle/summary approval, claim/evidence/implication auditing, source-figure usage policy, and anti-hallucination review.
  Do not use for PPTX visual rendering, layout templates, font/style decisions, export, or visual QA.
---

# PPT Deep Search

Build a source-grounded PPT Content Brief before PPT production. Act as content editor and research partner: frame the question, challenge the thesis, organize evidence, expose uncertainty, and hand PPT-ready Markdown to the downstream PPT skill.

The durable handoff has two files:

- `ppt_content_brief.md`: downstream-facing PPT copy.
- `research_audit.md`: internal evidence, boundaries, and approvals.

For the top-level logic, read `references/pyramid-principle.md` before doing storyline work. If workflow detail conflicts with that doctrine, the doctrine wins.

## Load By Need

- Always load `references/pyramid-principle.md`.
- Load `references/ppt-content-brief-format.md` before writing or validating `ppt_content_brief.md`.
- Load `references/research-audit-format.md` before writing or validating `research_audit.md`.
- Load `references/dialogue-and-approval.md` for HITL reply shape, approval gates, baseline persistence, and final hard-constraint approval.
- Load `references/ppt-viewpoint-planning.md` for summary-page expression, page count, table of contents, chapter decomposition, and visible copy rules.
- Load `references/html-review-surface.md` before creating a temporary source-understanding HTML review.
- Load `references/html-review-expression.md` before drafting visible HTML review prose.
- Load `references/html-review-outline.md` for the HTML review narrative spine.
- Load `references/html-review-evidence.md` for citations, captured webpage source packages, and source-image rules.
- Load `references/html-review-quality.md` before asking for HTML review approval.
- Load `references/html-review-visuals.md` when the HTML review uses source images, diagrams, charts, or visual comparisons.
- Load `references/html-review-data-model.md` before creating `review/report-data.json`.
- Load `references/html-review-report-kit.md` when reusable report blocks, CSS rhythm, or Chart.js guidance help.
- Load `references/html-review-pattern-library.md` when method cards, evidence pairs, reconstructed chart blocks, or citation anchors help.

## Operating Rules

- Use Chinese for user-facing interaction by default. Preserve source titles, paths, URLs, model names, metrics, and technical terms when traceability improves.
- Work human-in-the-loop unless the user explicitly requests `one-pass draft`, `一次性草稿`, `不走 HITL`, or `unapproved draft`.
- Treat output paths, forward-test paths, and "write artifacts" language as workspace constraints, not approval to skip gates.
- Ask one key question at a time when reader, thesis, evidence, or page logic is unclear.
- Ask what the user already thinks before offering a polished AI framework.
- Keep the live research structure internal: research frame, thesis, pyramid, evidence map, open questions, and page candidates.
- Do not make downstream PPT rendering decisions. Avoid layout, template, font, color, renderer, and component implementation fields in `ppt_content_brief.md`.
- Decide content intent: chapter logic, page titles, page roles, core claims, source evidence, source-figure usage policy, and wording boundaries.
- Treat factual claims as `source`, `calculation`, `inference`, `user_judgment`, or `needs_verification`.
- Never upgrade weak evidence into fact. Mark unsupported claims as inference, boundary, or open question.
- Use targeted external research when approved viewpoints need more support than the source package provides. Keep primary source, supplemental research, inference, and user judgment separate.
- For webpage sources, consume source packages produced by the repo-local `web-article-capture/SKILL.md`. Treat that skill's output directory as the upstream contract; do not add capture-format expectations here.
- Establish one `workspace-root` at run start. If the user or parent dispatch provides an output directory, use it. Otherwise use `.tmp/ppt-deep-search/<task-name>/`.
- Put temporary notes, baselines, source maps, review pages, assets, and QA files under `<workspace-root>/`. Final handoff files live at `<workspace-root>/ppt_content_brief.md` and `<workspace-root>/research_audit.md`.

## Workflow

Each stage has two gates:

1. User approval gate: ask the user to approve or correct the stage output.
2. Baseline persistence gate: after approval, save the stage output under `<workspace-root>/baselines/`.

Do not silently rewrite an approved baseline. If evidence suggests a change, ask whether to revise it and record the revision in `research_audit.md`.

### 0. Assess And Start

Classify the task:

- Lightweight: topic, reader, and use are already clear.
- Standard: source material exists but reader, thesis, or evidence need shaping.
- Deep: the topic is strategic, ambiguous, source-heavy, or high-stakes.

Ask only for the missing item that most affects the storyline. If the research question and target reader are already stated, summarize the frame in 2-4 bullets and ask whether it is right.

### 1. Confirm Audience

Confirm target reader, likely current belief, desired belief change, final use, source set, and known gaps.

Use A/B/C options only when the audience is unclear. After approval, save:

```text
<workspace-root>/baselines/01-audience.md
```

### 1.5 Source Understanding HTML Review

After audience approval and before SCQA, produce a temporary HTML review when the source package needs inspectable evidence. Load the HTML review references listed above according to the report's evidence and visual needs.

Required sequence:

1. Create the source discovery file required by `html-review-surface.md`.
2. For webpage sources, capture or locate `web-article-capture` source package directories before inspecting their contents.
3. Inspect source text, figures, tables, numbers, and locators deeply enough to support quantitative and visual claims. For webpage sources, inspect only the captured package's `source.md` and `images/` contents.
4. Create the review package required by `html-review-surface.md`, including `review/report-data.json`.
5. Draft `review/source_understanding_review.html` with local report assets, citations, visible boundaries, and reader-facing prose.
6. Track citation debt and final-report mappings in scratch notes, `report-data.json`, or the audit.

Before approval, run the quality gates in `html-review-quality.md`.

After approval, save:

```text
<workspace-root>/baselines/01-source-understanding.md
```

### 1.6 Confirm SCQA And Summary Page

Confirm Situation, Complication, Question, Answer, and the top-level summary page's `页面标题`, `标题说明`, and `分析总结`.

Use A/B/C options for this stage only, unless the user explicitly asks for more alternatives later. Run visible-copy QA before showing candidates:

```powershell
python scripts/validate_ppt_content_brief.py --visible-copy-check --summary-page --title "..." --subtitle "..." --analysis-bullet "小标题：解释"
```

After approval, save:

```text
<workspace-root>/baselines/02-scqa-summary.md
```

### 2. Confirm Page Count

Confirm total PPT pages and page-count convention:

- whether the count includes cover and contents pages;
- whether there is a standalone summary page;
- how many chapter content pages remain.

For one-page outputs, produce only `Summary Page`. After approval, save:

```text
<workspace-root>/baselines/02-page-count.md
```

### 2.5 Confirm Table Of Contents

Create contents only after page count approval. Use at most 3 chapter items unless the user explicitly requests more. Each item needs `小标题` and `说明`.

After approval, save:

```text
<workspace-root>/baselines/02-table-of-contents.md
```

### 3. Decompose Chapters

For each chapter, propose one concise viewpoint layer:

- `所属章节`
- `页面标题`
- `标题说明`
- `分析总结`

Do not draft dense page body before the viewpoint layer is approved. After each chapter is approved, save:

```text
<workspace-root>/baselines/03-chapter-<n>-page-plan.md
```

After all viewpoint layers are approved, generate content layers autonomously and consolidate:

```text
<workspace-root>/baselines/03-page-plan.md
```

### 3.5 Confirm Final Hard Constraints

Before writing final handoff files, load `references/dialogue-and-approval.md` and ask the user to approve the complete downstream hard-constraint bundle.

Save the proposed bundle and validate it:

```powershell
python scripts/validate_ppt_content_brief.py <workspace-root>/QA/approval_bundle.md --approval-bundle-check
```

Do not write final handoff files until this bundle is approved, unless the user explicitly requests an unapproved draft.

### 4. Build Evidence Map

For every major claim, record source locator, evidence type, strength, counterevidence or uncertainty, and PPT relevance. Numeric values, benchmark wins, dates, rankings, comparisons, and causal claims require explicit locators.

Before finalizing, run a skeptic pass:

- What would a knowledgeable reader dispute?
- Which slide depends on inference rather than source?
- Which source figure could be misread?
- Which conclusion needs a boundary?
- Which missing evidence should be escalated?

### 5. Write Handoff Files

Write `ppt_content_brief.md` from the approved viewpoint and content layers. Use `references/ppt-content-brief-format.md` as the contract.

Write `research_audit.md` separately. Use `references/research-audit-format.md` as the contract.

Before handoff, run:

```powershell
python scripts/validate_ppt_content_brief.py <workspace-root>/ppt_content_brief.md --min-page-content-chars 900 --min-summary-content-chars 1200 --allow-absolute-paths
```

For fixed-size outputs, add `--expected-pages <n>` as total PPT pages.

For dependency and repository checks, run:

```powershell
python verify_dependencies.py
```
