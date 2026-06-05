# Candidate Prompt: vLLM KV Cache Serving Web Capture

Use `web-article-capture/SKILL.md` to extract article/main webpage text and original inline images from the URLs in:

```text
candidate/input/urls.txt
```

Write one source package per page under:

```text
.tmp/forward-tests/web-article-capture/vllm-kv-cache-serving/<run-id>/
```

Also write a forward-test review page at:

```text
.tmp/forward-tests/web-article-capture/vllm-kv-cache-serving/<run-id>/review.html
```

The review page is for human inspection during forward testing. Use one section per source with original webpage link, local image thumbnails,正文 excerpt from `source.md`, and links to the local source package.

Use a fresh run id and preserve prior outputs.

Final response should briefly state which source packages were generated, where `review.html` was written, and whether each `source.md` includes article/main text with relevant original webpage images.

