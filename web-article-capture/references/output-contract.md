# Output Contract

This skill creates compact source packages for downstream agents.

## Directory Shape

```text
<output-root>/<source-slug>/
  source.md
  images/
```

## `source.md`

`source.md` is the default file for downstream agents to read. It carries the source metadata, article/main text, and local image references in reading order.

Use this shape:

```md
# Page title

Source: https://example.com/article
Captured: 2026-06-04

## Source Notes

- Publisher: Example
- Date: 2026-06-04
- Selected content: article/main content
- Capture notes: brief reliability notes when useful

## Content

Article paragraph...

![Image caption or nearby text](images/image-01.jpg)

Image source: https://example.com/original-image.jpg
Caption: Original caption when available.

Article continues...
```

## Images

Save original webpage images referenced by `source.md` under `images/`.

Name images predictably:

```text
images/image-01.jpg
images/image-02.png
```

Put enough context around each image in `source.md` for a later agent to understand why the image belongs there: nearby heading, paragraph, caption, chart title, diagram label, and original image URL.

When the page has no正文 images, keep `images/` empty and record that in `source.md`.
