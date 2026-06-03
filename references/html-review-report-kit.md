# HTML Review Report Kit

This file is the repo-local report kit for the temporary source-understanding HTML page. It is adapted for `ppt-deep-search`; do not depend on external skill source at runtime.

The kit borrows the strongest transferable parts of Tufte-style reports:

- one decision question drives the report
- claim first, visual second, caption third, boundary adjacent
- chart and narrative are physically close
- original evidence stays near reconstructed charts
- data lives in a small intermediate model before HTML
- the page uses low-noise typography and a small semantic palette

It is guidance and infrastructure, not a rigid template. Keep our Chinese-first outline and HIL approval gates.

## Default Dependencies

Keep the artifact lightweight:

- Required: plain HTML, CSS, JavaScript.
- Optional: Chart.js 4 through CDN for interactive charts.
- Optional: web fonts through CDN.
- No npm, no framework, no build step.
- If CDN scripts are used, test through `scripts/serve_html_review.py` instead of relying on `file://`.

If network/CDN access is undesirable, use inline SVG charts or HTML tables instead of Chart.js.

## Report Rhythm

A good source-understanding report usually follows this rhythm:

```text
title claim
subtitle decision context
status strip / KPI cards
opening narrative + side navigation

section:
  claim-like h2
  state-line: one sentence with the section's quantitative or decision takeaway
  chart/source image/table + aside interpretation
  original evidence + transformation note when a visual is reconstructed
  boundary or decision implication

references
```

Do not put two charts back-to-back. Insert prose, an evidence table, source image, or boundary note between them.

## CSS Tokens

Use these as the default editorial vocabulary when the report has no existing style:

```css
:root {
  --ink: #1a1a1a;
  --ink-light: #555;
  --ink-muted: #888;
  --bg: #fffff8;
  --paper: #ffffff;
  --bg-aside: #f8f4ea;
  --rule: #d8d2c4;
  --accent: #9f2f24;
  --positive: #2a7a5a;
  --warning: #c89000;
  --risk: #a02a2a;
  --blue: rgba(42,80,140,0.72);
}
body {
  margin: 0;
  color: var(--ink);
  background: var(--bg);
  font-family: Georgia, "Noto Serif SC", "Songti SC", "SimSun", serif;
  line-height: 1.68;
}
.mono, table td.number, .status-value {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-variant-numeric: tabular-nums;
}
.report-wrap {
  max-width: 1180px;
  margin: 0 auto;
  padding: 40px 24px 72px;
}
.toc-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 190px;
  gap: 32px;
}
.toc {
  position: sticky;
  top: 24px;
  align-self: start;
  border-left: 1px solid var(--rule);
  padding-left: 18px;
  color: var(--ink-light);
  font-size: 14px;
}
@media (max-width: 860px) {
  .toc-layout { grid-template-columns: 1fr; }
  .toc { position: static; border-left: 0; padding-left: 0; }
}
```

## Status Strip

Use when the first viewport needs concrete proof quickly.

```html
<div class="status-strip">
  <div class="status-cell status-positive">
    <div class="status-label">8K KV cache</div>
    <div class="status-value">4x</div>
    <div class="status-note">1170 MB -> 293 MB</div>
  </div>
</div>
```

Rules:

- 2-4 cells.
- Each cell should have a number, condition, or binary outcome.
- Do not use vague cells such as `效果显著` without a measured context.

## Summary Card With Sparkline

Use when a KPI needs a small trend or shape indicator.

```html
<div class="summary-row">
  <div class="summary-card" style="--card-color: var(--positive)">
    <div class="summary-label">低 retention 质量</div>
    <div class="summary-number-row">
      <div class="summary-number">+78.7%</div>
      <svg class="spark-inline" id="spark-quality" width="72" height="22"></svg>
    </div>
    <div class="summary-detail">HotpotQA, 50% retention, Llama-3.1-8B</div>
  </div>
</div>
```

