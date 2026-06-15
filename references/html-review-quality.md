# HTML Review Quality Gate

Run this check before asking for source-understanding approval.

## Human Review Checklist

- First viewport states the core conclusion and strongest evidence in Chinese.
- Reader lens from `html-review-expression.md` is reflected in the argument.
- Each major section answers a concrete reader question.
- Figures and tables say what to notice, what claim they support, and what they
  do not prove.
- Side navigation may use fixed outline labels; in-body headings should state
  conclusions or decision implications.
- The report adds autonomous research value beyond the user's supplied outline.
- The problem domain is understandable without reading the original source.
- Alternatives are compared, not merely named.
- Mechanism sections have explanatory visuals when relationships matter.
- Results include tradeoffs, limitations, and weak evidence.
- References are complete enough to audit.
- Webpage URLs cited in the report map to local `web-article-capture` source
  package directories in `report-data.json`.
- Webpage images displayed in the report are local `review/assets/` files with
  matching asset metadata.
- The page asks one clear approval or correction question.

## Script Gates

Run when practical:

```powershell
python scripts/validate_web_evidence_package.py <workspace-root>/review/report-data.json --require-images when-indexed
python scripts/validate_html_review_data.py <workspace-root>/review/report-data.json
python scripts/validate_html_review.py <workspace-root>/review/source_understanding_review.html
```

For product launches, technical announcements, official blogs, or media-rich
webpages, also validate the upstream source package directories with the
`web-article-capture` validator:

```powershell
python web-article-capture/scripts/validate_capture_package.py <captured-source-root> --require-images when-referenced
```

## Rejection Triggers

Revise before showing the report if visible main body contains:

- generic template headings or default section names instead of topic-specific
  claims;
- mechanical outline headings used as body titles without a topic claim;
- work-log narration, QA status, or agent process notes in the main reading
  flow;
- raw data-model labels exposed as reader-facing prose;
- dense bracket citation chains;
- plain non-clickable citation markers in visible paragraphs;
- broken or duplicate citation anchors;
- remote webpage image hotlinks;
- webpage facts cited only by URL without local evidence;
- visual captions that describe provenance instead of what to notice;
- a first viewport that starts with process rather than conclusion.

Move audit-only language to `research_audit.md`, a details appendix, HTML
comments, or structured report data.
