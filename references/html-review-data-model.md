# HTML Review Data Model

Scope map:

- Owns the required `review/report-data.json` staging model.
- Defines source discovery, citations, assets, KPI, section, chart, comparison, and decision records.
- Defines supported block types, data rules, and output directory shape.
- Does not define visible prose; use `html-review-expression.md`.
- Does not define final PPT format; use `ppt-content-brief-format.md`.

This reference defines the intermediate data model for the temporary source-understanding HTML report.

Use it together with `references/html-review-surface.md` and `references/html-review-pattern-library.md`.

The goal is to make the HTML report data-first instead of hand-wavy. Before writing report HTML, normalize the most important facts, extracted numbers, source images, comparison objects, and chart contracts into:

```text
.tmp/ppt-deep-search/<task-name>/review/report-data.json
```

For forward tests with a custom output directory, place it under that run's `review/` directory.

This file is not a downstream PPT artifact. It is a staging model for producing a clearer HTML review and a more reliable `research_audit.md`.

## When To Create It

Create `report-data.json` for every source-understanding HTML review. Small text-only reports may use a minimal file, but they should not skip the artifact.

Populate richer fields when the report includes any of these:

- reconstructed charts from source tables, benchmarks, APIs, or captured visual material
- KPI strips or numeric summary cards
- method comparison cards
- original source figures/tables copied into `review/assets/`
- Pareto/frontier, tradeoff, heatmap, matrix, or small-multiple visuals
- more than two cited quantitative claims

## Required Shape

```json
{
  "meta": {
    "title": "Chinese decision-grade report title",
    "question": "The one decision question the report answers",
    "audience": "Target reader",
    "reader_lens": {
      "reader_role": "Who will inspect the report.",
      "reader_knows": "What they probably already understand.",
      "reader_cares_about": "What would make the source matter to them.",
      "reader_next_decision": "What they need to approve, reject, test, or clarify after reading."
    },
    "generated_at": "2026-06-03T00:00:00+08:00",
    "source_package": "local source package root or non-web source description",
    "source_discovery_path": "sources/source-discovery.md"
  },
  "source_discovery": {
    "primary_sources": [
      {
        "id": "primary-nvidia-news",
        "title": "NVIDIA official announcement",
        "url_or_path": "https://example.com/official",
        "why_it_matters": "Defines the official wording and product object.",
        "capture_status": "captured | planned | blocked"
      }
    ],
    "adjacent_route_sources": [
      {
        "id": "adjacent-copilot-pc",
        "title": "Adjacent product or method source",
        "url_or_path": "https://example.com/adjacent",
        "comparison_role": "Explains how a neighboring route differs on mechanism, evidence, or boundary.",
        "capture_status": "captured | planned | blocked"
      }
    ],
    "boundary_sources": [
      {
        "id": "boundary-availability",
        "title": "Availability or benchmark caveat source",
        "url_or_path": "https://example.com/boundary",
        "boundary_checked": "Release date, metric condition, security claim, procurement state, or other overclaim risk.",
        "capture_status": "captured | planned | blocked"
      }
    ],
    "citation_debt": [
      {
        "claim_or_comparison_need": "A useful claim that appeared while drafting but needs more support.",
        "needed_source_type": "official docs | paper | product page | benchmark | repository | standard | technical article",
        "resolution": "captured and cited | rewritten as boundary | left as open question",
        "linked_citations": ["r2"]
      }
    ]
  },
  "citations": [
    {
      "id": "t4",
      "marker": "T4",
      "kind": "table",
      "title": "Table 4: Inference efficiency",
      "locator": "paper Table 4 / local image path / URL section",
      "source_type": "primary",
      "url": null,
      "local_path": "D:/.../images/table_004.png"
    },
    {
      "id": "r1",
      "marker": "R1",
      "kind": "webpage",
      "title": "NVIDIA Blog article title",
      "locator": "official blog article body captured in source.md",
      "source_type": "primary",
      "url": "https://example.com/article",
      "local_path": "sources/web/nvidia-blog/source.md",
      "web_capture": {
        "package_path": "sources/web/nvidia-blog",
        "source_md": "sources/web/nvidia-blog/source.md",
        "images_dir": "sources/web/nvidia-blog/images",
        "captured_at": "2026-06-03T00:00:00+08:00"
      }
    }
  ],
  "assets": [
    {
      "id": "table_004",
      "role": "original_evidence",
      "path": "assets/table_004.png",
      "source_citation": "t4",
      "caption_takeaway": "The source table provides KV cache, TTFT, and throughput values used in the reconstructed chart."
    },
    {
      "id": "webimg_001",
      "role": "original_web_image",
      "path": "assets/webimg_001.png",
      "source_citation": "r1",
      "page_url": "https://example.com/article",
      "source_url": "https://example.com/uploads/source-image.png",
      "capture_method": "Codex in-app Browser / Browser plugin page asset download",
      "download_status": "ok",
      "content_type": "image/png",
      "bytes": 123456,
      "alt": "Original alt text when available",
      "caption": "Original figcaption when available",
      "nearby_text": "Heading or paragraph near the image in article order.",
      "inferred_meaning": "One Chinese sentence explaining what this image likely shows based on DOM context.",
      "meaning_confidence": "high | medium | low",
      "usage_policy": "original | summarize_rebuild | background_only | discard",
      "caption_takeaway": "Chinese report-facing takeaway if this image is used."
    }
  ],
  "kpis": [
    {
      "id": "kv-cache-8k",
      "label": "8K KV cache",
      "value": "4x",
      "status": "positive",
      "context": "g=4 reduces KV cache from 1170 MB to 293 MB",
      "citation": "t4"
    }
  ],
  "sections": [
    {
      "id": "evidence",
      "nav_label": "实验信号与边界",
      "heading_claim": "8K 与 32K 的容量信号足以支持立项复测",
      "state_line": "g=4 keeps the same model runnable under tighter memory pressure, but backend integration is still unproven.",
      "blocks": [
        {
          "type": "chart_with_aside",
          "chart_id": "kv-cache-context",
          "caption_takeaway": "KV cache falls by roughly 4x across tested context lengths.",
          "source_citations": ["t4"]
        }
      ]
    }
  ],
  "charts": [
    {
      "id": "kv-cache-context",
      "question": "How much KV cache memory does g=4 save across context lengths?",
      "chart_type": "bar_line",
      "source_citations": ["t4"],
      "units": ["MB", "%"],
      "conditions": "Qwen3-8B-like, one 80GB GPU, batch size 1",
      "data": [
        {"tokens": 2048, "g1_kv_mb": 306, "g4_kv_mb": 77},
        {"tokens": 8192, "g1_kv_mb": 1170, "g4_kv_mb": 293}
      ],
      "derived_fields": [
        {
          "name": "saving_ratio",
          "formula": "g1_kv_mb / g4_kv_mb"
        }
      ],
      "caption_takeaway": "The memory reduction is structural rather than a one-off point.",
      "known_limits": "This table does not prove production serving scheduler impact."
    }
  ],
  "comparison_methods": [
    {
      "id": "h2o",
      "name": "H2O / token eviction",
      "positioning": "Token-axis KV eviction for preserving heavy hitters under a fixed cache budget.",
      "mechanism": "Keep recent and high-importance tokens, evict lower-value token states.",
      "representative_evidence": "Summarize one primary or high-quality source result here.",
      "boundary": "Works on time/token axis; does not reduce depth-wise cache duplication by itself.",
      "relationship": "Orthogonal to depth-wise sharing; may combine with it if quality loss is controlled.",
      "visual_summary": "mini_flow | evidence_badge | axis_marker | source_image",
      "citations": ["r2"]
    }
  ],
  "decisions": [
    {
      "label": "立项复测",
      "status": "recommended",
      "reason": "Source evidence supports enough capacity signal; production integration remains unverified.",
      "citations": ["t4", "t5"]
    }
  ]
}
```

