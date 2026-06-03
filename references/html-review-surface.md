# HTML Review Surface

This reference defines the temporary human-review HTML page used during source understanding. It is a Chinese-first research report for human review, not an internal audit dump and not the downstream PPT Content Brief.

Use it when the source-understanding stage needs more than a compact chat summary: papers, technical news, product announcements, repository analysis, incident reports, benchmarks, or mixed source packages.

Load `references/html-review-data-model.md`, `references/html-review-report-kit.md`, and `references/html-review-pattern-library.md` together with this file. This file defines the content standard and outline; the data model defines the staging contract for extracted facts, the report kit defines reusable Tufte-style report blocks and preview behavior, and the pattern library contains additional repo-local visual, chart, evidence-pair, and citation patterns. Do not depend on external skill source at runtime.

## Purpose

The page must help a human quickly judge whether the agent understands the technical issue, the evidence, the competitive context, the method, the results, and the boundaries. It should read like a polished technical report that a decision maker would willingly open, not like a scratchpad.

It should answer:

- What problem is being discussed?
- What changed, was proposed, or was discovered?
- Why does it matter to the target reader?
- What evidence supports it?
- What is uncertain, limited, or contested?
- What follow-up research or deck direction should happen next?

## Research Autonomy Standard

The outline is a floor, not a form to mechanically fill. The agent must behave like a researcher preparing a useful briefing: decide what extra context, comparisons, figures, definitions, timelines, diagrams, and evidence are needed for this topic to become understandable and decision-ready.

Requirements:

- Do not merely follow the required outline section by section. Use the outline to ensure coverage, then add the topic-specific material that the reader would naturally need.
- Expand beyond the provided source when the source alone is too narrow to explain the problem, prior art, market/technical context, or implications. Use primary or high-quality supplemental sources where possible.
- Add definitions, background diagrams, method maps, timelines, benchmark context, glossary notes, or architecture sketches when they reduce reader confusion.
- Ask what a skeptical reader would challenge, then proactively answer the top objections with evidence, boundaries, or open questions.
- Ask what an expert reader would expect to see, then include the missing comparison, metric, baseline, caveat, or related method when it matters.
- Prefer self-directed synthesis over template compliance: if a section would be thin, combine it with a stronger section and create a more useful topic-specific section instead.
- The final page should feel authored: it should have a clear point of view, selected evidence, and a deliberate reading path, not equal-weight notes under every heading.

Reject the report if it feels like the agent filled headings without discovering or explaining anything the user did not already hand it.

## Report-Writing Standard

The visible page body must be Chinese-first and report-like.

Requirements:

- Use Chinese section titles and Chinese narrative by default. Preserve English only for method names, model names, datasets, metrics, commands, URLs, and source titles.
- Lead with a decision-grade conclusion, not an audit label. Prefer language like `这篇论文值得进入下一轮 serving 实验，但不能直接作为上线结论` over `当前理解` or `证据状态`.
- Make the main body read as a coherent report: thesis, context, comparison, mechanism, evidence, risk, next decision. Avoid raw work-log language.
- Do not expose internal labels in visible prose: `paper evidence`, `inference`, `needs_verification`, `source-original`, `agent-diagram`, `agent-chart`, `source-derived`, `审计`, `证据状态`, `claim/evidence`, `locator`, or `QA`.
- Do not put bracket citations after every sentence in the main body. Use a small superscript-style citation marker or concise footnote marker where needed, then put full locator details in the references section.
- Do not paste dense citation chains such as `[S1][F4][T2][T4][T5]` into paragraphs. When several sources support one sentence, cite the most important 1-2 markers and list the rest in the reference entry.
- Keep citations visually quiet: smaller text, superscript, or footnote-style links are acceptable. They must support auditability without interrupting reading.
- Every visible citation/index marker must be clickable. Clicking a marker in the report body must jump to the matching reference entry. Each reference entry should include a backlink to the first or nearest referring paragraph.
- Move internal evidence classification to a hidden/details section, appendix, or `research_audit.md`; it must not dominate the report.
- Treat the required outline as the hidden logic job of each section, not as the visible heading. Visible report headings should be claim-like conclusions, not topic labels. For example, use `R-CLA 值得进入受控 serving 实验` instead of `结论先行`, `KV cache 已从计算优化问题变成容量约束` instead of `问题为什么重要`, and `R-CLA 的差异在训练期鲁棒性，而不是又一种 token pruning` instead of `已有做法与缺口`.
- The side navigation is allowed to use fixed logical labels because it serves wayfinding, not persuasion. A good default navigation set is: `结论先行` / `问题为什么重要` / `已有做法与缺口` / `关键机制` / `实验信号与边界` / `下一步验证` / `参考资料`.
- The in-body section heading serves persuasion and must communicate the section's conclusion. If space is tight, pair the fixed navigation label with a claim-like in-body heading rather than reusing the navigation label as the heading.
- Avoid English headings such as `Executive Abstract`, `Problem Domain`, `References` unless the source or user explicitly requires English.
- The first viewport should feel like an executive summary, not a chat transcript or intermediate reasoning dump.

