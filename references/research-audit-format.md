# Research Audit Format

This file defines the internal audit artifact for `ppt-deep-search`.

`research_audit.md` is not a downstream PPT copy source. It exists to preserve human approvals, evidence discipline, source usage policy, and anti-hallucination checks after the final `ppt_content_brief.md` has been stripped down to PPT-ready text.

## Required Headings

- `# Research Audit`
- `## Research Frame`
- `## Source Understanding`
- `## Executive Thesis`
- `## Reader Cognitive Path`
- `## Pyramid Outline`
- `## Chapter Logic`
- `## Page Logic Audit`
- `## Claim Evidence Implication Table`
- `## Evidence Map`
- `## Source Usage Policy`
- `## Supplemental Research`
- `## Assumptions and Open Questions`
- `## Approval Log`

## What Belongs Here

- Human-approved hard constraints: audience, page count, counting convention, titles, subtitles, analysis summaries, and table-of-contents entries.
- Internal logic fields: page role, supported chapter claim, Claim/Evidence/Implication, boundary reminders, and source usage policy.
- Evidence source locators: file paths, URLs, page numbers, section names, figure/table ids, or user statements.
- Verification status for numeric claims and causal claims.
- Supplemental research source list and how it supports or qualifies the approved viewpoint.
- Assumptions, open questions, and claims that should be softened.

## What Must Not Be Copied Into PPT Content Brief

Do not copy these audit concepts into `ppt_content_brief.md`:

- Claim/Evidence/Implication labels.
- Evidence type labels such as `source`, `inference`, `user_judgment`, or `needs_verification`.
- Source locator tables.
- Approval logs.
- Misread-risk analysis.
- Baseline file paths.
- Internal boundary analysis unless rewritten as a short `备注`.

## QA Purpose

QA should use this file to check that the PPT-ready content is grounded, but the PPT maker should not treat this file as slide copy.