## Supported Block Types

The `sections[].blocks[]` array may use these repo-local block types:

| Block type | Use when | Required minimum |
| --- | --- | --- |
| `status_strip` | first viewport needs 2-4 headline facts | `items[]` with label, value, context, citation |
| `summary_cards` | several KPI facts need compact comparison | `cards[]` with label, value, detail, citation |
| `chart_with_aside` | a chart/source visual needs interpretation | `chart_id`, caption, aside bullets, source citations |
| `data_table_with_aside` | exact rows matter | columns, rows, interpretation, source citations |
| `original_evidence_pair` | a visual is reconstructed | reconstructed id, original asset id, transformation note |
| `method_cards` | prior art/current-status comparison | 3-5 method objects with mechanism, evidence, boundary |
| `comparison_matrix` | alternatives share common axes | axes, rows, synthesis sentence |
| `heatmap` | strength/coverage/risk is ordinal or numeric | rows, columns, values, scale meaning |
| `strip_chart` | sparse ranked/labeled rows | rows with label, value, proportional value |
| `decision_register` | next-step gates need approval | gate, current signal, missing proof, status |
| `narrative` | prose carries the report | content with citations where factual |

Do not force every report to use every block. Pick the minimum set that makes the evidence easy to inspect.

## Data Rules

- Prefer exact values over adjectives.
- Preserve units, task conditions, model names, hardware, date, and benchmark setup next to the values.
- If a value is calculated, record the formula in `charts[].derived_fields` or in a nearby note.
- If a chart is reconstructed from a source table or image, include both the chart contract and the original evidence asset or citation.
- For webpage sources, every cited URL should point to a local `web-article-capture` source package directory. Consume only that package's `source.md` and `images/` contract here.
- Keep captured package `images/` directories for original webpage images referenced by `source.md`.
- In `report-data.json`, point citations to the captured package directory and `source.md`. For any webpage image shown in the HTML, add an `assets[]` item with the displayed local `path`, original package image path, original image URL when known, nearby context, and usage policy.
- Before presenting the HTML review, run the HTML review data validators. Run the `web-article-capture` package validator separately for captured source package directories when practical.
- Use `source_discovery` to preserve the positive research path: which primary, adjacent-route, and boundary sources were considered; which were captured; and which drafting-time citation gaps required new crawling. This is not a substitute for visible citations, but it prevents
  the agent from treating validation as a reason to delete comparison claims.
- Keep source ids stable. The HTML body can show quiet numeric footnotes, but the data model should preserve `S/F/T/R` style markers for audit.
- Do not include hidden judge rubrics, forward-test expectations, or main-agent strategy in this file.

## Output Directory Pattern

Recommended review directory:

```text
review/
  report-data.json
  source_understanding_review.html
  assets/
    table_004.png
    figure_004.png
```

The HTML should be usable by opening it directly when it has no external scripts. If it uses CDN-backed Chart.js or web fonts, preview it through `scripts/serve_html_review.py`.
