# PPT Viewpoint Planning

Scope map:

- Owns visible viewpoint planning before final content expansion.
- Covers summary expression, title/subtitle rules, analysis-summary rules, page count, TOC, and chapter decomposition.
- Does not own final brief fields or density; use `ppt-content-brief-format.md`.

This reference owns visible slide-copy planning before final content expansion.
It does not define the final file format; use `ppt-content-brief-format.md` for
that.

## Visible Viewpoint Layer

The approved viewpoint layer contains:

- `页面标题`
- `标题说明`
- `分析总结`

For chapter content pages it also contains `所属章节`.

Keep internal page role, evidence status, source boundary, and reasoning notes in
baselines or `research_audit.md`, not in `ppt_content_brief.md`.

## Summary Page Expression

For top-level summary page approval, present 2-3 concrete candidates:

```text
【A】
页面标题：...
标题说明：...
分析总结：
- 小标题：解释
```

Show only fields that can become visible slide copy. Keep thesis notes, evidence
boundary, audience rationale, and internal page role outside the option block.

## Title And Subtitle

`页面标题` is a short claim hook. It must state the page's conclusion, not an
abstract theme, method name, outline label, or category.

Good examples:

- `先复测，再谈上线`
- `可立项，不可直上`
- `瓶颈在层，不只在 token`

Bad examples:

- `R-CLA 路线判断`
- `Depth-wise KV sharing`
- `KV cache 新实验轴`
- `问题分析`

`标题说明` adds condition, evidence, or boundary. It should carry scenario,
measurable benefit or cost, experimental condition, and decision implication
where available.

## Analysis Summary

`分析总结` contains 1-3 labeled core-claim bullets in `小标题：解释` form.

Choose the number by information density:

- Use one bullet when the page proves one condition, mechanism, or judgment.
- Use 2-3 bullets only for genuinely separate decision dimensions.
- Combine bullets that describe the same cause-effect chain.
- Move support detail into `正文内容`.

Good dimensions include:

- result plus deployment scope;
- benefit plus cost;
- scenario plus boundary;
- mechanism plus engineering proof.

Each bullet should be independently meaningful and provable by the page body.

## Visible-Copy QA

Before asking the user to approve visible copy, run:

```powershell
python scripts/validate_ppt_content_brief.py --visible-copy-check --title "..." --subtitle "..." --analysis-bullet "小标题：解释"
```

For summary pages add `--summary-page`.

Treat failures as blockers. Rewrite before asking for approval.

## Page Count

Confirm total PPT pages and convention:

- total pages vs content pages;
- including or excluding cover;
- including or excluding contents;
- whether Page 2 is a standalone summary page.

For one-page outputs, produce only `Summary Page` and omit contents and chapter
content.

## Table Of Contents

Create contents only after page count approval.

Each item uses:

```text
01 小标题：...
说明：...
```

Use at most 3 chapter items unless the user explicitly asks for more. The
`小标题` should be a navigation label; the body pages will carry claim-like
titles.

## Chapter Decomposition

Decompose one chapter at a time. For each chapter:

1. State the current decision in one sentence.
2. Offer one concise recommended page plan.
3. Ask the user what to adjust.
4. Save the approved chapter baseline.

Do not draft dense supporting content until the chapter's viewpoint layer is
approved. After approval, generate the content layer autonomously.

Return to the user before finalizing content only if evidence contradicts the
approved viewpoint, materially changes visible copy, or changes the argument
direction.
