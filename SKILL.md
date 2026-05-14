---
name: ppt-deep-search
description: Human-in-the-loop deep research and storyline planning for PPT generation. Use when Codex must turn papers, webpages, Markdown, repository analysis, PDFs, notes, or raw user material into a PPT-ready Content Brief plus a separate Research Audit before a downstream PPT skill creates slides. Use for research framing, reader cognitive path design, pyramid-outline construction, page title/subtitle/summary approval, claim/evidence/implication auditing, source-figure usage policy, and anti-hallucination review. Do not use for PPTX visual rendering, layout templates, font/style decisions, export, or visual QA.
---

# PPT Deep Search

Build a source-grounded PPT Content Brief before PPT production. Act as content editor and research partner: frame the question, challenge the thesis, organize evidence, expose uncertainty, and hand PPT-ready structured Markdown to the downstream PPT skill.

This skill is modeled as a research dialogue, not a one-shot summarizer. The durable handoff has two files: `ppt_content_brief.md` for downstream PPT generation, and `research_audit.md` for internal evidence, boundaries, and approvals.

Before doing any storyline work, read `references/pyramid-principle.md` and follow it as the highest-level doctrine. If any workflow detail conflicts with that doctrine, the doctrine wins.

For the downstream file contract and QA-checked fields, see `references/ppt-content-brief-format.md`. Load `references/research-audit-format.md` when writing or validating the internal audit file.

## Operating Rules

- Use Chinese for all user-facing interaction by default, including questions, options, stage summaries, approval prompts, and final handoff notes. Keep source titles, figure/table labels, code paths, URLs, model names, metrics, and technical terms in their original language when that improves traceability.
- Work human-in-the-loop by default. Do not skip straight to the final PPT Content Brief unless the user explicitly asks for a one-pass draft or the research frame is already fully specified.
- Ask one key question at a time when research direction, target reader, thesis strength, or evidence boundary is unclear. One turn should resolve one decision.
- Ask what the user is already thinking before offering a polished AI framework. Use the user's judgment as a first-class input, not as an afterthought.
- Prefer single-select options at major forks, with a free-form escape hatch. Use open prose questions only when options would bias the answer or the user needs to explain context.
- Keep a live research structure after each round: research frame, thesis, pyramid outline, evidence map, open questions, and page candidates. Keep this internal structure out of the final PPT content file.
- Do not make visual-rendering decisions. Avoid fields such as `visual_anchor.kind`, `template`, `contentLayout`, renderer names, column layout, font size, color, card structure, and visual-anchor implementation details.
- Do decide content intent: chapter logic, page titles, page roles, core claims, source evidence, source-figure usage policy, and wording boundaries. Put role/evidence/boundary audit details in `research_audit.md`, not in `ppt_content_brief.md`.
- Treat every factual claim as one of: `source`, `calculation`, `inference`, `user_judgment`, or `needs_verification`.
- Never upgrade weak evidence into a fact. If a claim lacks source support, label it as inference or open question.
- If the approved viewpoint needs more support than the provided source material contains, use external research such as web search, official docs, papers, repository docs, or reputable technical articles to gather more context. Mark those materials as supplemental evidence and explain how they support, qualify, or challenge the approved viewpoint.
- Do not let external research replace the approved viewpoint or blur source boundaries. Separate `primary source`, `supplemental research`, `inference`, and `user_judgment` in the evidence map.
- Absolute local source paths are acceptable in `research_audit.md` because this workflow runs on the same machine. Do not put local absolute paths in `ppt_content_brief.md`; use source names there and keep exact locators in the audit file.
- Put all temporary notes, drafts, extracted inventories, and QA outputs under the host workspace `.tmp/ppt-deep-search/<task-name>/`. The only final handoff files are `ppt_content_brief.md` and `research_audit.md`.

## Workflow

Follow the pyramid principle doctrine in `references/pyramid-principle.md`: confirm the audience first, analyze the source material in plain language, resolve SCQA and the top-level summary page, confirm page count, create concise table-of-contents entries, then decompose one chapter at a time. Do not generate a table of contents before page count is approved, and do not decompose pages before the table of contents is approved.

