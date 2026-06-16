# HTML Review Evidence

This reference owns citation, provenance, captured webpage source package, and
final-report evidence-mapping rules for the temporary HTML review.

## Evidence Rules

- Treat source materials as primary evidence.
- Use external research to contextualize, not overwrite source boundaries.
- For news or recent entities, verify with current web research and concrete
  dates.
- Numeric claims, comparisons, rankings, dates, causal claims, and benchmark
  wins require citations.
- If a claim has no locator, remove it from the visible report or phrase it as
  an open question in Chinese.
- Quote sparingly. Prefer paraphrase plus locator.
- Missing citations should trigger source acquisition, not citation removal.

## Captured Webpage Sources

Before citing a webpage, use a local source package produced by
`web-article-capture/SKILL.md`, or create one before writing the report.

Consume the package by reading its handoff files:

```text
<source-slug>/
  source.md
  images/
```

`source.md` is the upstream reading artifact. It should contain the webpage URL,
title, captured date when available, article/main text, local image references,
original image URLs, captions or nearby text, and capture notes. `images/`
contains original webpage images referenced by `source.md`.

Do not add extra capture-format requirements from this skill. If the report
needs report-specific page captures, derived crops, copied assets, or evidence mappings, create
and describe them in the HTML review package and `report-data.json`.

Do not present these as captured webpage source packages:

- search-result snippets;
- raw HTML;
- `curl` or `Invoke-WebRequest` output;
- third-party crawler output;
- self-written Playwright, Puppeteer, or Selenium captures;
- hand-written excerpts.

## Citation Anchors

Every visible citation marker must be clickable.

Use stable HTML anchors:

```html
<sup id="cite-ref-t4-1"><a href="#ref-t4">4</a></sup>
<li id="ref-t4">[T4] Table 4 ... <a href="#cite-ref-t4-1">back</a></li>
```

If one reference is cited multiple times, use unique body ids such as
`cite-ref-t4-1` and `cite-ref-t4-2`. The reference may link back to the first
or nearest occurrence.

Do not paste dense citation chains such as `[S1][F4][T2]` into paragraphs.
Use the most important 1-2 markers and list extra locators in the reference
entry.

## Webpage Images In The Final Report

When a webpage image from a captured source package is displayed in the final
HTML report, copy or derive the displayed asset under:

```text
<workspace-root>/review/assets/
```

Reference them with relative paths such as:

```text
assets/<image>.png
```

Do not hotlink remote images. Screenshots are useful audit evidence, but they
are not a substitute for original webpage images when the report needs the
actual image.

## Audit Placement

Audit status, data-model fields, and agent work-log labels belong in
`report-data.json`, hidden details blocks, or `research_audit.md`, not the main
visible flow.