Bad visible copy:

```text
1. Executive Abstract
当前理解：这篇 paper 把 KV cache 优化从...
证据状态：paper evidence / inference / needs_verification
[S1][F4][T2][T4][T5]
```

Better visible copy:

```text
R-CLA 值得进入下一轮 serving 实验，但还不是上线结论
R-CLA 值得进入下一轮 serving 实验：它把 KV cache 优化从“删哪些 token”扩展到“哪些层可以共享 KV”。论文中的 Table 2/4/5 同时给出质量稳定性、缓存降幅和 batch capacity 信号，但这些结果仍需要在本地 backend 上复测。¹
```

## Required Outline

Use this outline as the default narrative spine. These names describe the job of each section; do not mechanically use them as visible headings. Write the actual headings in Chinese, adapted to the topic, and make them claim-like conclusions whenever possible. Keep the underlying jobs.

### 1. 结论先行

Open with a crisp claim: the current problem, what the source or actor did, what problem it addresses, and what effect or tradeoff is supported by evidence.

Requirements:

- State the core conclusion in the first viewport.
- Include the strongest concrete evidence available: metric, benchmark, date, adoption signal, incident number, cost/runtime/token number, or source figure/table.
- Separate confirmed facts from inference.
- Make the reader want to continue, but do not overclaim.

### 2. 问题为什么重要

Explain the problem space before explaining the proposed solution.

Requirements:

- Define the system, workflow, user, or market context.
- Explain why the problem is hard now.
- Identify the constraints that matter: latency, cost, accuracy, reliability, security, regulation, developer experience, deployment, interoperability, or business impact.
- Use one explanatory diagram if the domain has multiple actors, layers, or flows.

### 3. 已有做法与缺口

Show how similar problems are currently handled.

Requirements:

- Compare 3-5 relevant prior methods, products, research lines, standards, or industry practices. If fewer than 3 truly relevant alternatives exist, explain why in the report.
- Use supplemental research when the provided source is too narrow.
- Explain what each alternative optimizes for, where it struggles, and why it is or is not a fair comparison to the current source.
- For each comparison object, provide an abstract-style mini-summary with: `一句话定位`, `核心机制`, `主要证据或代表结果`, `适用边界`, and `与本文/本对象的关键差异`.
- Each comparison object must include at least one visual summary, not merely share one visual for the entire section. Good options: source figure, simplified mechanism diagram, tiny flow, axis marker in a method map, evidence card, sparkline/bar, or compact mini-table.
- Include one synthesis visual for the section after the mini-briefs: comparison matrix, method map, layer stack, quadrant, small-multiple cards, timeline, or tradeoff chart. The visual must help the reader compare methods, not merely decorate the page.
- Prefer a structured comparison over a long prose list. A good default is 3-5 method cards, each with its own mini visual, plus one matrix that compares optimization axis, required model change, serving-time impact, evidence strength, and deployment risk.
- Do not treat a quick web search as sufficient. For each selected alternative, use a primary or high-quality source when available, and cite it in the references section.
- State selection criteria: why these 3-5 objects are the right comparison set for the target reader.
- Analyze tradeoffs, not just capabilities. For every alternative, name what it buys, what it costs, what deployment assumption it makes, and which user/serving scenario would make it attractive.
- Explicitly connect the comparison back to the current source: after every mini-brief, state whether the current source is complementary, substitutive, orthogonal, or weaker/stronger on a specific axis.

Minimum mini-brief shape:

```text
方法名 / 产品名 / 研究线
一句话定位：它用什么方式解决什么问题。
图解摘要：1 个小图、源图、流程、矩阵标记或证据卡。
核心机制：关键技术动作，不超过 3 句。
主要证据：1-2 个代表性指标、发现、产品事实或标准条款。
适用边界：什么时候有效，什么时候风险变高。
与本文差异：优化轴、代价、部署条件、证据强度或组合关系。
```

Depth gate:

- A comparison object is underdeveloped if it has only a name, a one-sentence description, or a generic "improves performance" claim.
- A comparison object is underdeveloped if it has no primary/high-quality source, no mechanism explanation, no evidence, or no boundary.
- A comparison object is underdeveloped if the reader cannot tell why it was selected instead of another adjacent method.

### 4. 关键机制

