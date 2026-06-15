# HTML Review Pattern Library

Scope map:

- Owns optional HTML review patterns such as report shells, narrative-data pairs, evidence pairs, reconstructed charts, method cards, and citation anchors.
- Does not own report-level purpose; use `html-review-surface.md`.
- Does not own data staging; use `html-review-data-model.md`.
- Stable boilerplate may move to assets or scripts when it becomes deterministic.

This library contains repo-local patterns for the temporary source-understanding HTML report. It borrows proven report habits from prior experiments, but the patterns here are owned by this skill and do not require external skill code.

Use this file together with `references/html-review-surface.md`, `references/html-review-expression.md`, `references/html-review-data-model.md`, and `references/html-review-report-kit.md`. The surface file defines the report standard and outline; the expression contract defines
reader-facing visible prose; the data model and report kit define the preferred Tufte-style staging and block infrastructure; this file defines additional reusable presentation patterns that help the agent meet that standard.

## Report Shell

Use a long-form technical report shell by default.

Required traits:

- Chinese-first visible text.
- Light gray page background and a white paper-like article surface.
- Left sticky navigation on desktop; navigation above content on mobile.
- Main content width wide enough for figures and tables, but not so wide that paragraphs become hard to read.
- First viewport contains the conclusion, strongest evidence, and why the reader should care.
- The visible prose follows `html-review-expression.md`: it serves the reader's next decision and keeps internal process outside the main reading flow.
- Side navigation can use fixed logical labels such as `结论先行`, `问题为什么重要`, `已有做法与缺口`, `关键机制`, `实验信号与边界`, `下一步验证`, and `参考资料`. In-body section headings state conclusions, not outline jobs; headings such as `问题为什么重要` should be rewritten into topic-specific claims such as `KV cache
  已从计算优化问题变成容量约束`.
- Tables, figures, charts, and source images sit near the paragraph that interprets them.
- Print mode removes navigation, progress UI, shadows, and decorative backgrounds.

Recommended local CSS tokens:

```css
:root {
  --bg: #f7f8fb;
  --paper: #ffffff;
  --ink: #1c2430;
  --muted: #667085;
  --line: #dbe2ea;
  --accent: #0f766e;
  --accent-2: #2563eb;
  --soft: #eef7f5;
  --warn: #c2410c;
  --risk: #b42318;
  --radius: 8px;
}
body {
  margin: 0;
  color: var(--ink);
  background: linear-gradient(180deg, #f3f7fa 0%, var(--bg) 360px, var(--bg) 100%);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  line-height: 1.75;
}
.review-layout {
  display: grid;
  grid-template-columns: minmax(220px, 280px) minmax(0, 1fr);
  gap: 28px;
  max-width: 1480px;
  margin: 0 auto;
  padding: 28px;
}
.review-toc {
  position: sticky;
  top: 20px;
  align-self: start;
  max-height: calc(100vh - 40px);
  overflow: auto;
  padding: 18px 16px;
  background: rgba(255,255,255,.88);
  border: 1px solid var(--line);
  border-radius: var(--radius);
}
.review-paper {
  min-width: 0;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
}
.review-article { padding: 46px min(6vw, 76px) 68px; }
@media (max-width: 1020px) {
  .review-layout { display: block; padding: 14px; }
  .review-toc { position: relative; top: 0; max-height: 280px; margin-bottom: 14px; }
  .review-article { padding: 28px 18px 42px; }
}
```

Do not paste this blindly if the generated HTML already has an equivalent shell. Use it as the local default style vocabulary.

## Narrative-Data Pair

Use this pattern when a chart, original table, source figure, or compact matrix needs interpretation.

```html
<section class="evidence-pair" id="result-memory">
  <div class="evidence-main">
    <!-- chart, source image, compact table, SVG, Mermaid, or HTML/CSS diagram -->
  </div>
  <aside class="evidence-aside">
    <p class="aside-kicker">实验信号</p>
    <p><strong>读图结论：</strong>一句话说明读者应该注意的差异、趋势或边界。</p>
    <p><strong>口径：</strong>写清楚模型、数据集、batch、输入长度、时间范围或其他条件。</p>
    <p><strong>决策含义：</strong>说明这张图如何影响下一步验证或 PPT 叙事。</p>
  </aside>
</section>
```

Recommended behavior:

- Left side carries the visual or table; right side carries interpretation.
- The aside is not an audit log. It should read like a report sidebar.
- The aside should satisfy the figure/table contract in `html-review-expression.md`: what to notice, what claim it supports, and what it does not prove.
- Every paragraph should earn its place: result, condition, caveat, or implication.
- On mobile, collapse to one column.

Suggested CSS:

```css
.evidence-pair {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(240px, 320px);
  gap: 28px;
  align-items: start;
  margin: 24px 0 30px;
}
.evidence-aside {
  border-left: 1px solid var(--line);
  padding-left: 18px;
  color: #475467;
  font-size: 14px;
}
.aside-kicker {
  margin: 0 0 8px;
  color: var(--muted);
  font-size: 12px;
  letter-spacing: .08em;
  text-transform: uppercase;
}
@media (max-width: 900px) {
  .evidence-pair { grid-template-columns: 1fr; }
  .evidence-aside { border-left: 0; padding-left: 0; }
}
```

## Reconstructed Chart Plus Original Evidence

When the agent redraws numbers from a source table, figure, benchmark, API response, or public dataset, present the reconstructed view and original evidence together.

Required parts:

1. Reconstructed visual: low-noise chart, compact SVG, small multiple, matrix, or table.
2. Original evidence: source figure/table screenshot, original table excerpt, link to source row, or reference entry.
3. Transformation note: one sentence explaining what was extracted or calculated.
4. Caption: one sentence stating what the reader should conclude.

