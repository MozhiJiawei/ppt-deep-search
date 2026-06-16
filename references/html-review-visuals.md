# HTML Review Visuals

Use visuals only when they explain faster than prose. Tool choice is secondary
to auditability.

## Original Images

Use original source figures, table captures, product images, or report-specific
page captures
when the reader must inspect the actual evidence.

Requirements:

- Preserve figure and table labels when possible.
- Add a short Chinese caption explaining what to notice.
- Do not redraw source evidence as if it were original data.
- If cropping or annotating, keep a path to the original image in metadata or
  audit notes.
- For webpage sources, display copied or derived local assets that trace back to
  images in a `web-article-capture` source package.

## Explanatory Diagrams

Use architecture, mechanism, flow, sequence, layer, quadrant, tree, pyramid, or
swimlane diagrams when relationships matter.

Requirements:

- Choose one dominant diagram grammar.
- Keep diagrams inspectable, usually 4-9 nodes.
- Accent only 1-2 focal elements.
- Record whether the diagram is source-derived or agent-interpreted.
- Make the visible caption explain the idea in reader language.

## Data Charts

Use quantitative charts only when data is traceable.

Good fits:

- frontier or Pareto plots;
- accuracy vs cost, latency, or memory charts;
- benchmark comparison bars;
- ablation curves;
- timelines;
- heatmaps or matrices.

Requirements:

- Store the data table or extraction note near the output artifact.
- Label axes with units and conditions.
- Cite each data source.
- Pair reconstructed charts with original evidence or direct references.
- Use inline SVG, Chart.js, HTML/CSS charts, or tables as appropriate.

## Transferable Habits

From long-form technical reports:

- use a calm reading surface;
- keep source images close to related claims;
- start with an executive technical brief;
- integrate narrative and data tightly;
- use chart-plus-aside, table-plus-interpretation, small multiples, evidence
  cards, and low-noise charts when useful.

If Chart.js or web fonts are loaded from a CDN, preview through:

```powershell
python scripts/serve_html_review.py <workspace-root>/review
```