Explain the source's method, product move, architecture, or core technical idea.

Requirements:

- Name the key mechanism in plain language.
- Show how the mechanism works with a diagram when relationships matter.
- Identify which part is genuinely new, which part is borrowed or standard, and which part is an implementation detail.
- Keep source-derived architecture separate from agent-inferred simplification.

### 5. 实验信号与边界

Present what worked, what did not, and where the evidence stops.

Requirements:

- Show benefits with source-grounded numbers where available.
- Show constraints and downsides with the same prominence as benefits.
- Use Pareto-style visuals when the evidence has competing axes such as accuracy vs. cost, quality vs. latency, throughput vs. memory, or capability vs. complexity.
- If Pareto/frontier language is used, define the axes and cite the data behind each plotted point.
- Weak or missing evidence must be stated in reader-facing Chinese, such as `仍需本地验证` or `论文没有覆盖这一点`; reserve the internal label `needs_verification` for the audit appendix or `research_audit.md`.

### 6. 下一步验证

End with what should be checked next.

Requirements:

- List open questions, missing evidence, and likely follow-up sources.
- Separate practical next steps from speculative research directions.
- State what user approval or correction is needed before moving to SCQA and page planning.

### 7. 参考资料

End with a reference section.

Requirements:

- Every factual claim in the page must map to a quiet citation marker such as a superscript number, footnote link, or compact marker. The marker must resolve to `[S1]`, `[F2]`, `[T1]`, or `[R3]` style entries in the reference section, but the main report should not look like a source-marker chain.
- `S` means textual/source document, `F` means figure/image, `T` means table/data, `R` means supplemental research.
- References must include enough locator detail for audit: source title, URL or local path, section/page/figure/table when available, access date for web sources, and whether the item is primary or supplemental.
- Local absolute paths are allowed in this review page and in `research_audit.md`; keep final `ppt_content_brief.md` cleaner.
- Implement citation navigation with stable HTML anchors:
  - Body marker: `<sup id="cite-ref-t4-1"><a href="#ref-t4">4</a></sup>`
  - Reference entry: `<li id="ref-t4">[T4] Table 4 ... <a href="#cite-ref-t4-1">↩</a></li>`
  - If one reference is cited multiple times, use unique body ids such as `cite-ref-t4-1`, `cite-ref-t4-2`; the reference backlink may return to the first occurrence or include multiple backlinks.
  - Source figures and table captions must use the same clickable citation pattern, not plain text labels.
  - Validate that all `href="#..."` targets exist and all reference ids are unique before showing the page.

## Evidence Rules

- Treat source materials as primary evidence; use external research to contextualize, not to overwrite source boundaries.
- For news or recent entities, verify with current web research and use concrete dates.
- Numeric claims, comparisons, rankings, dates, causal claims, and benchmark wins require citations.
- If a claim has no locator, either remove it from the visible report or phrase it as an open question in Chinese. Track the internal status as `needs_verification` only in the audit appendix or `research_audit.md`.
- Quote sparingly. Prefer paraphrase plus locator.
- Keep provenance for each visual in image metadata, captions, an appendix, or `research_audit.md`; do not show raw provenance labels in the main report body.
- Citation links are part of evidence quality. Broken anchors, non-clickable source markers, duplicate ids, or references with no reachable body marker count as report defects.

## Visual Rules

Use visuals only when they explain faster than prose.

The report should borrow from strong external report skills without becoming dependent on their full implementation. Keep our outline and evidence standards, and use the repo-local contracts in `references/html-review-data-model.md`, `references/html-review-report-kit.md`, and `references/html-review-pattern-library.md` for reusable report data, shell, narrative-data blocks, reconstructed charts, method cards, chart contracts, and citation anchor patterns.

Transferable visual habits:

- From SenseNova-style reports: use a calm long-form reading surface, clear side navigation, Chinese-first headings, source images placed near the relevant explanation, and a first viewport that reads like an executive technical brief.
- From Tufte-style reports: integrate narrative and data tightly; use a `report-data.json` staging model for extracted numbers and source assets; use chart-plus-aside, table-plus-interpretation, small multiples, compact evidence cards, and low-noise charts when they help the reader compare or decide.
- Do not require any single drawing tool. The agent may use source images, Mermaid, inline SVG, HTML/CSS diagrams, Chart.js, hand-authored tables, or other lightweight methods.
- Tool choice is secondary to auditability: reconstructed visuals must identify their source data, units, conditions, and relationship to the original evidence.
- If Chart.js or web fonts are loaded from a CDN, preview through `scripts/serve_html_review.py` so the report is tested in a browser-like localhost environment rather than only as a local file.

### Original Images

Use original source figures, table captures, screenshots, or product images when the user must inspect the actual evidence.

