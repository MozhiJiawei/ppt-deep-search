---
name: ppt-deep-search
description: Human-in-the-loop deep research and storyline planning for PPT generation. Use when Codex must turn papers, webpages, Markdown, repository analysis, PDFs, notes, or raw user material into a structured Storyline Brief before a downstream PPT skill creates slides. Use for research framing, reader cognitive path design, pyramid-outline construction, claim/evidence/implication mapping, source-figure usage policy, slide/page role candidates, and anti-hallucination evidence review. Do not use for PPTX visual rendering, layout templates, font/style decisions, export, or visual QA.
---

# PPT Deep Search

Build a source-grounded Storyline Brief before PPT production. Act as content editor and research partner: frame the question, challenge the thesis, organize evidence, expose uncertainty, and hand a semi-structured Markdown brief to the downstream PPT skill.

This skill is modeled as a research dialogue, not a one-shot summarizer. The durable output is the Storyline Brief, but the main work is helping the user make content decisions before the downstream PPT skill renders slides.

Before doing any storyline work, read `references/pyramid-principle.md` and follow it as the highest-level doctrine. If any workflow detail conflicts with that doctrine, the doctrine wins.

## Operating Rules

- Use Chinese for all user-facing interaction by default, including questions, options, stage summaries, approval prompts, and final handoff notes. Keep source titles, figure/table labels, code paths, URLs, model names, metrics, and technical terms in their original language when that improves traceability.
- Work human-in-the-loop by default. Do not skip straight to the final Storyline Brief unless the user explicitly asks for a one-pass draft or the research frame is already fully specified.
- Ask one key question at a time when research direction, target reader, thesis strength, or evidence boundary is unclear. One turn should resolve one decision.
- Ask what the user is already thinking before offering a polished AI framework. Use the user's judgment as a first-class input, not as an afterthought.
- Prefer single-select options at major forks, with a free-form escape hatch. Use open prose questions only when options would bias the answer or the user needs to explain context.
- Keep a live research structure after each round: research frame, thesis, pyramid outline, evidence map, open questions, and page candidates.
- Do not make visual-rendering decisions. Avoid fields such as `visual_anchor.kind`, `template`, `contentLayout`, renderer names, column layout, font size, color, card structure, and visual-anchor implementation details.
- Do decide content intent: chapter logic, page titles, page roles, core claims, source evidence, source-figure usage policy, and wording boundaries.
- Treat every factual claim as one of: `source`, `calculation`, `inference`, `user_judgment`, or `needs_verification`.
- Never upgrade weak evidence into a fact. If a claim lacks source support, label it as inference or open question.
- If the approved viewpoint needs more support than the provided source material contains, use external research such as web search, official docs, papers, repository docs, or reputable technical articles to gather more context. Mark those materials as supplemental evidence and explain how they support, qualify, or challenge the approved viewpoint.
- Do not let external research replace the approved viewpoint or blur source boundaries. Separate `primary source`, `supplemental research`, `inference`, and `user_judgment` in the evidence map.
- Absolute local source paths are acceptable when the workflow runs on the same machine. Prefer readable locators, and do not rewrite paths if absolute paths make the downstream handoff clearer.
- Put all temporary notes, drafts, extracted inventories, and QA outputs under the host workspace `.tmp/ppt-deep-search/<task-name>/`.

## Workflow

Follow the pyramid principle doctrine in `references/pyramid-principle.md`: confirm the audience first, analyze the source material in plain language, resolve SCQA and the top-level summary page, confirm page count, create concise table-of-contents entries, then decompose one chapter at a time. Do not generate a table of contents before page count is approved, and do not decompose pages before the table of contents is approved.

Each stage has two gates:

1. User approval gate: ask the user to approve or correct the stage output.
2. Baseline persistence gate: after approval, save that stage output under `.tmp/ppt-deep-search/<task-name>/baselines/` and treat it as the baseline for later stages.

Do not silently rewrite an approved baseline. If later evidence suggests a change, ask whether to revise the baseline and record the revision in `Approval Log`.

After saving any approved baseline, tell the user the baseline path in one short sentence. If the user chooses a previous option after several challenge rounds, preserve that history in the baseline and record which historical option was selected.

### 0. Assess and Start the Dialogue

Classify the task before producing structure:

- **Lightweight**: the user already has a topic, reader, and expected deck use. Ask at most one clarifying question, then draft a compact Storyline Brief.
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

