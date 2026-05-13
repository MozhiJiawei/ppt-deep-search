# Storyline Brief Format

This file defines the contract between `ppt-deep-search` and downstream PPT generation skills. It is a semantic and QA contract, not a slide layout contract.

The Storyline Brief must give the PPT maker enough grounded material to write real slide content without inventing substance. It should preserve the human-approved logic while letting the PPT maker decide layout, visual composition, and rendering details.

## Required Headings

The final brief must include these headings exactly:

- `# Storyline Brief`
- `## Research Frame`
- `## Source Understanding`
- `## Executive Thesis`
- `## Reader Cognitive Path`
- `## Pyramid Outline`
- `## Chapter Logic`
- `## Page Briefs`
- `## Claim Evidence Implication Table`
- `## Evidence Map`
- `## Source Usage Policy`
- `## Visual Opportunities`
- `## Assumptions and Open Questions`
- `## Recommended Deck Storyline`
- `## Approval Log`

Downstream tools should treat missing headings as a hard contract failure.

## QA-Checked Top-Level Fields

`## Research Frame` must include:

- `研究问题`
- `目标读者`
- `读者当前判断`
- `希望改变的判断`
- `核心结论`
- `材料范围`
- `证据边界`

`## Source Understanding` must include:

- `它是什么`
- `它解决了什么问题`
- `跟同类技术比有什么亮点`

The source understanding section exists so humans can challenge the agent before approving the summary page. It should be written after the audience is clear and before the top-level summary page is approved.

## Pyramid And Chapter Contract

The brief follows the Pyramid Principle:

1. Confirm the audience and judgment shift.
2. Confirm the source understanding.
3. Confirm the top-level conclusion as its own summary page.
4. Confirm total page count and counting convention.
5. Confirm the table of contents.
6. Confirm each chapter's title and viewpoint summary.
7. Generate page content only after the relevant chapter title and viewpoint summary are approved.

`## Pyramid Outline` must explicitly include a standalone top-level summary page, using wording such as `顶层总结页` or `Top-level summary page`.

`## Chapter Logic` must contain no more than 3 chapters. Each chapter item must include:

- `目录小标题`: a short title for the table of contents.
- `目录说明`: a one-sentence explanation shown on the contents page.
- `章节论点`: the chapter-level argument that all pages in the chapter support.

The table of contents is not the page plan. It is a compact navigation page made of short titles plus short explanations.

## Page Brief Contract

Each page brief must use this heading pattern:

```markdown
### Page N: 页面标题
```

`N` is the actual PPT page number, not a restarted content-page index. If the deck includes cover and contents pages, page briefs must still use the real downstream page numbers.

Each page brief must include these fields:

- `页面角色`: the slide's job in the argument, such as top-level summary, problem framing, mechanism explanation, proof page, comparison, implication, recommendation, or caveat.
- `支撑的章节论点`: the approved chapter argument this page supports. The page should not drift away from it.
- `页面标题`: the direct slide title for the PPT maker.
- `标题说明`: the subtitle or title explanation for the PPT maker.
- `分析总结`: 1-3 Chinese short labeled statements that can go directly on the slide, for example `- 资源浪费：...`.
- `Claim / Evidence / Implication`: the page's logic chain. It must visibly include `Claim`, `Evidence`, and `Implication`.
- `参考图片`: source image, evidence image, diagram idea, screenshot strategy, or `无直接图片，建议结构图/流程图`. It should guide the PPT maker without prescribing layout.
- `支撑信息`: enough grounded body material for the PPT maker to write the slide. This is where mechanisms, comparisons, examples, causal chains, constraints, quotes, source locators, and numeric evidence belong.
- `边界提醒`: caveats, uncertainty, source limitations, or claims that need verification.

Optional helper fields are allowed if they do not duplicate rendering decisions. `信息密度说明` is recommended when explaining why the page has enough body material or where supplemental research was used.

## How Downstream PPT Makers Should Use Page Fields

