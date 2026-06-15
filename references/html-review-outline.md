# HTML Review Outline

Use this outline as the hidden narrative spine for source understanding. The
visible body headings should be topic-specific conclusions, not these fixed
labels. Fixed labels are acceptable in side navigation.

## 1. 结论先行

Open with the current problem, what the source or actor did, what it addresses,
and what effect or tradeoff is supported.

Requirements:

- State the core conclusion in the first viewport.
- Include the strongest concrete evidence available.
- Separate confirmed facts from inference.
- Do not overclaim.

## 2. 问题为什么重要

Explain the problem space before the solution.

Requirements:

- Define the system, workflow, user, or market context.
- Explain why the problem is hard now.
- Identify constraints such as latency, cost, accuracy, reliability, security,
  regulation, developer experience, deployment, or interoperability.
- Use an explanatory diagram when the domain has multiple actors or layers.

## 3. 已有做法与缺口

Compare relevant prior methods, products, research lines, standards, or
industry practices.

Requirements:

- Compare 3-5 relevant objects when available.
- Explain selection criteria.
- For each object, cover positioning, mechanism, representative evidence,
  boundary, and difference from the current source.
- Give each comparison object its own source basis.
- Prefer a structured comparison over a long prose list.
- Use one synthesis visual such as a matrix, method map, timeline, or tradeoff
  chart when it helps.

A comparison is underdeveloped if it has only a name, no source, no mechanism,
no evidence, no boundary, or no reason for selection.

## 4. 关键机制

Explain the source's method, product move, architecture, or core idea.

Requirements:

- Name the key mechanism in plain language.
- Show how it works when relationships matter.
- Identify what is new, borrowed, standard, or implementation detail.
- Keep source-derived architecture separate from agent simplification.

## 5. 实验信号与边界

Present what worked, what did not, and where evidence stops.

Requirements:

- Show benefits with source-grounded numbers when available.
- Show constraints and downsides with similar prominence.
- Use frontier or Pareto visuals only when axes and data are traceable.
- State weak or missing evidence in reader-facing Chinese, such as
  `仍需本地验证`.

## 6. 下一步验证

End with what should be checked next.

Requirements:

- List open questions and missing evidence.
- Separate practical next steps from speculative research.
- State what approval or correction is needed before SCQA and page planning.

## 7. 参考资料

End with a reference section.

Requirements:

- Every factual claim maps to a quiet clickable citation or an open question.
- Use `S` for source text, `F` for figure or image, `T` for table or data, and
  `R` for supplemental research.
- Include enough locator detail for audit.
- For webpages, include original URL and local `web-article-capture` source package locator.
