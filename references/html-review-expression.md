# HTML Review Expression Contract

This contract defines reader-facing prose for the temporary source-understanding HTML review. Use it together with `html-review-surface.md`; it does not replace evidence, citation, data, or visual contracts.

## Core Rule

Visible prose is for the reader's next decision, not for the agent's workflow.

The main reading flow should translate source evidence into judgment a target reader can use. Internal process, extraction notes, evidence status, audit labels, and uncertainty bookkeeping belong in `report-data.json`, `research_audit.md`, HTML comments, or clearly separated
`<details>` blocks.

## Reader Lens

Before drafting the HTML review, define this lens in scratch notes or `report-data.json` metadata:

- `reader_role`: who will inspect the report.
- `reader_knows`: what they probably already understand.
- `reader_cares_about`: what would make the source matter to them.
- `reader_next_decision`: what they need to approve, reject, test, or clarify after reading.

Use this lens to decide how much background, mechanism explanation, comparison context, and boundary wording the visible report needs.

## Section Contract

Every major section must answer one reader question, even when the visible heading is a claim:

- What is this?
- Why does it matter?
- How does it work?
- What does the evidence prove?
- What does the evidence not prove?
- What should be checked next?

Keep the reader question out of the visible heading unless it is the most natural wording. The visible heading should state the section's conclusion or decision implication.

## Paragraph Contract

One paragraph should do one job:

- context
- mechanism
- evidence
- implication
- boundary

Avoid mixing all five into one dense paragraph. If a paragraph needs both evidence and caveat, make the caveat explicit in the next sentence or nearby aside.

## Figure And Table Contract

Every important figure, table, chart, or source image must translate evidence into reader judgment:

- what to notice
- what claim it supports
- what it does not prove

Do not use images as decorative proof. A caption or nearby aside should tell the reader where to look and what boundary prevents overclaiming.

## Natural Chinese

Use natural Chinese reasoning connectors when they make the argument easier to follow:

- `所以`
- `但`
- `这里要注意`
- `换句话说`
- `对读者来说`

Avoid stiff filler in visible prose:

- `本节介绍`
- `综上所述`
- `由此可见`
- `该文提出`

This is not a request for casual hosting language. Keep technical terms, exact numbers, benchmark names, method names, and source labels precise.

## Acceptance Check

Before showing the HTML review, read only the visible main body and ask:

- Can a reader who has not opened the source understand the decision question?
- Does each major section answer a concrete reader question?
- Does each visual say what to notice, what it supports, and what it cannot prove?
- Are internal workflow notes absent from the main reading flow?
- Is the prose clear without becoming shallow or promotional?