Rules:

- Use 2-4 cards.
- The big number must have a condition line.
- Use sparklines only when the shape is meaningful; otherwise use a plain KPI cell.

Suggested CSS:

```css
.summary-row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; margin: 28px 0; }
.summary-card { border-top: 3px solid var(--card-color, var(--rule)); border-bottom: 1px solid var(--rule); padding: 14px 0 16px; }
.summary-label { color: var(--ink-muted); font-size: 13px; }
.summary-number-row { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; }
.summary-number { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 28px; font-variant-numeric: tabular-nums; }
.summary-detail { color: var(--ink-light); font-size: 13px; line-height: 1.45; }
@media (max-width: 860px) { .summary-row { grid-template-columns: 1fr; } }
```

## State Line

Every major body section should begin with one concise conclusion sentence:

```html
<p class="state-line">g=4 在 8K 输入下把 KV cache 降到约 1/4，但生产 scheduler 收益仍需本地验证。</p>
```

Rules:

- Max one sentence.
- Prefer numbers, conditions, and decision implications.
- Do not write `本节介绍...`.

## Chart With Aside

Use this for reconstructed charts, source tables, compact matrices, or source figures.

```html
<div class="aside-container">
  <figure class="chart-panel">
    <canvas id="kvCacheChart" aria-label="KV cache by context length"></canvas>
    <figcaption>重构图：g=4 在各输入长度下都把 KV cache 降到约 1/4。<sup id="cite-ref-t4-1"><a href="#ref-t4">4</a></sup></figcaption>
  </figure>
  <aside class="aside-note">
    <p class="aside-title">读图边界</p>
    <p><strong>口径：</strong>Qwen3-8B-like，单 80GB GPU，batch size 1。</p>
    <p><strong>含义：</strong>容量收益明确，但这还不是完整 serving backend 结论。</p>
  </aside>
</div>
```

Rules:

- The visual answers one question.
- The aside explains condition, interpretation, and boundary.
- Captions state the takeaway, not just provenance.
- Reconstructed visuals must cite the original data source.

## Data Table With Interpretation

Use when exact lookup matters more than shape, or when a chart needs the underlying rows visible.

```html
<div class="aside-container">
  <div class="table-wrapper">
    <table>
      <thead>
        <tr><th>输入长度</th><th>KV g=1</th><th>KV g=4</th><th>TTFT g=1/g=4</th></tr>
      </thead>
      <tbody>
        <tr class="highlight-row"><td>8K</td><td class="number">1170 MB</td><td class="number">293 MB</td><td class="number">297 / 286 ms</td></tr>
      </tbody>
    </table>
    <div class="caption">表格：保留原始数量级，避免读者只看趋势图而忽略条件。</div>
  </div>
  <aside class="aside-note">
    <p><strong>读表结论：</strong>8K 是最适合复测的首个工程点，因为容量、TTFT、throughput 都有对应数值。</p>
  </aside>
</div>
```

Rules:

- Wrap wide tables in `.table-wrapper`.
- Number columns use tabular figures.
- Highlight at most 1-2 rows; the highlight should correspond to the report's decision point.

Suggested CSS:

```css
.table-wrapper { overflow-x: auto; margin: 18px 0; }
table { width: 100%; border-collapse: collapse; }
th { color: var(--ink-muted); font-weight: 400; font-size: 13px; border-bottom: 1px solid var(--rule); text-align: right; }
th:first-child, td:first-child { text-align: left; font-family: inherit; }
td { border-bottom: 1px solid rgba(216,210,196,.7); padding: 9px 8px; text-align: right; }
td.number { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-variant-numeric: tabular-nums; }
.highlight-row { background: rgba(42,122,90,.08); }
```

## Original Evidence Pair

When the chart is reconstructed, keep the source evidence nearby:

```html
<div class="evidence-row">
  <figure>
    <img src="assets/table_004.png" alt="原始 Table 4">
    <figcaption>原始证据：Table 4 给出用于重构的 KV cache、TTFT 与 throughput 数值。<sup id="cite-ref-t4-2"><a href="#ref-t4">4</a></sup></figcaption>
  </figure>
  <div class="transform-note">
    提取字段：input length、KV cache MB、TTFT ms、throughput tok/s；派生字段：g1/g4 KV cache ratio。
  </div>
</div>
```

Rules:

- Never let a rebuilt chart impersonate an original figure.
- Keep extraction notes in `report-data.json` and `research_audit.md`; show only the reader-useful transformation note in HTML.

## Method Mini-Brief

Use for the prior-art/current-status section.

```html
<article class="method-card">
  <h3>H2O / token eviction</h3>
  <div class="method-visual" aria-label="token axis visual">
    <span class="axis-chip">token axis</span>
    <span class="axis-chip muted">layer axis unchanged</span>
  </div>
  <p><strong>定位：</strong>在固定 KV 预算下保留 heavy hitters 和 recent tokens。</p>
  <p><strong>机制：</strong>按 token 重要性做缓存保留/淘汰，而不是减少每层都存 KV 的结构。</p>
  <p><strong>边界：</strong>它和 depth-wise sharing 原则上正交，但组合后的质量损失需要实测。</p>
</article>
```

Rules:

- Use 3-5 cards when the domain allows.
- Each card needs one tiny visual summary: axis chip, mini flow, sparkline, evidence badge, source image, or compact mini-table.
- Follow cards with one synthesis visual: comparison matrix, method map, timeline, tradeoff chart, or small multiples.

## Matrix, Heatmap, And Strip Chart

Use these instead of crowded charts when comparison density is high.

### Comparison Matrix

```html
<table class="comparison-matrix">
  <thead><tr><th>路线</th><th>优化轴</th><th>模型改造</th><th>serving 风险</th><th>与本文关系</th></tr></thead>
  <tbody>
    <tr><td>KV quantization</td><td>bit</td><td>低</td><td>中</td><td>正交</td></tr>
    <tr><td>R-CLA</td><td>layer</td><td>高</td><td>待验证</td><td>当前对象</td></tr>
  </tbody>
</table>
```

### Heatmap

Good for strength/coverage matrices: method x evidence, feature x source, risk x scenario.

```html
<div class="heatmap-grid" style="--cols: 4">
  <div class="heatmap-cell head">方法</div>
  <div class="heatmap-cell head">质量</div>
  <div class="heatmap-cell head">容量</div>
  <div class="heatmap-cell head">延迟</div>
  <div class="heatmap-cell">R-CLA</div>
  <div class="heatmap-cell good">强</div>
  <div class="heatmap-cell good">强</div>
  <div class="heatmap-cell warn">弱</div>
</div>
```

### Strip Chart

Good for ranked rows or periodic observations when exact labels matter.

```html
<div class="strip-chart">
  <div class="strip-row">
    <span class="strip-label">8K</span>
    <span class="strip-value">1170 -> 293 MB</span>
    <span class="strip-bar"><span style="width:75%"></span></span>
    <span class="strip-note">约 4x</span>
  </div>
</div>
```

Rules:

- Use matrices when the reader compares categories across shared axes.
- Use heatmaps only when color intensity encodes a real ordinal or numeric scale.
- Use strip charts for sparse, labeled rows; avoid full bar charts when the labels are the story.

## Decision Register

Use near the end when the report must tell the human what to approve next.

```html
<table class="decision-register">
  <thead><tr><th>门槛</th><th>当前信号</th><th>下一步验证</th><th>状态</th></tr></thead>
  <tbody>
    <tr>
      <td>质量</td>
      <td>低 retention QA 结果更稳</td>
      <td>复测目标任务集</td>
      <td class="status-warning">待验证</td>
    </tr>
  </tbody>
</table>
```

