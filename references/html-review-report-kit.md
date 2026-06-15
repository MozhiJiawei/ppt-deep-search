# HTML Review Report Kit

Scope map:

- Owns reusable report blocks, CSS rhythm, and optional chart/block guidance.
- Does not own reader-facing prose; use `html-review-expression.md`.
- Does not own evidence rules; use `html-review-evidence.md`.
- Does not own full HTML templates or assets.

This file defines reusable report blocks for source-understanding HTML pages.
Use it when the page needs repeatable CSS rhythm, compact data blocks, source
visual placement, or browser preview behavior.

It does not own reader-facing prose. For that, use
`html-review-expression.md`.

## Data-Smart Standard

Use blocks only when they help the reader answer a technical question. Avoid
decorative charts, decorative cards, and UI polish that hides evidence.

Each data or visual block should expose:

- the claim it supports;
- source, unit, condition, and boundary;
- what the reader should notice;
- what the evidence does not prove.

## Report Rhythm

Use a calm long-form report shell:

- first viewport: conclusion, strongest evidence, and decision implication;
- middle: context, comparisons, mechanism, and evidence;
- end: limitations, open questions, and references.

Side navigation may use stable logical labels. Body headings should be
topic-specific conclusions.

## CSS Tokens

Use a small token set rather than one-off styling:

- text: body, muted, heading, accent;
- surface: page, panel, evidence, callout;
- border: subtle and evidence;
- spacing: small, medium, large;
- chart: axis, grid, highlight, source.

Prefer simple CSS custom properties. Avoid large decorative palettes.

## Status Strip

Use a status strip for compact facts such as date, source type, evidence
strength, benchmark condition, or deployment status.

Rules:

- Keep labels short.
- Cite any factual status.
- Do not expose internal audit labels in visible text.

## Summary Card

Use a summary card for the first viewport or section lead.

It should contain:

- one conclusion sentence;
- 2-4 evidence points;
- one boundary or next-decision note;
- optional sparkline or compact indicator when data exists.

## Chart With Aside

Use when a reconstructed or extracted chart needs interpretation.

Pair:

- chart or table;
- source or extraction note;
- aside explaining what to notice, what claim it supports, and what it does not
  prove.

Do not chart values that lack source locators.

## Data Table With Interpretation

Use for method comparisons, benchmark rows, feature matrices, or source tables.

Rules:

- Keep columns focused on the reader's decision.
- Include unit and condition in headers or captions.
- Add one interpretation paragraph after the table.
- Cite rows or source groups.

## Original Evidence Pair

Use when the report interprets a source figure, table, screenshot, or product
image.

Pair:

- original image or capture;
- plain-language interpretation;
- source locator;
- boundary note.

For webpage sources, use local assets under `review/assets/`.

## Method Mini-Brief

Use for each comparison object in the "已有做法与缺口" job.

Recommended fields:

- 一句话定位
- 核心机制
- 主要证据
- 适用边界
- 与本文或本对象的关键差异

Each mini-brief needs its own source basis. Do not use a single citation at the
end if several fields contain sourced assertions.

## Matrix, Heatmap, And Strip Chart

Use a comparison matrix when the reader must compare options across the same
criteria.

Use a heatmap when relative strength matters more than precise values.

Use a strip chart for one-dimensional distribution, ranking, timeline, or
capacity comparison.

All three require explicit source basis and a caption that states the takeaway.

## Decision Register

Use a decision register for open questions, risks, and next checks.

Columns can include:

- question;
- why it matters;
- current evidence;
- missing check;
- recommended next action.

Keep it reader-facing. Move internal evidence status to the audit file.

## Chart.js Defaults

Chart.js is optional. If used:

- load it intentionally;
- keep chart options minimal;
- label units and conditions;
- cite the backing data;
- preview through the local server when CDN resources are involved.

## Inline SVG

Inline SVG is suitable for compact sparklines, flows, and diagrams. Keep SVG
simple and inspectable. Do not embed large generated SVG blobs when a table or
source image would be clearer.

## Scroll Reveal

Scroll effects are optional. They must not hide evidence, delay reading, or make
the report depend on animation to make sense.

## Self-Check

Before approval, confirm:

- every chart or table answers a named question;
- reconstructed visuals are paired with source evidence;
- source images are local when sourced from webpages;
- captions say what to notice;
- citations are clickable and quiet;
- the page remains readable without animation.