Each stage has two gates:

1. User approval gate: ask the user to approve or correct the stage output.
2. Baseline persistence gate: after approval, save that stage output under `.tmp/ppt-deep-search/<task-name>/baselines/` and treat it as the baseline for later stages.

Do not silently rewrite an approved baseline. If later evidence suggests a change, ask whether to revise the baseline and record the revision in `Approval Log`.

After saving any approved baseline, tell the user the baseline path in one short sentence. If the user chooses a previous option after several challenge rounds, preserve that history in the baseline and record which historical option was selected.

### 0. Assess and Start the Dialogue

Classify the task before producing structure:

- **Lightweight**: the user already has a topic, reader, and expected deck use. Ask at most one clarifying question, then draft a compact PPT Content Brief plus Research Audit.
- **Standard**: the user has source material and a PPT goal, but reader, thesis, or evidence boundaries need shaping. Run the full dialogue.
- **Deep**: the topic is strategic, ambiguous, source-heavy, or likely to change a reader's high-stakes judgment. Spend more time on assumptions, counterevidence, and boundaries before page candidates.

Opening move:

- If the user has not stated the research question or target reader, ask only for the missing item that most affects the storyline.
- If the user has stated both, summarize the current frame in 2-4 bullets and ask whether the frame is right before expanding.
- If the user provided a strong opinion, reflect it back and ask what would count as convincing evidence.

Do not ask the user to fill a long form. Turn form-like fields into a short sequence of decisions.

### 0.5 Keep Replies Readable

Human-in-the-loop work should feel like a clear research conversation, not a dumped analysis log.

Use this shape for normal turns:

```text
我现在的判断：
- ...
- ...

需要你拍板的一件事：
...
```

Keep each turn short:

- Use 2-4 bullets for the current read.
- Ask exactly one question.
- Avoid long evidence inventories in chat; save detailed maps for the brief.
- When offering choices, use 2-3 options with short labels and one-line tradeoffs.
- Do not paste the full live structure unless the user asks to review it.

Use A/B/C options only for audience selection and the top-level summary page expression. Do not force A/B/C for chapter planning or page planning; guide with a concise proposal, then let the user ask for changes.

For the top-level summary page expression, present 2-3 concrete candidate expressions in this shape:

```text
【A】
表达的观点：...
标题：...
分析总结：
1. 标签：...
2. 标签：...
3. 标签：...

【B】
表达的观点：...
标题：...
分析总结：
1. 标签：...
2. 标签：...
3. 标签：...
```

The user should be choosing between PPT-ready top-level summary expressions, not abstract themes. When discussing chapters or content pages, do not force options. Give your best proposal and ask the user what to adjust.

### 1. Confirm Audience

Confirm or infer only what is reasonably clear:

- Target reader
- Reader's likely current belief
- Desired belief change
- Final use: PPT, decision, learning, proposal, external material, or other
- Source set and known gaps

Use A/B/C options for audience selection when the audience is not already clear. Audience options should include target reader, current belief, desired belief change, and final use.

Stage 1 required approval: target audience, reader's current belief, desired belief change, final use, and source set.

After approval, save:

```text
.tmp/ppt-deep-search/<task-name>/baselines/01-audience.md
```

### 1.5 Source Understanding Analysis

After the audience is approved and before discussing the top-level summary page, output a concise source-understanding analysis in Chinese. This is not a final brief; it gives the human a basis for judgment and follow-up questions.

Include exactly these three parts:

- `它是什么`：the object/system/paper/tool in plain language.
- `它解决了什么问题`：the concrete pain or decision problem it addresses.
- `跟同类技术比有什么亮点`：why it differs from adjacent approaches or existing solutions.

Keep the first version source-grounded and compact: 3-6 bullets total. If the user challenges the analysis or asks for deeper comparison, expand only the challenged part and preserve the revised version in the baseline. Then ask the user whether this understanding is basically right or what needs correction.

