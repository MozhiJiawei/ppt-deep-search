# Pyramid Principle Doctrine

This doctrine is the highest-level guidance for `ppt-deep-search`. Follow it before any workflow detail in `SKILL.md`.

## Core Belief

A PPT Content Brief is not a summary of source material. It is a pyramid-shaped content package that helps a reader accept one top-level summary. Internal evidence and approvals belong in a separate Research Audit.

The deck should answer the reader's governing question first, express that answer as a standalone top-level summary page, then support it with a small number of necessary arguments, page-level evidence, and implications.

Deep source understanding serves audience-facing expression. Original source quotes, tables, figures, and numeric claims provide credibility, but they are not the storyline by themselves. Translate source evidence into the reader's decision logic: what they should believe, why it matters for their context, what evidence makes it credible, and what boundary keeps the claim honest. Never choose between "faithful to the source" and "logical for the audience"; a strong brief must do both.

## Non-Negotiable Rules

1. **Answer first**
   - Start from the top-level summary the reader should take away.
   - The top-level summary must become its own page, usually Page 1 after cover/contents if those exist.
   - Do not start by listing paper sections, source figures, or implementation details.

2. **Parent ideas summarize child ideas**
   - A chapter title must be a claim, not a topic label.
   - Each chapter claim must directly support the top-level summary.
   - Each page must directly support one chapter claim.

3. **Same-level ideas must be the same kind of thing**
   - Do not mix problem statements, mechanisms, evidence, implications, and caveats as sibling chapters.
   - If the top-level summary is supported by "why this matters," "why this works," and "why this is credible," make those the sibling claims.

4. **Separate page scale, table of contents, and content pages**
   - Page count is a separate decision gate. Do not generate table-of-contents entries until page count is approved.
   - Page count must state its counting convention: total PPT pages vs content pages, and whether cover, contents, appendix, or transition pages are included.
   - Table-of-contents entries are navigation labels, not content pages.
   - Each table-of-contents entry must contain a concise title and one short explanation.
   - Do not use the A/B/C `表达的观点 / 标题 / 分析总结` pattern for table-of-contents entries.
   - Use A/B/C only for audience selection and the top-level summary page expression.
   - Do not use A/B/C for chapter decomposition or page decomposition unless the user explicitly asks for alternatives.
   - When listing multiple approved/proposed pages in one chapter, label them as `Page N`, not `A/B`.

5. **Use at most three chapter claims**
   - A human reader should be able to hold the storyline in working memory.
   - More than three chapters usually means the agent is covering source material instead of structuring an argument.
   - For small decks, use one or two chapters. For larger decks, use three.

6. **Decompose one chapter at a time**
   - Do not present all chapter page breakdowns in one turn.
   - Ask the user to confirm one chapter's internal page logic before moving to the next chapter.
   - Each chapter baseline becomes a constraint for later pages.

7. **Pages are not source-section slices**
   - A page is a unit of persuasion: one page title, one title subtitle, 1-3 analysis-summary bullets, one role, enough supporting facts, and explicit boundaries.
   - Source figures and tables are evidence for page claims, not page reasons by themselves.
   - Use source language and locators for traceability, then rewrite the visible claim in the reader's decision language. If a paragraph only describes what the paper says but not why the reader should care, it is not yet PPT-ready.

8. **Prefer quantitative, testable claims**
   - Write like an engineer or scientist making a decision, not like an essayist naming a theme.
   - Before proposing the top-level summary, inspect the source's tables, figures, chart images, captions, appendix tables, and extracted text enough to know the strongest data points.
   - When the source provides numbers, comparisons, costs, thresholds, rates, dates, sample sizes, rankings, or experimental conditions, use them in the top-level summary page, page subtitles, or analysis-summary bullets.
   - A strong visible claim usually names the object, scenario, measurable effect, cost or constraint, and decision implication.
   - If exact numbers are unavailable, use concrete observable conditions such as applicable task type, trigger condition, failure mode, or verification criterion.
   - Keep qualitative abstraction in the body only after the measurable or observable judgment is clear.

9. **SCQA frames the need for the pyramid**
   - Situation: what stable context does the reader already accept?
   - Complication: what changes or breaks their current judgment?
   - Question: what governing question must the deck answer?
   - Answer: the top-level summary.

## Required Pyramid Shape

```text
Top-level summary page
└── Chapter claim 1
    ├── Page claim 1.1
    └── Page claim 1.2
└── Chapter claim 2
    ├── Page claim 2.1
    └── Page claim 2.2
└── Chapter claim 3
    ├── Page claim 3.1
    └── Page claim 3.2
```

Allowed variation:

- A 1-page output may contain only the top-level summary page.
- A 3-5 page output usually has the top-level summary page plus one or two chapter claims.
- A 6+ page output may use up to three chapter claims.

## Good Chapter Claims

Good:

- `模型市场的浪费来自长尾与突发并存，而不是单模型 serving 不够快`
- `token-level 控制面突破了 request-level pooling 的 active-model 上限`
- `生产部署数据证明该基础设施方向具备 OPEX 价值`

Weak:

- `问题规模与商业痛点`
- `Aegaeon 的关键突破`
- `实验结果`
- `系统优化`

The weak examples are topics. They do not explain why the top-level summary is true.

## Human-in-the-Loop Discipline

The user must approve pyramid decisions from top to bottom:

1. Audience and belief change.
2. Source-understanding analysis: what it is, what problem it solves, and what is distinctive versus similar approaches.
3. SCQA and top-level summary page.
4. Page count only.
5. Table-of-contents entries: concise title plus short explanation.
6. Chapter 1 page decomposition.
7. Chapter 2 page decomposition.
8. Chapter 3 page decomposition, if present.
9. Final PPT Content Brief plus Research Audit.

Never skip ahead. Never ask the user to approve every chapter's page plan at once.
