# PPT Content Brief Format

This file defines the downstream-facing output contract for `ppt-deep-search`.

The final delivery artifact is `ppt_content_brief.md`. It must contain only structured text that a PPT maker can directly quote, adapt, or place into slides. Internal reasoning, evidence chains, source analysis, approval records, and QA notes belong in `research_audit.md`, not in the PPT content brief.

## Artifact Split

Produce two files at handoff:

- `ppt_content_brief.md`: downstream-facing slide content package. It contains PPT-ready titles, subtitles, summary labels, body text, and visual references.
- `research_audit.md`: internal working record. It contains source locators, Claim/Evidence/Implication, usage policy, assumptions, open questions, approval log, and anti-hallucination notes.

The PPT generation skill should consume `ppt_content_brief.md` first. It may inspect `research_audit.md` only for verification, not as slide copy.

## PPT Content Brief Required Headings

`ppt_content_brief.md` must include these headings exactly:

- `# PPT Content Brief`
- `## Deck Metadata`
- `## Summary Page`

For multi-page decks, it must also include:

- `## Table of Contents`
- `## Page Content`

For a 1-page output, omit `## Table of Contents` and `## Page Content`.

## Deck Metadata Fields

`## Deck Metadata` must include:

- `主题`
- `目标读者`
- `页数口径`
- `核心结论`
- `内容来源`
- `关联审计文件`

These fields are for downstream orientation. Keep them compact and PPT-relevant. Do not put source analysis, evidence discussion, approval history, or local absolute paths here. Use source names such as `Aegaeon paper package` and put exact file paths in `research_audit.md`.

## Table Of Contents Contract

`## Table of Contents` is the contents-page copy contract. It is not the page plan and not an evidence map. In multi-page decks, contents should be Page 3 because Page 2 is the standalone summary page.

Each item must use this shape:

```markdown
01 小标题：...
说明：...
```

Rules:

- Use at most 3 chapter items unless the user explicitly requested more.
- `小标题` must be a short navigation title suitable for the top-left chapter marker.
- `说明` must be one concise sentence suitable for the contents page.
- Do not include `Claim`, `Evidence`, source locators, approval notes, or boundary analysis in the contents section.

## Summary Page Contract

`## Summary Page` is the standalone top-level conclusion page. In multi-page decks it must be Page 2, after the cover and before `## Table of Contents`. In a 1-page output it is Page 1 and `## Table of Contents` / `## Page Content` should be omitted.

The summary page must include:

- `页码`: the actual PPT page number of the summary page.
- `页面标题`: direct slide title.
- `标题说明`: subtitle or title explanation.
- `分析总结`: 1-3 Chinese short core-claim statements that can go directly on the slide. Choose the count by the page's information density.
- `正文内容`: concise support material for the summary page, organized to support the selected core claim(s).
- `参考图片`: image, chart, screenshot, diagram, or visual evidence instruction.
- `备注`: optional speaker note or non-obtrusive caveat.

The summary page is not a chapter content page. It should express the deck's top-level conclusion and preview the logic that the following chapters will prove.

## Page Content Contract

Each slide content block must use this heading pattern:

```markdown
### Page N: 页面标题
```

`N` is the actual PPT page number, not a restarted content-page index.

Each page must include only these fields:

- `所属章节`: the exact `小标题` from `## Table of Contents` that this page supports.
- `页面标题`: direct slide title.
- `标题说明`: subtitle or title explanation.
- `分析总结`: 1-3 Chinese short core-claim statements that can go directly on the slide. Choose the count by the page's information density.
- `正文内容`: dense slide-body material, written as PPT-usable Chinese text and organized to support the selected core claim(s).
- `参考图片`: image, chart, screenshot, diagram, or visual evidence instruction the PPT maker can use.
- `备注`: optional speaker note or non-obtrusive caveat that may be used in notes/footnotes.

Do not include internal fields such as `页面角色`, `支撑的章节论点`, `Claim / Evidence / Implication`, `Evidence`, `Source Locator`, `Source Usage Policy`, `Approval Log`, `边界提醒`, or `信息密度说明` in `ppt_content_brief.md`.

## Page Field Meanings

- `所属章节`: use to map the page to a table-of-contents item. It must exactly match one `小标题`.
- `页面标题`: use as slide title. It should be a short object label or hook and readable as visible slide copy.
- `标题说明`: use as subtitle or lead sentence. It should be a high-signal quantitative sentence with scenario, measurable benefit/cost, experimental condition, or decision implication. `页面标题` and `标题说明` share one visible title line in the downstream slide, so their combined length must fit, and the title should be less than half the length of the explanation.
- `分析总结`: use as the high-visibility summary band. Each bullet must be a real core claim in the form `小标题：解释`. Summary pages usually carry more compression and can use 2-3 bullets. Chapter content pages are usually more focused and often need only 1-2 bullets. A good bullet is short, independently meaningful, evidence-bearing when possible, and provable by the page body.
- `正文内容`: use as the main content pool for the slide. It should be specific enough for the PPT maker to write blocks, captions, and explanatory paragraphs without inventing substance. Make the body support each selected `分析总结` claim with mechanisms, facts, comparisons, examples, implications, and cautions.
- `参考图片`: use to select or recreate visual material. It should name the visual object and its intended use, but not prescribe layout, template, font, color, or column count.
- `备注`: use for speaker notes, footnotes, or cautious wording. Keep it short and useful.

