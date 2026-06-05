# Main Agent Prompt: Run vLLM KV Cache Serving Web Capture Forward Test

Orchestrate one isolated child-agent run. Keep page extraction inside the child run.

Dispatch only:

```text
请使用仓库 `web-article-capture/SKILL.md` 完成网页图文抓取 forward test：

- Candidate Prompt: web-article-capture/forward-tests/vllm-kv-cache-serving/candidate/prompt.md
- Candidate Input: web-article-capture/forward-tests/vllm-kv-cache-serving/candidate/input/
- Output: .tmp/forward-tests/web-article-capture/vllm-kv-cache-serving/<run-id>/

你已经是 candidate child；不要再 spawn 子 agent。
```

After completion, inspect the output and run:

```powershell
python web-article-capture/scripts/validate_capture_package.py <run-output> --require-images when-referenced
```

Open or inspect `<run-output>/review.html` for a human-readable sampling pass: original links, local images, and正文 excerpts should line up for every source.

Write `judgment.md` under the run output directory. Include whether one child agent can reliably capture the roughly 10-source webpage set expected for deep research, and whether `review.html` made the result easy to inspect.

