# Pyramid Principle Doctrine

This doctrine is the highest-level guidance for `ppt-deep-search`. Follow it before any workflow detail in `SKILL.md`.

## Core Belief

A Storyline Brief is not a summary of source material. It is a pyramid of decisions that helps a reader accept one top-level conclusion.

The deck should answer the reader's governing question first, then support that answer with a small number of necessary arguments, then support each argument with page-level evidence and implications.

## Non-Negotiable Rules

1. **Answer first**
   - Start from the top-level conclusion the reader should take away.
   - The top-level conclusion must become its own page, usually Page 1 after cover/contents if those exist.
   - Do not start by listing paper sections, source figures, or implementation details.

2. **Parent ideas summarize child ideas**
   - A chapter title must be a claim, not a topic label.
   - Each chapter claim must directly support the top-level conclusion.
   - Each page must directly support one chapter claim.

3. **Same-level ideas must be the same kind of thing**
   - Do not mix problem statements, mechanisms, evidence, implications, and caveats as sibling chapters.
   - If the top-level conclusion is supported by "why this matters," "why this works," and "why this is credible," make those the sibling claims.

4. **Use at most three chapter claims**
   - A human reader should be able to hold the storyline in working memory.
   - More than three chapters usually means the agent is covering source material instead of structuring an argument.
   - For small decks, use one or two chapters. For larger decks, use three.

5. **Decompose one chapter at a time**
   - Do not present all chapter page breakdowns in one turn.
   - Ask the user to confirm one chapter's internal page logic before moving to the next chapter.
   - Each chapter baseline becomes a constraint for later pages.

6. **Pages are not source-section slices**
   - A page is a unit of persuasion: one page title, one title subtitle, 1-3 analysis-summary bullets, one role, enough supporting facts, and explicit boundaries.
   - Source figures and tables are evidence for page claims, not page reasons by themselves.

7. **SCQA frames the need for the pyramid**
   - Situation: what stable context does the reader already accept?
   - Complication: what changes or breaks their current judgment?
   - Question: what governing question must the deck answer?
   - Answer: the top-level conclusion.

## Required Pyramid Shape

```text
Top-level conclusion page
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

- A 1-page output may contain only the top-level conclusion page.
- A 3-5 page output usually has the top-level conclusion page plus one or two chapter claims.
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

The weak examples are topics. They do not explain why the top-level conclusion is true.

## Human-in-the-Loop Discipline

The user must approve pyramid decisions from top to bottom:

1. SCQA and top-level conclusion.
2. Page count and chapter claims.
3. Chapter 1 page decomposition.
4. Chapter 2 page decomposition.
5. Chapter 3 page decomposition, if present.
6. Final Storyline Brief.

Never skip ahead. Never ask the user to approve every chapter's page plan at once.