- Use `页面标题` as the slide title.
- Use `标题说明` as subtitle, explanatory line, or title support.
- Use `分析总结` as the summary band or high-visibility takeaway block.
- Use `支撑信息` as the main content source. Do not rely only on title and summary.
- Use `Claim / Evidence / Implication` to preserve argumentative logic.
- Use `参考图片` and `Evidence Map` to choose visual/evidence assets.
- Use `边界提醒` as footnote, caveat, speaker note, or verification warning.

If a page lacks enough support material, the downstream PPT maker should fail validation or ask for more research instead of inventing body content.

## Density Rules

The QA hard minimum is `1400` counted content characters per Page Brief. A strong target for deep-research PPT work is `1800-2400` counted content characters per page.

The density requirement exists to prevent empty slides. It should not be satisfied by padding, repeated conclusions, or verbose restatement. Good density comes from:

- concrete mechanisms and process steps;
- named entities, components, and roles;
- primary-source details and source locators;
- comparisons with alternatives or prior approaches;
- constraints, tradeoffs, and failure modes;
- numeric claims with source or verification status;
- implications for the target reader;
- visual evidence guidance tied to the page argument.

When original material is too thin to support an approved claim, the agent may use web search or other research tools to gather supplemental information. Supplemental research must be marked as supplemental and must not replace the human-approved viewpoint.

## Evidence Discipline

Every page must include evidence markers. Acceptable markers include:

- `primary source`
- `source`
- `supplemental research`
- `calculation`
- `inference`
- `user_judgment`
- `needs_verification`
- `原文`
- `推论`
- `用户判断`
- `待验证`

Numeric claims must carry a visible source locator, calculation note, or verification marker. If a number is useful but not verified, mark it as `needs_verification` or `待验证`.

Evidence should support the approved viewpoint. Do not create a new claim just because an external source is interesting.

## Required Tables

`## Claim Evidence Implication Table` must include these columns or clearly equivalent labels:

- `Claim`
- `Evidence`
- `Evidence Type`
- `Strength`
- `Implication`
- `Boundary`

`## Evidence Map` must include:

- `Source Locator`
- `Supports Claim`
- `Usage Policy`
- `Misread Risk`

`## Source Usage Policy` must classify sources with one of these policies or Chinese equivalents:

- `original` / `原样`
- `summarize` / `摘要`
- `background` / `背景`
- `supplemental` / `补充`
- `discard` / `舍弃`

`## Assumptions and Open Questions` must include explicit assumption or open-question markers.

`## Approval Log` must include proof that the human approved or corrected these hard constraints:

- `Audience`
- `Source understanding`
- `Page count`
- `counting convention`
- `Page titles`
- `Baseline File`

## Banned Layout And Rendering Fields

The Storyline Brief must not prescribe PPT rendering implementation. These fields or concepts are banned and should fail QA:

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

The brief may recommend evidence images, diagrams, screenshots, or visual opportunities. It must not tell the PPT maker which exact template, renderer, font, color system, or column layout to use.

## Downstream PPT Maker Validation Checklist

A PPT generation skill should validate at least:

- All required headings exist.
- `Research Frame` and `Source Understanding` contain required fields.
- `Chapter Logic` has at most 3 chapters.
- Each chapter has `目录小标题`, `目录说明`, and `章节论点`.
- A standalone top-level summary page exists.
- Page briefs use actual PPT page numbers.
- Every page contains all required page fields.
- `分析总结` has 1-3 directly usable Chinese labeled statements.
- Every page includes `Claim`, `Evidence`, and `Implication`.
- Every page meets the hard density threshold.
- Every page has evidence markers and a non-empty boundary reminder.
- Numeric claims include source, calculation, or verification status.
- CEI table and Evidence Map include required columns.
- Source Usage Policy classifies source usage.
- Approval Log records human approval of hard downstream constraints.
- Banned layout/rendering fields do not appear.

When validation fails, downstream tools should ask for a revised brief or mark the failing pages explicitly instead of silently filling gaps.