Recommended shape:

```html
<div class="rebuild-block">
  <figure>
    <!-- reconstructed chart -->
    <figcaption>重构图：说明趋势、差异或权衡；标注单位和条件。<sup id="cite-ref-t4-1"><a href="#ref-t4">4</a></sup></figcaption>
  </figure>
  <figure>
    <img src="assets/source-table-4.png" alt="原始表格 4">
    <figcaption>原始证据：Table 4 给出用于重构的 KV cache、TTFT 与 throughput 数值。<sup id="cite-ref-t4-2"><a href="#ref-t4">4</a></sup></figcaption>
  </figure>
</div>
```

Rules:

- Do not let the reconstructed chart replace the original evidence.
- Do not imply a visual is an original figure when it was rebuilt by the agent.
- If a data point is calculated, preserve the formula or extraction note in `research_audit.md` and cite the source rows in the visible report.
- Prefer one reconstructed chart plus one original evidence block over a pile of redundant captures.
- For webpage evidence, pair the reconstructed or selected visual with an asset copied or derived from a `web-article-capture` source package, and keep the original webpage URL plus local package mapping in `report-data.json`. Do not use remote `<img src="https://...">` hotlinks in the report.

## Method Mini-Brief Card

Use this pattern for the `已有做法与缺口` section. Each compared method/product/research line needs enough substance to be useful.

Required fields:

- `一句话定位`
- `图解摘要`
- `核心机制`
- `代表证据`
- `适用边界`
- `与本文/本对象的关系`

Citation behavior:

- Put quiet clickable citations next to the specific fields they support, especially `核心机制`, `代表证据`, and `适用边界`.
- If a card needs a claim but the source is missing, pause drafting and fetch the source or rewrite the claim as an open question. Do not remove the claim merely to avoid a citation error.

Recommended shape:

```html
<article class="method-card">
  <h3>方法名</h3>
  <p class="method-position">一句话定位：它用什么方式解决什么问题。</p>
  <div class="method-visual">
    <!-- tiny flow, evidence badge, axis marker, source image, mini table, or SVG -->
  </div>
  <dl>
    <dt>核心机制</dt><dd>不超过三句，说明关键动作。</dd>
    <dt>代表证据</dt><dd>1-2 个指标、实验、产品事实、标准条款或来源结论。</dd>
    <dt>适用边界</dt><dd>什么时候有效，什么时候风险变高。</dd>
    <dt>与本文关系</dt><dd>互补、替代、正交或弱于/强于本文的具体轴。</dd>
  </dl>
</article>
```

Recommended behavior:

- Use 3-5 cards when the domain allows.
- Each card needs its own visual summary, even if small.
- After the cards, include one synthesis visual: comparison matrix, method map, timeline, tradeoff axis, or small-multiple table.

## Professional Chart Contract

Before drawing any quantitative chart, write the chart contract in scratch notes or artifact metadata.

When practical, store the chart contract in `review/report-data.json` under `charts[]` so the generated HTML, research audit, and later PPT brief share the same numbers.

```text
chart_id:
question: What question does this chart answer?
chart_type: bar | line | scatter | matrix | heatmap | small-multiple | table | other
source_data:
  - marker: [T4]
    locator: table/figure/url/row/page
    fields: input length, KV cache MB, throughput tok/s
derived_fields:
  - name: throughput uplift %
    formula: (g4_tok_s - g1_tok_s) / g1_tok_s
units: MB, ms, tok/s, %
conditions: model, hardware, batch size, context length, date
caption_takeaway:
known_limits:
```

Chart quality rules:

- Every axis needs a unit or explicit categorical meaning.
- Use at most 3 semantic colors in one chart.
- Avoid dual axes unless the two measures cannot share a scale and the caption explains the risk.
- Do not put two charts back to back without prose, table, or evidence between them.
- Prefer small multiples over crowded legends when comparing more than 3 series.
- If the data is sparse or exact lookup matters more than shape, use a table or matrix instead of a chart.
- If the chart is based on source evidence, pair it with original evidence or a clickable reference.

## Citation And Anchor Pattern

Use quiet clickable markers in visible prose and figure captions.

```html
<p id="p-cache-result">g=4 在 8K 输入下把 KV cache 从 1170 MB 降到 293 MB，同时 throughput 从 34.0 提升到 41.6 tok/s。<sup id="cite-ref-t4-1"><a href="#ref-t4">4</a></sup></p>

<ol class="references">
  <li id="ref-t4">[T4] Source title, Table 4, locator details. <a href="#cite-ref-t4-1">↩</a></li>
</ol>
```

Validation requirements:

- Every body marker `href="#ref-id"` has a matching reference id.
- Every reference id is unique.
- Every reference has at least one backlink to a referring paragraph, caption, or table.
- Avoid chains of three or more markers in visible prose.

## HTML Self-Check

Before showing the HTML report, inspect it for these structural signs:

- At least one side navigation or clear table of contents for long reports.
- Visible prose follows the reader-facing expression contract instead of exposing workflow narration.
- Side navigation uses stable logical labels; body headings are claim-like and topic-specific.
- At least one `evidence-pair` or equivalent narrative-data block when the report includes quantitative results.
- At least one original-evidence link, figure, table, captured source image, or reference near any reconstructed visual.
- Webpage references and displayed webpage images trace back to local `web-article-capture` source packages, with `report-data.json` mapping each cited URL/image to the package and report asset.
- The visible report does not expose raw data-model fields, QA status, or agent work-log labels as reader-facing prose.
- Citation anchors are clickable and not just bracket text.
- The `已有做法与缺口` section contains developed mini-briefs, not only a comparison table.