## Density Rules

The QA hard minimum is `1200` counted content characters for `## Summary Page` and `900` counted content characters per chapter content page, counted mainly from `分析总结`, `正文内容`, `参考图片`, and `备注`. The summary page is the highest-density page in the deck: it should compress the top-level conclusion, chapter logic, decision implications, key numbers or mechanisms, visual cue, and boundary wording into one PPT-ready page. A strong technical or decision content page usually lands around `1200-1800` counted characters.

The lower threshold exists because internal evidence and audit text no longer live inside the final PPT content file. Do not pad. Good density comes from:

- mechanisms and process steps;
- named components, actors, and roles;
- concrete comparisons;
- quantitative context that can be shown on slides;
- examples, constraints, and adoption implications;
- visual guidance tied to the slide message.

If a page is thin, enrich `正文内容` with source-grounded explanation or supplemental research, then record the source trail in `research_audit.md`.

## Banned Content In PPT Content Brief

The final PPT content file must not contain internal audit language or rendering implementation language.

Banned internal/audit tokens:

- `Claim`
- `Evidence`
- `Implication`
- `Evidence Map`
- `Source Locator`
- `Source Usage Policy`
- `Approval Log`
- `needs_verification`
- `user_judgment`
- `supplemental research`
- `primary source`
- `inference`
- `边界提醒`
- `证据边界`
- `证据状态`
- `误读风险`

Banned local path pattern:

- Windows absolute paths such as `D:\...`
- Unix absolute source paths such as `/mnt/...` or `/home/...`

Banned rendering/layout tokens:

- `visual_anchor.kind`
- `visual_anchor_renderer`
- `contentLayout`
- `renderer`
- `expected_renderer`
- `visual_strategy`
- `template:`
- `字号`
- `字体`
- `配色`
- `几栏`
- `两栏`
- `三栏`
- `四栏`

## Research Audit File

`research_audit.md` should contain everything useful for human review and QA that should not leak into PPT copy:

- approved audience and belief change;
- source understanding: what it is, what problem it solves, and what is distinctive;
- pyramid outline and approved chapter/page logic;
- Claim/Evidence/Implication table;
- evidence map with source locators and usage policy;
- supplemental research notes;
- numeric claim verification status;
- assumptions and open questions;
- approval log and baseline file references.

The audit file protects against hallucination. The PPT content file protects downstream slide generation from being polluted by internal scaffolding.

## Downstream PPT Maker Validation Checklist

A PPT generation skill should validate:

- `ppt_content_brief.md` has only the required downstream headings.
- `Deck Metadata` has required fields.
- `Table of Contents` uses short title plus one-sentence explanation.
- `Summary Page` exists before `Page Content` and contains PPT-ready title, subtitle, analysis summary, body content, visual reference, and notes.
- Each page has all required page fields.
- Each content page has `所属章节`, and it matches one table-of-contents `小标题`.
- `分析总结` has 1-3 directly usable Chinese labeled statements.
- `页面标题`, `标题说明`, and `分析总结` are concise enough to work as visible slide copy.
- `页面标题 + 标题说明` fits the shared title line.
- Default visible-copy QA budget: `页面标题` <= 18 Chinese-width units, `标题说明` <= 60, shared `页面标题 + 标题说明` <= 82, one `分析总结` bullet <= 52, summary-page analysis total <= 170, content-page analysis total <= 120. `页面标题` should be less than half the length of `标题说明`.
- The number of `分析总结` bullets matches the page role and information density: summary pages often use 2-3, while focused chapter content pages often use 1-2.
- Each `分析总结` bullet is a short core claim in `小标题：解释` form, and `正文内容` supports those selected claim(s).
- Each page meets the content-density threshold.
- Expected page count for QA means total PPT pages. `--expected-pages 1` means Summary Page only; `--expected-pages 7` means Page 1 cover, Page 2 summary, Page 3 contents, and Page 4-7 chapter content pages.
- Banned internal/audit tokens do not appear.
- Banned rendering/layout tokens do not appear.
- `关联审计文件` points to a `research_audit.md` file for verification if needed.
- No local absolute paths appear in `ppt_content_brief.md`; exact paths belong in `research_audit.md`.

When validation fails, ask for a revised content brief instead of silently using internal audit text as slide copy.