After approval, save:

```text
.tmp/ppt-deep-search/<task-name>/baselines/01-source-understanding.md
```

### 1.6 Confirm SCQA and Top-Level Summary Page

Confirm:

- Situation, complication, governing question, and answer
- The top-level summary page expression: page title, title subtitle, and analysis-summary bullets

Use A/B/C options for this top-level summary page expression. Do not use A/B/C after this stage unless the user explicitly asks for alternatives.

Stage 1.6 required approval: SCQA and top-level summary page.

After approval, save:

```text
.tmp/ppt-deep-search/<task-name>/baselines/01-audience-thesis.md
```

This file becomes the baseline for all later page-count, chapter, and page-title decisions.

The approved top-level summary page must become its own page in the final page plan. Do not merge it into a later evidence or mechanism page.

### 2. Confirm Page Count

After the user approves Stage 1, ask for page count or page-count range as its own decision. Do not propose table-of-contents entries yet.

Offer 2-3 page-count options with tradeoffs, for example:

- 5 total pages: cover + contents + 3 content pages.
- 7 total pages: cover + contents + 5 content pages.
- 9 total pages: cover + contents + 7 content pages.

Always state the counting convention:

- Total PPT pages.
- Whether cover is included.
- Whether contents page is included.
- Number of actual content pages available after cover/contents.

If the user says "7 pages" without clarifying, ask whether that means `7 total PPT pages` or `7 content pages` before creating the table of contents.

Stage 2 required approval: page count or page-count range, counting convention, whether cover/contents are included, and resulting content-page budget.

After approval, save:

```text
.tmp/ppt-deep-search/<task-name>/baselines/02-page-count.md
```

Also create a page-number map in the baseline. For multi-page decks, preserve this order by default: `Page 1: cover`, `Page 2: top-level summary`, `Page 3: contents`, `Page 4-N: chapter content pages`. If the user asks for a 1-page output, produce only `Page 1: top-level summary` and omit contents and chapter content pages. Later page briefs must use these actual PPT page numbers, not a restarted content-page index.

### 2.5 Confirm Table of Contents

Only after page count is approved, propose the table of contents. The table of contents is a navigation contract, not a content-page plan.

Use this exact shape:

```text
01 小标题：...
说明：...

02 小标题：...
说明：...
```

Rules:

- The table of contents must have at most three content chapters unless the user explicitly requests more.
- The top-level summary page is not a table-of-contents entry; it is the standalone Page 2 in multi-page decks. If the output is only 1 page, omit the table of contents entirely.
- Each `小标题` must be short enough to fit the page's top-left chapter indicator.
- Each `说明` should be one concise sentence explaining what that chapter proves.
- Do not use `表达的观点 / 标题 / 分析总结` for the table of contents.

Stage 2.5 required approval: table-of-contents small titles, descriptions, order, and the chapter claim each entry represents.

After approval, save:

```text
.tmp/ppt-deep-search/<task-name>/baselines/02-table-of-contents.md
```

Then consolidate page count and table of contents into:

```text
.tmp/ppt-deep-search/<task-name>/baselines/02-deck-structure.md
```

Do not create chapter-internal page titles until this baseline exists.

### 3. Decompose One Chapter at a Time

Advance the research through focused turns, one chapter at a time. Never ask the user to approve all chapter page decompositions in one message.

For each chapter:

- Restate the approved chapter claim.
- Recalculate the remaining content-page budget before proposing the chapter's page count. State the remaining page numbers if useful.
- Propose that chapter's page count based on the total page budget and previously approved chapter allocations.
- Use the approved page-number map from Stage 2. If the deck includes cover and contents, do not restart content page numbering at `Page 1`.
- Do not present a page number outside the approved budget. If the desired chapter split would exceed the budget, resolve the budget tradeoff before showing the page plan.
- First propose only the viewpoint layer for that chapter's pages: page title, title subtitle, analysis-summary bullets, page role, and the chapter claim each page supports.
- Do not write dense supporting content yet. Wait until the user explicitly approves each page's title, title subtitle, and analysis-summary bullets.
- After the viewpoint layer is approved, expand the content layer autonomously: Claim / Evidence / Implication, reference-image strategy, supporting information, and boundaries. The human does not need to guide or approve dense content page by page.
- The content layer must support the approved viewpoint; it must not introduce a new unapproved viewpoint.
- Return to the user before finalizing content only if evidence contradicts the approved viewpoint, the content would materially change the title/subtitle/analysis-summary, or supplemental research changes the argument direction.
- Use `Page N`, `Page N+1`, etc. for actual page labels.
- Ask the user to approve or tell you the adjustment direction before moving from one chapter's viewpoint layer to the next chapter's viewpoint layer. Do not force alternatives unless the user asks.
- If the user revises a page title, title subtitle, or analysis-summary bullet, restate the full updated viewpoint layer before saving it as approved. Do not save a baseline that only records the changed fragment.
- Save a chapter baseline after approval.

Use this loop:

1. State the current decision in one sentence.
2. Offer one concise recommended proposal, or ask one open question if the chapter logic is still unclear.
3. Capture the user's choice or correction.
4. Update the live structure: thesis, pyramid, evidence map, approved chapter page plan, assumptions, or open questions.
5. Move to the next highest-impact unresolved decision.

Stage 3 required approval: each chapter's page decomposition, every page title, every page title subtitle, every page's analysis-summary bullets, every page role, and critical page-level boundaries. The title, subtitle, and analysis-summary bullets must be approved before the agent writes detailed supporting content for that page. After viewpoint approval, the agent should generate dense supporting content independently.

After each chapter is approved, save:

```text
.tmp/ppt-deep-search/<task-name>/baselines/03-chapter-<n>-page-plan.md
```

After all chapter viewpoint layers are approved, autonomously generate content layers for every approved page, then consolidate viewpoint and content layers into:

```text
.tmp/ppt-deep-search/<task-name>/baselines/03-page-plan.md
```

Only after this consolidated page-plan baseline exists may the agent write the final handoff files.

### 3.2 Fill Content With Source-Grounded Material

After the viewpoint layer is approved, fill each page with enough concrete material for the downstream PPT Maker to write body text without inventing substance.

Use this order:

1. First use the provided source material: paper sections, figures, tables, extracted XML, notes, repository docs, or user-provided artifacts.
2. If the source material is too thin to support the approved viewpoint, say so briefly and run targeted external research. Prefer official docs, original papers, project repositories, standards, benchmarks, vendor posts, or other primary/high-quality sources.
3. Use supplemental research to add context, comparisons, examples, definitions, adjacent approaches, adoption constraints, or counterpoints.
4. Label every supplemental item clearly in `Evidence`, `Evidence Map`, or `Source Usage Policy` so downstream readers know it did not come from the original source package.

External research should support the approved viewpoint, not create a new one. If research changes the viewpoint materially, return to the user for approval before writing the content layer.

### 3.5 Confirm Downstream Hard Constraints

Before writing the final handoff files to disk, explicitly ask the user to approve every hard constraint that the downstream PPT skill must follow.

The required approval bundle is:

- Page count or page-count range.
- Page-count convention: total pages vs content pages, including/excluding cover and contents.
- Target audience and desired reader belief change.
- Approved source-understanding analysis: what it is, what problem it solves, and what is distinctive versus similar approaches.
- SCQA, top-level thesis, and big logic.
- Table-of-contents small titles, descriptions, order, and represented chapter claims.
- Chapter logic, or for a 1-page output, the page's internal content beat sequence.
- Every page title.
- Every page's title subtitle.
- Every page's `分析总结` bullets.
- Every page role.
- Required source figures/tables/screenshots and their usage policy: original, summarize/rebuild, background only, or discard.
- Supplemental research sources, if used, and whether they are primary source, official docs, paper, repository, technical article, or needs verification.
- Claims that must be preserved.
- Boundary reminders that the downstream PPT skill must not weaken.

