# Judge Rubric: NVIDIA Dynamo Disaggregated Serving Web Capture

Score each dimension 0-3.

- Browser Discipline: renders pages through Codex in-app Browser / Browser plugin.
- Browser Recovery: retries page-specific navigation timeouts in a fresh tab, scrolls lazy-loaded正文 figures into view before collecting image URLs, and records the exact blocked stage when Browser access remains blocked.
- Content Selection: captures article/main正文 from NVIDIA Dynamo docs and technical blog sources, excluding page chrome.
- Markdown Package: writes useful `source.md` for each page, with metadata, readable正文, and image references placed near relevant text.
- Image Package: downloads original正文 images, charts, diagrams, and figure/caption pairs into `images/`, then references them from `source.md` near the related text.
- Source Notes: records concise capture notes inside `source.md` when source boundaries, missing media, versioned docs, or reliability details matter.
- Completeness Judgment: final notes say which packages were generated and whether the text/image pairing is complete.
- QA Discipline: runs `web-article-capture/scripts/validate_capture_package.py <run-output> --require-images when-referenced` or records why it could not.
- Research-Scale Stability: one child captures the full 10-ish page source set into one package per page with consistent `source.md` + `images/` shape.
- Forward Review Page: writes `<run-output>/review.html` with one section per source, original links, local image thumbnails,正文 excerpts, and package links.

Blocking findings:

- A package is missing `source.md` or `images/`.
- `source.md` image references point to missing local files.
- The captured正文 is mostly page chrome rather than article/main content.
- Important正文 figures or charts are missing while sidebar/recommendation images are kept.
- Assigned URLs are missing, or multiple pages are mixed into one source package.
- Browser navigation timeout leads directly to fallback without a focused fresh-tab retry.
- `review.html` is missing or does not show the source text/image pairing for human inspection.