Also create a page-number map in the baseline. If cover and contents are included, preserve actual PPT page numbers, for example: `Page 1: cover`, `Page 2: contents`, `Page 3: top-level summary`, `Page 4-N: content pages`. Later page briefs must use these actual PPT page numbers, not a restarted content-page index.

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
- The top-level summary page is not necessarily a table-of-contents entry; it may be the opening summary page.
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

Only after this consolidated page-plan baseline exists may the agent write the final Storyline Brief.

### 3.2 Fill Content With Source-Grounded Material

After the viewpoint layer is approved, fill each page with enough concrete material for the downstream PPT Maker to write body text without inventing substance.

Use this order:

1. First use the provided source material: paper sections, figures, tables, extracted XML, notes, repository docs, or user-provided artifacts.
2. If the source material is too thin to support the approved viewpoint, say so briefly and run targeted external research. Prefer official docs, original papers, project repositories, standards, benchmarks, vendor posts, or other primary/high-quality sources.
3. Use supplemental research to add context, comparisons, examples, definitions, adjacent approaches, adoption constraints, or counterpoints.
4. Label every supplemental item clearly in `Evidence`, `Evidence Map`, or `Source Usage Policy` so downstream readers know it did not come from the original source package.

External research should support the approved viewpoint, not create a new one. If research changes the viewpoint materially, return to the user for approval before writing the content layer.

### 3.5 Confirm Downstream Hard Constraints

Before writing the final Storyline Brief to disk, explicitly ask the user to approve every hard constraint that the downstream PPT skill must follow.

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

Before final Storyline Brief writing, confirm that every page went through this order: viewpoint layer approval first, then AI-generated content-layer expansion. If any page's content was drafted before its title, title subtitle, and analysis-summary bullets were approved, pause and ask the user to approve or revise the viewpoint layer before finalizing that page.

Do not ask the user to review dense content page by page unless the content would change an approved viewpoint or introduce a new major claim. The user owns logic; the agent owns source-grounded content generation.

Present the bundle compactly and ask for approval or corrections. Do not save the final `storyline_brief.md` until the user approves this bundle, unless the user explicitly asks for an unapproved draft. If producing an unapproved draft, mark it clearly in `Research Frame` and `Assumptions and Open Questions`.

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

是否批准我按这组约束写入 Storyline Brief？你可以直接改其中任一项。
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

### 5. Write the Storyline Brief

Write the final Storyline Brief only when the user explicitly says to proceed, the conversation has resolved the main forks, or a deadline requires a first draft. Use this exact Markdown skeleton:

```markdown
# Storyline Brief

## Research Frame
研究问题：
目标读者：
读者当前判断：
希望改变的判断：
核心结论：
材料范围：
证据边界：

## Source Understanding
它是什么：
它解决了什么问题：
跟同类技术比有什么亮点：

## Executive Thesis
...

## Reader Cognitive Path
1. ...
2. ...
3. ...

## Pyramid Outline
0. 顶层总结页：...
   页面标题：
   标题说明：
   分析总结：
1. 章节论点：...
   二级支撑：
   - ...
   证据状态：
   - ...
   边界：
   - ...

## Chapter Logic
1. 目录小标题：...
   目录说明：...
   章节论点：...
   章节角色：建立问题 / 解释机制 / 证明效果 / 对比方案 / 提炼启示 / 行动建议
   本章必须讲清：...
   关键证据：...

## Page Briefs

### Page 1: 页面标题
页面角色：frame / claim / mechanism / evidence / comparison / implication / synthesis
支撑的章节论点：顶层总结页 / 章节论点 1 / 章节论点 2 / 章节论点 3
页面标题：...
标题说明：...
分析总结：
- 标签：可直接放入 PPT 的中文短句。
Claim / Evidence / Implication：
- Claim：...
  Evidence：primary source / supplemental research / inference / user_judgment / needs_verification...
  Implication：...
参考图片：
- ...
支撑信息：
- 正文素材：可直接展开成 PPT 正文的机制、数据、对比、例子、推理链或限制条件。
- 正文素材：每条都要比标题和分析总结更具体，说明“为什么这样判断”或“下游页面该写什么”。
- 正文素材：优先给 source-grounded 细节；不确定的推论要标注为 inference / needs_verification。
边界提醒：
- ...
信息密度说明：本页为 PPT Maker 提供足够正文素材，避免只给一句结论。

## Claim Evidence Implication Table
| ID | Claim | Evidence | Evidence Type | Strength | Implication | Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | ... | ... | source/inference/user_judgment/needs_verification | strong/medium/weak/missing | ... | ... |

## Evidence Map
| Evidence ID | Source Locator | Supports Claim | Usage Policy | Must Preserve | Misread Risk |
| --- | --- | --- | --- | --- | --- |
| E1 | ... | C1 | original / summarize / background / discard | ... | ... |

## Source Usage Policy
- Must use original:
- May summarize or rebuild:
- Background only:
- Supplemental research:
- Discard:

## Visual Opportunities
- ...

## Assumptions and Open Questions
- Assumption:
- Open question:

## Recommended Deck Storyline
...

## Approval Log
| Stage | Approved Constraint | User Approval Summary | Baseline File |
| --- | --- | --- | --- |
| 1 | Audience and belief change | ... | .tmp/ppt-deep-search/<task-name>/baselines/01-audience.md |
| 1.5 | Source understanding: what it is, solved problem, distinctive亮点 | ... | .tmp/ppt-deep-search/<task-name>/baselines/01-source-understanding.md |
| 1.6 | SCQA, big logic, top-level summary page | ... | .tmp/ppt-deep-search/<task-name>/baselines/01-audience-thesis.md |
| 2 | Page count and counting convention | ... | .tmp/ppt-deep-search/<task-name>/baselines/02-page-count.md |
| 2.5 | Table-of-contents small titles, descriptions, order, chapter claims | ... | .tmp/ppt-deep-search/<task-name>/baselines/02-table-of-contents.md |
| 3 | Chapter-by-chapter page titles, title subtitles, analysis summaries, page roles, source usage, boundaries | ... | .tmp/ppt-deep-search/<task-name>/baselines/03-page-plan.md |
```

