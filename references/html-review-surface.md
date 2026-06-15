# HTML Review Surface

Scope map:

- Owns purpose, outcome standard, research autonomy, source discovery, and output package for HTML reviews.
- Does not own visible prose details; use `html-review-expression.md`.
- Does not own citations or captured webpage source rules; use `html-review-evidence.md`.
- Does not own approval checks; use `html-review-quality.md`.

This is the entry contract for the temporary source-understanding HTML review.
The page is a Chinese-first technical report for human approval, not an audit
dump and not the downstream PPT Content Brief.

## Purpose

Use the HTML review when source understanding needs inspectable evidence:
papers, product announcements, technical news, repository analysis, incidents,
benchmarks, or mixed source packages.

The page must help the human decide whether the agent understands:

- the problem;
- the source evidence;
- the comparison context;
- the method or mechanism;
- the results and boundaries;
- the next research or deck-planning move.

## Related References

These files are also listed in `SKILL.md`; this section restates their roles for readers already inside the HTML review contract.

Always load:

- `references/html-review-expression.md`

Load by need:

- `references/html-review-outline.md` for the default narrative spine.
- `references/html-review-evidence.md` for citations, captured webpage source
  packages, and source-image rules.
- `references/html-review-visuals.md` for source images, diagrams, charts, and
  reusable visual habits.
- `references/html-review-quality.md` before approval.
- `references/html-review-data-model.md` when using `report-data.json`, copied
  assets, reconstructed charts, KPI strips, method comparisons, or more than
  two cited quantitative claims.
- `references/html-review-report-kit.md` when reusable CSS, report rhythm,
  chart/table/source-image blocks, preview behavior, or Chart.js defaults help.
- `references/html-review-pattern-library.md` when using method cards,
  evidence pairs, reconstructed chart blocks, or citation anchor patterns.

Load only what the current review needs.

## Outcome Standard

The page succeeds when it lets the human both trust the evidence and make a
sharper technical judgment.

Trustworthy by inspection:

- Put original source images, report-specific page captures, tables, or quoted evidence near the
  claims they support.
- Keep citations quiet, clickable, and close to the claim, chart, table, or
  caption they support.
- Use local browser-captured assets for webpage evidence.
- Name weak or missing evidence as a boundary instead of hiding it.

Data-smart technical judgment:

- Extract numbers, units, benchmark conditions, system constraints, dates,
  architecture layers, compatibility limits, and adoption signals.
- Use KPI strips, matrices, decision registers, evidence tables, reconstructed
  charts, source-image pairs, timelines, or diagrams when they clarify the
  decision.
- Do not create decorative charts. Every chart or table should answer a
  technical question and preserve source, unit, condition, and boundary.

## Research Autonomy

The required outline is a floor, not a template. The agent should behave like a
researcher preparing a useful briefing.

Requirements:

- Add definitions, background diagrams, timelines, benchmark context, glossary
  notes, or architecture sketches when they reduce reader confusion.
- Use primary or high-quality supplemental sources when the provided source is
  too narrow.
- Answer likely skeptical objections with evidence, boundaries, or open
  questions.
- Include missing comparisons, metrics, baselines, caveats, or related methods
  when expert readers would expect them.
- Prefer a clear authored synthesis over equal-weight notes under every heading.

Reject a report that merely fills headings without explaining anything beyond
the user's input.

## Source Discovery Before Writing

Before drafting, create:

```text
<workspace-root>/sources/source-discovery.md
```

Include:

- primary sources;
- adjacent-route comparison sources;
- boundary/check sources;
- candidate visuals;
- crawl and capture plan.

When drafting reveals missing evidence, loop back to discovery and capture. Do
not remove useful comparisons only to pass validation. Fetch the source or mark
the idea as an open question or boundary.

## Output Package

Create:

```text
<workspace-root>/review/
  report-data.json
  source_understanding_review.html
  assets/
```

The page may propose implications and next questions, but it must not replace
later SCQA, page-count, table-of-contents, page-viewpoint, or final approval
gates.