Requirements:

- Preserve figure/table labels when possible.
- Add a short Chinese caption explaining what the user should notice.
- Do not redraw source evidence as if it were original data.
- If cropping or annotating, keep a path to the original image and label the derivative in metadata or audit notes.

### Explanatory Diagrams

Use explanatory architecture, mechanism, flow, sequence, layer, quadrant, nested, tree, pyramid, or swimlane diagrams when relationships matter.

Requirements:

- Choose one dominant diagram grammar. Do not hybridize multiple diagram types in one figure.
- Keep diagrams sparse enough to inspect: usually 4-9 nodes; split if larger.
- Use accent on 1-2 focal elements only.
- Diagrams may simplify relationships, but the audit notes must record whether the diagram is source-derived or agent-interpreted. The visible caption should explain the idea in reader language.

### Professional Data Charts

Use professional quantitative charts when the data can be traced to sources. Borrow Tufte-style discipline: high data-ink ratio, few colors, clear units, minimal decoration, and a caption that states the takeaway.

Good fits:

- Pareto/frontier plots
- accuracy vs. cost / latency / memory charts
- benchmark comparison bars
- ablation curves
- timeline charts
- heatmaps or matrices

Requirements:

- Store the chart data table or extraction note near the output artifact.
- Label axes with units and conditions.
- Do not chart values copied from memory; cite each data source.
- When reconstructing a chart from a source table or figure, pair it with the original evidence or a direct reference so the reader can audit the transformation.
- Use any lightweight implementation that fits the artifact: inline SVG, Chart.js, HTML/CSS charts, or tables. Avoid heavy dependencies unless the user explicitly approves them.

## Quality Gate

Before showing the page to the user, check:

- The first viewport states the core conclusion and strongest evidence in Chinese.
- Side navigation may use fixed logical outline labels for wayfinding. In-body section headings are not merely the outline labels. They should state the section's conclusion or decision implication.
- The report contains autonomous research value beyond the user's provided outline: at least one useful comparison set, explanatory frame, background diagram, decision matrix, timeline, skeptical objection answer, or non-obvious synthesis.
- No main-body heading is left in English unless intentionally preserved.
- The main body does not contain raw internal labels such as `evidence status`, `paper evidence`, `inference`, `needs_verification`, `source-original`, `agent-chart`, or `QA`.
- Citation markers are visually quiet and do not appear as long bracket chains.
- Citation/index markers are clickable and jump to `参考资料`; reference entries include backlinks.
- All HTML anchor ids used by citations are unique, and every `href="#id"` points to an existing element.
- The problem domain is understandable without reading the original source first.
- Alternatives are compared, not merely named.
- The method/mechanism section has an explanatory visual when relationships matter.
- Results include tradeoffs, limitations, and weak evidence.
- Every factual claim maps to a citation or to an open question in Chinese.
- The references section is complete enough to audit.
- The page asks one clear approval/correction question.

## Rejection Triggers

Revise before showing the report if any of these appear in the visible main body:

- English default section headings such as `Executive Abstract`, `Problem Domain`, `Current State`, or `References` when the user expects Chinese.
- Mechanical outline headings used as in-body titles, such as `结论先行`, `问题为什么重要`, `已有做法与缺口`, `关键机制`, `实验信号与边界`, or `下一步验证`, when they appear without a topic-specific claim. These labels are acceptable in side navigation.
- Work-log phrases such as `当前理解`, `我现在的判断`, `证据状态`, `source understanding`, `approval bundle`, `QA passed`, or `落盘`.
- Raw evidence labels such as `paper evidence`, `source`, `inference`, `needs_verification`, `source-original`, `source-cropped`, `agent-diagram`, `agent-chart`.
- Dense bracket citation chains with three or more markers in a row.
- Plain, non-clickable citation markers such as `[S1]` or `[T4]` in visible paragraphs or figure captions.
- Broken reference navigation: citation links that do nothing, links that jump to the wrong reference, missing reference ids, duplicate ids, or references with no backlink.
- Paragraphs that mix Chinese and avoidable English glue words when a natural Chinese phrase exists.
- A first viewport that begins with audit process rather than the topic's conclusion and strongest evidence.
- Visual captions that describe provenance instead of telling the reader what to notice.
- Mechanical outline compliance: every required heading exists, but the content only paraphrases the source, repeats the user's prompt, or lacks topic-specific expansion.
- No autonomous synthesis: the report does not add a comparison set, decision frame, background explanation, expert caveat, skeptical objection answer, or other non-obvious research value.

If any trigger is needed for auditability, move it to `research_audit.md`, a `<details>` audit appendix, HTML comments, or structured metadata outside the visible report flow.