Before final handoff writing, confirm that every page went through this order: viewpoint layer approval first, then AI-generated content-layer expansion. If any page's content was drafted before its title, title subtitle, and analysis-summary bullets were approved, pause and ask the user to approve or revise the viewpoint layer before finalizing that page.

Do not ask the user to review dense content page by page unless the content would change an approved viewpoint or introduce a new major claim. The user owns logic; the agent owns source-grounded content generation.

Present the bundle compactly and ask for approval or corrections. Do not save the final `ppt_content_brief.md` and `research_audit.md` until the user approves this bundle, unless the user explicitly asks for an unapproved draft. If producing an unapproved draft, mark that status in `research_audit.md`.

A user approving the last chapter or saying "generate final files" is not enough unless they have also approved the final hard-constraint bundle in this stage. If the user asks to generate final files immediately after a chapter approval, first show the compact hard-constraint bundle below and ask for approval.

Approval prompt pattern:

```text
落盘前请确认这组下游硬约束：
- 听众：...
- 原始信息理解：它是什么 / 解决什么问题 / 跟同类技术比的亮点
- SCQA：...
- 顶层总结页：标题 / 标题说明 / 分析总结
- 大逻辑：...
- 页数：...
- 页数口径：总页数 / 正文内容页；是否包含封面和目录页
- 目录：
  - 01 小标题：... / 说明：...
- Page 1 标题：...
- Page 1 标题说明：...
- Page 1 分析总结：...
- 主证据图：...
- 不能说满的边界：...

是否批准我按这组约束写入 PPT Content Brief 和 Research Audit？你可以直接改其中任一项。
```

### 4. Build the Evidence Map

For every major claim, record:

- Evidence source and locator: file path, URL, section, figure/table number, quote snippet, or user statement.
- Evidence type: direct source, calculated, inferred, user judgment, or needs verification.
- Strength: strong, medium, weak, or missing.
- Counterevidence, boundary, or uncertainty.
- PPT relevance: must use as source figure, may summarize/rebuild, background only, or discard.

Anti-hallucination rule: numeric values, benchmark wins, dates, rankings, comparisons, and causal claims require explicit source locators. If the source locator is absent, move the statement to `Open Questions` or mark it `needs_verification`.

Before finalizing, run a skeptic pass:

- What claim would a knowledgeable reader dispute?
- Which slide candidate depends on inference rather than source?
- Which source figure could be misread if placed without context?
- Which conclusion should be softened with a boundary?
- Which missing evidence should be escalated to the user instead of silently invented?

### 5. Write the Handoff Files

Write the final handoff only when the user explicitly says to proceed, the conversation has resolved the main forks, or a deadline requires a first draft.

Write `ppt_content_brief.md` as the only downstream PPT copy source. It must contain only PPT-ready structured text. For multi-page decks, preserve this order: `Summary Page`, `Table of Contents`, then chapter-mapped `Page Content`. For a 1-page output, include only `Summary Page` after `Deck Metadata`; omit `Table of Contents` and `Page Content`.

```markdown
# PPT Content Brief

## Deck Metadata
主题：
目标读者：
页数口径：
核心结论：
内容来源：
关联审计文件：research_audit.md

## Summary Page
页码：Page 2
页面标题：
标题说明：
分析总结：
- 标签：可直接放入 PPT 的中文短句。
正文内容：
- 顶层总结页可直接使用的正文素材。
参考图片：
- ...
备注：
- 可选。只放 PPT 可用的脚注、讲者备注或谨慎表述。

## Table of Contents
01 小标题：...
说明：...

## Page Content

### Page 1: 页面标题
所属章节：必须精确匹配目录里的小标题
页面标题：...
标题说明：...
分析总结：
- 标签：可直接放入 PPT 的中文短句。
正文内容：
- 可直接展开成 PPT 正文的机制、数据、对比、例子、推理链或限制条件。
- 每条都要比标题和分析总结更具体，说明“为什么这样判断”或“下游页面该写什么”。
参考图片：
- ...
备注：
- 可选。只放 PPT 可用的脚注、讲者备注或谨慎表述。
```

