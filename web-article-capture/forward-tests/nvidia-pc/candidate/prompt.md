# Candidate Prompt: Web Article Capture Forward Test

Use `web-article-capture/SKILL.md` to extract article/main webpage text and original inline images from the URLs in:

```text
candidate/input/urls.txt
```

Write one source package per page under:

```text
.tmp/forward-tests/web-article-capture/nvidia-pc/<run-id>/
```

Also write a forward-test review page at:

```text
.tmp/forward-tests/web-article-capture/nvidia-pc/<run-id>/review.html
```

The review page is for human inspection during forward testing. Use one section per source with:

- page title and original webpage link;
- local images from the source package, shown as thumbnails with captions or nearby text;
-正文 excerpt from `source.md`;
- links to the local source package and `source.md`.

Use a fresh run id and preserve prior outputs.

Final response should briefly state which source packages were generated, where `review.html` was written, and whether each `source.md` includes article/main text with the relevant original webpage images.

