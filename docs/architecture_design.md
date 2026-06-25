# Architecture Design

This document is the development-time contract for `ppt-deep-search`.
`SKILL.md` is runtime guidance for agents; this file explains how the runtime pieces must stay aligned when maintainers change behavior.

## Runtime Contract

`ppt-deep-search` owns research alignment before downstream PPT generation.
It does not render final PPTX decks.

The runtime has two ordered phases:

1. Source Understanding review gate.
   The agent builds `review/source_understanding_review.html`, exports screenshots, records independent visual QA in `review/visual-qa.md`, and saves an approved source-understanding baseline.
2. PPT Content Brief HITL.
   The agent confirms final PPT audience, SCQA, page count, table of contents, and page viewpoints, then writes `ppt_content_brief.md`.

The Source Understanding gate is not optional. `SKILL.md` must not route into `references/ppt-brief-hitl.md` until the Source Understanding artifact is approved or the run records a clear blocker.

## Artifact Ownership

Workspace artifacts live under one task root, usually `.tmp/ppt-deep-search/<task-name>/` or `.tmp/forward-tests/<case-id>/<run-id>/`.

Required Source Understanding artifacts:

- `review/source_understanding_review.html`
- `review/source-understanding-images/`
- `review/visual-qa.md`
- `baselines/015-source-understanding.md`

Required final handoff:

- `ppt_content_brief.md`

The final handoff is written for downstream PPT makers. It must not contain judge notes, audit traces, approval logs, or author-facing source-locator tables. Those records belong in `review/`, `sources/`, `baselines/`, or QA logs.

## Reference Files

`SKILL.md` stays short: routing, hard gates, workspace contract, and final deliverables.

Detailed behavior lives in references:

- `references/evidence-principle.md` and `references/evidence-examples.md` define expression quality, source evidence priority, image use, and pyramid-style claims.
- `references/source-understanding-html-ppt.md` defines the Source Understanding HTML deck contract, screenshot export, independent visual QA, and approval gate.
- `references/ppt-brief-hitl.md` defines final PPT brief HITL, its JSON shape, skeleton generation, visible-copy checks, and final brief QA.

When a runtime rule changes, update the relevant reference and add or adjust an executable gate when the rule is machine-checkable.

## Script Gates

Repository-level dependency and contract checks start at `verify_dependencies.py`.

Current script responsibilities:

- `scripts/validate_markdown_size.py` enforces Markdown size budgets.
- `scripts/validate_source_understanding_html.py` renders Source Understanding HTML to PNG with Playwright, checks slide navigation, and enforces the hard image-scale gate.
- `scripts/hitl_json_to_brief_skeleton.py` converts approved HITL JSON into `ppt_content_brief.md` skeletons. It supports one-page summary-only briefs with empty TOC and content pages.
- `scripts/validate_ppt_content_brief.py` validates final brief structure, visible copy, density, and expected page count.

Do not rely on prose-only checks for artifact presence, approved baselines, or renderable HTML when a validator can check them.

## Forward Tests

Forward tests are main-agent orchestration flows with isolated candidate child agents.
The main agent acts as the human stakeholder and writes `judgment.md`.

Forward-test instructions must stay judge-side:

- Candidate dispatch stays minimal and must not include rubrics or expected failure modes.
- Judge rubrics and fixture manifests must require the Source Understanding review artifacts before accepting final brief work.
- Web-source cases must also expect `sources/web/<source-slug>/` capture packages and capture validator evidence.

Latest local forward-test evidence as of 2026-06-25:

- `20260625-forward-test-1` completed full runs for `aegaeon-gpu-pooling-hitl`, `rtx-spark-agent-pc-web-evidence-hitl`, and `stochastic-kv-routing-hitl`. All were judged `Pass with issues`; no blocking findings remained.
- `20260625-source-html-navcheck-1` completed Source Understanding-only runs for the same three cases. RTX Spark and Stochastic KV Routing were `Pass`; Aegaeon was `Pass with issues` because visual QA needed five repair rounds.
- The latest source-only runs validated the Source Understanding HTML render path, exported PNGs, independent visual QA records, and keyboard-navigation gate.

When refreshing published showcase docs, use the newest run directory under `.tmp/forward-tests/<case-id>/`, read its `judgment.md`, and copy only publication-safe artifacts into `docs/showcase/` or `docs/assets/forward-tests/`.

## Change Discipline

Runtime behavior changes must update the affected runtime docs, references, scripts, and forward-test judge expectations together.

Before submitting:

```powershell
python scripts/validate_markdown_size.py .
python verify_dependencies.py --skip-services
```

Run targeted script self-tests for changed validators or generators. For Source Understanding or brief-HITL changes, also run or inspect the relevant forward-test result and record what was validated.