## Right-Size the Brief

Match the brief to the requested downstream artifact:

- If the user asks for a 1-page PPT, produce exactly one `Page Brief`. Treat `Chapter Logic` as the content beat sequence inside that page, not as a multi-slide chapter plan.
- If the user asks for a short deck, produce one `Page Brief` per intended content page unless the user asks for alternatives.
- Do not create a broad multi-chapter deck storyline when the task is a single page. Put unused angles in `Assumptions and Open Questions` or `Visual Opportunities`.
- Keep `Recommended Deck Storyline` scoped to the requested artifact, for example "one-page storyline" for a single-slide request.

## Page Brief Density

Each `### Page N:` section must contain enough material for PPT Maker to create a dense content page. As a default target:

- At least 900 counted content characters per page brief, excluding headings and field labels.
- A `页面标题`, `标题说明`, and `分析总结` section. `分析总结` must contain 1-3 directly usable Chinese label bullets such as `粒度升级：...`.
- At least one `Claim / Evidence / Implication` item.
- A `支撑的章节论点` field that links the page to either the standalone top-level summary page or one approved chapter claim.
- At least one source locator, user-judgment marker, or `needs_verification` marker in `Evidence`.
- A `支撑信息` section that reads like a deep-research material pack, not a list of more conclusions. Use it to provide the concrete body content a slide can consume: mechanisms, source facts, quantitative context, comparison points, causal chains, caveats, and suggested reading order.
- At least one `边界提醒` item unless the page is a cover/contents candidate.

Do not pad with vague filler just to pass the length check. If a page is thin, add source-grounded mechanisms, comparisons, constraints, implications, examples, or reading guidance. When the original source package is insufficient, do targeted external research and mark it as supplemental. The goal is that a downstream PPT Maker can fill title, analysis-summary band, body text, captions, and evidence notes without inventing missing substance.

## QA

Before handing the brief to a PPT skill, save it as Markdown and run:

```powershell
python scripts/validate_storyline_brief.py .tmp/ppt-deep-search/<task-name>/storyline_brief.md --min-page-content-chars 900
```

For fixed-size outputs, add `--expected-pages <n>`. For example, a 1-page PPT brief should pass:

```powershell
python scripts/validate_storyline_brief.py .tmp/ppt-deep-search/<task-name>/storyline_brief.md --min-page-content-chars 900 --expected-pages 1
```

The QA script checks required output headings, stable page fields, banned visual-rendering fields, per-page information density, claim/evidence/implication presence, evidence source discipline, source usage policy, and open-question sections. Treat script failures as blockers.

For dependency checks in this skill repository, run:

```powershell
python verify_dependencies.py
```