Rules:

- Good for `下一步验证`.
- State the gate, current evidence, missing proof, and decision status.

## Chart.js Defaults

If using Chart.js, set defaults before constructing charts:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<script>
Chart.defaults.font.family = 'Georgia, "Noto Serif SC", serif';
Chart.defaults.font.size = 13;
Chart.defaults.color = '#555';
Chart.defaults.plugins.legend.labels.usePointStyle = false;
Chart.defaults.plugins.legend.labels.boxWidth = 8;
Chart.defaults.plugins.legend.labels.boxHeight = 8;
Chart.defaults.plugins.legend.labels.borderRadius = 4;
Chart.defaults.plugins.tooltip.backgroundColor = '#1a1a1a';
Chart.defaults.plugins.tooltip.cornerRadius = 2;
Chart.defaults.scale.grid.color = '#eee';
</script>
```

Anti-patterns:

- Do not use pie, donut, or 3D charts.
- Do not use more than 3 semantic colors in a chart.
- Do not use dual axes unless both axes are essential to the claim and labeled clearly.
- Do not use filled multi-line charts when lines overlap heavily.

## Inline SVG Sparkline

Use for small trend evidence inside cards or tables without bringing in Chart.js:

```html
<svg class="spark-inline" id="spark-cache" width="64" height="18"></svg>
<script>
function drawSparkline(svgId, values, color) {
  const svg = document.getElementById(svgId);
  if (!svg || values.length < 2) return;
  const w = Number(svg.getAttribute('width'));
  const h = Number(svg.getAttribute('height'));
  const pad = 2;
  const max = Math.max(...values);
  const min = Math.min(...values);
  const range = max - min || 1;
  const step = (w - pad * 2) / (values.length - 1);
  const points = values.map((v, i) => {
    const x = pad + i * step;
    const y = h - pad - ((v - min) / range) * (h - pad * 2);
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  });
  svg.innerHTML = `<polyline points="${points.join(' ')}" fill="none" stroke="${color}" stroke-width="1.3" stroke-linejoin="round"/><circle cx="${points.at(-1).split(',')[0]}" cy="${points.at(-1).split(',')[1]}" r="2" fill="${color}"/>`;
}
</script>
```

## Scroll Reveal

Subtle reveal is allowed for report readability, but it must not hide content or become a visual trick.

```html
<script>
function installReveal() {
  const targets = document.querySelectorAll('.aside-container, .summary-card, figure, .flyout');
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    targets.forEach(el => el.classList.add('visible'));
    return;
  }
  targets.forEach(el => el.classList.add('reveal'));
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  targets.forEach(el => observer.observe(el));
}
installReveal();
</script>
```

Suggested CSS:

```css
.reveal { opacity: 0; transform: translateY(14px); transition: opacity .45s ease, transform .45s ease; }
.reveal.visible { opacity: 1; transform: translateY(0); }
@media (prefers-reduced-motion: reduce) { .reveal { opacity: 1; transform: none; transition: none; } }
```

## Self-Check

Before showing the report:

- Is there a `report-data.json` when the report is numeric or visual-heavy?
- Does the HTML visibly consume the important `report-data.json` objects, such as through `data-report-*` attributes, matching chart ids, or a clear extraction note?
- Does the title answer one decision question?
- Does every chart have a chart contract, units, condition, and claim caption?
- Is every reconstructed chart paired with original evidence or a direct reference?
- Are method cards developed enough to explain mechanism, evidence, boundary, and relationship?
- Are citations quiet, clickable, and complete?
- Are tables/matrices used when exact comparison matters more than chart shape?
- Are scroll effects disabled or harmless under reduced motion?
- Does the first viewport include the next decision or minimum validation matrix when the report is for an engineering decision?
- Does the report stay a source-understanding surface rather than becoming the downstream PPT outline?
- Does the report still feel authored rather than assembled from blocks?
