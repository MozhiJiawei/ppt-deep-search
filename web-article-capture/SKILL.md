---
name: web-article-capture
description: >-
  Extract article/main webpage text and original inline images into compact source packages for downstream agents. Use when Codex needs browser-rendered webpage capture for source grounding, media-rich official pages, article text, webpage image assets, or reusable web source packages.
---

# Web Article Capture

Use Codex in-app Browser to extract each target page's article/main正文图文. Produce one compact Markdown source package per page for downstream agents.

## Browser Entry

Before browser work, read `browser:control-in-app-browser`. Browser is usually controlled through Node REPL with `agent.browsers.get("iab")`.

## Capture Principles

First understand the rendered page, then choose the extraction approach that fits that page.

The target is the page's正文 reading experience: the main text plus the original images that belong inside that正文 flow. Preserve the relationship between paragraphs, headings, captions, charts, diagrams, and nearby images.

Use dynamic page-specific extraction when needed. A product page, docs page, blog post, keynote page, and live blog may each need a different DOM path or asset strategy. Let the rendered page structure decide the capture logic.

Prefer images that a reader would naturally treat as part of the article/main content: hero images, body figures, charts, diagrams, tables rendered as images, and image/caption pairs tied to nearby正文. Keep image references near the text they support.

Screenshots of the rendered page are not source images. A page with no正文 images can have an empty `images/` directory and a note in `source.md`.

## Browser Recovery

Treat Browser failures as page-specific states to investigate before changing approach.

- When navigation times out in a batch run, retry that URL in a fresh tab before deciding it is blocked.
- When a page uses lazy-loaded figures, scroll to the正文 figure/chart area and let the rendered page load real image assets before collecting `currentSrc`, `srcset`, `data-src`, or equivalent asset URLs.
- When Browser access remains blocked after focused retry, record the blocked stage in `source.md`: browser setup, tab creation, navigation, load state, DOM snapshot, or image asset loading.

Use the validator before handing off.

## Output

For each page, write one directory:

```text
<output-root>/<source-slug>/
  source.md
  images/
```

`source.md` is the downstream-facing file. Include:

- source URL, title, captured date, publisher/date/author when available;
- article/main正文 in readable Markdown structure;
- local image references such as `![caption](images/image-01.jpg)` near the related text;
- original image URL and caption/nearby text below each image;
- brief capture notes when they help a later agent judge reliability.

`images/` contains the original webpage images referenced by `source.md`.

Run the validator before handing off:

```powershell
python web-article-capture/scripts/validate_capture_package.py <output-root> --require-images when-referenced
```