Write `research_audit.md` separately. Use `references/research-audit-format.md` as the contract. Put Research Frame, Source Understanding, Pyramid Outline, Chapter Logic, page roles, supported chapter claims, Claim/Evidence/Implication, Evidence Map, Source Usage Policy, Visual Opportunities, Assumptions/Open Questions, and Approval Log there.

Do not put `Claim`, `Evidence`, `Implication`, source locator tables, approval history, local absolute source paths, `needs_verification`, `inference`, `user_judgment`, or `边界提醒` into `ppt_content_brief.md`. If a caveat matters for the slide, rewrite it as a concise `备注`. Put exact local paths and source locators in `research_audit.md`.

## Right-Size the Brief

Match the brief to the requested downstream artifact:

- If the user asks for a 1-page PPT, produce `## Summary Page` as `Page 1` and omit `## Table of Contents` and `## Page Content`.
- If the user asks for a short deck, produce one `Page Content` block per intended chapter content page unless the user asks for alternatives.
- Do not create a broad multi-chapter deck storyline when the task is a single page. Put unused angles in `Assumptions and Open Questions` or `Visual Opportunities`.
- Keep `Recommended Deck Storyline` scoped to the requested artifact, for example "one-page storyline" for a single-slide request.

## PPT Content Density

`## Summary Page` and each `### Page N:` section in `ppt_content_brief.md` must contain enough material for PPT Maker to create a dense page. As a default target:

- At least 1200 counted content characters for `## Summary Page` and at least 900 counted content characters per chapter content page, excluding headings and field labels. The summary page should be the highest-density page: compress the top-level conclusion, chapter logic, decision implications, key numbers or mechanisms, visual cue, and boundary wording into one PPT-ready page. A strong technical or decision content page usually lands around 1200-1800 counted characters.
- Every content page must include `所属章节`, and that value must exactly match one `小标题` in `## Table of Contents`. The summary page is separate and does not need `所属章节`.
- A `页面标题`, `标题说明`, and `分析总结` section. `分析总结` must contain 1-3 directly usable Chinese label bullets such as `粒度升级：...`.
- A `正文内容` section that reads like a PPT body material pack, not a list of more conclusions. Use it to provide the concrete body content a slide can consume: mechanisms, source facts, quantitative context, comparison points, causal chains, caveats rewritten for slides, and suggested reading order.
- A `参考图片` section that names the image/chart/screenshot/diagram candidate without prescribing layout.

Do not pad with vague filler just to pass the length check. If a page is thin, add source-grounded mechanisms, comparisons, constraints, implications, examples, or reading guidance. When the original source package is insufficient, do targeted external research and record the supplemental trail in `research_audit.md`, not in the PPT content file.

## QA

Before handing the brief to a PPT skill, save `ppt_content_brief.md` and run:

```powershell
python scripts/validate_ppt_content_brief.py .tmp/ppt-deep-search/<task-name>/ppt_content_brief.md --min-page-content-chars 900 --min-summary-content-chars 1200
```

For fixed-size outputs, add `--expected-pages <n>` as total PPT pages. For example, a 1-page PPT with only the summary page should use `--expected-pages 1`, while a 7-page deck with Page 1 cover, Page 2 summary, Page 3 contents, and Page 4-7 chapter content should use `--expected-pages 7`.

```powershell
python scripts/validate_ppt_content_brief.py .tmp/ppt-deep-search/<task-name>/ppt_content_brief.md --min-page-content-chars 900 --min-summary-content-chars 1200 --expected-pages 7
```

The QA script checks required downstream headings, stable PPT page fields, banned internal audit fields, banned visual-rendering fields, direct PPT usability, and per-page content density. Treat script failures as blockers. Keep source evidence QA in `research_audit.md`.

For dependency checks in this skill repository, run:

```powershell
python verify_dependencies.py
```
