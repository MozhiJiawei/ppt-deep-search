# Dialogue And Approval

Scope map:

- Owns HITL reply shape, baseline persistence, skipped approval, and final hard-constraint approval.
- Does not own visible slide-copy rules; use `ppt-viewpoint-planning.md`.
- Does not own final file fields; use `ppt-content-brief-format.md`.

This reference owns human-in-the-loop conversation shape, baseline discipline,
and final approval. Keep visible chat compact; keep audit detail in files.

## Conversation Shape

Normal user-facing turns should feel like a research conversation:

```text
我现在的判断：
- ...
- ...

需要你拍板的一件事：
...
```

Use these rules:

- Use 2-4 bullets for the current read.
- Ask exactly one decision question.
- Avoid dumping evidence inventories in chat.
- Save detailed maps for baselines and `research_audit.md`.
- Use 2-3 options only when options clarify the decision.
- Include a free-form escape hatch when using options.

Use A/B/C options for:

- unclear audience selection;
- top-level summary page expression.

Do not force A/B/C for chapter planning or page planning. Give the best
proposal and ask what to adjust.

## Baseline Discipline

Every approved stage must become a baseline under:

```text
<workspace-root>/baselines/
```

After saving a baseline, tell the user the path in one short sentence.

Do not silently rewrite an approved baseline. If new evidence suggests a
change, ask whether to revise it and record the revision in `research_audit.md`.

If the user chooses an earlier option after several challenge rounds, preserve
the history and record which historical option was selected.

## Skipped Approval

Only skip gates when the user explicitly requests a one-pass or unapproved
draft. Accepted phrases include:

- `one-pass draft`
- `一次性草稿`
- `不走 HITL`
- `unapproved draft`

When gates are skipped, mark every skipped approval as unapproved in
`research_audit.md`.

Output directory language does not count as approval. Forward-test paths,
artifact paths, or "write files" instructions only define where outputs go.

## Final Hard-Constraint Bundle

Before writing final handoff files, ask the user to approve the downstream
constraints that the PPT maker must preserve:

- page count and page-count convention;
- target audience and desired belief change;
- approved source-understanding conclusion and evidence boundary;
- SCQA, top-level thesis, and big logic;
- table-of-contents titles, descriptions, order, and chapter claims;
- chapter logic or one-page internal beat sequence;
- every page title, subtitle, and `分析总结` bullet;
- every page role;
- required source figures, tables, captured visuals, and usage policy;
- supplemental research sources and type;
- claims that must be preserved;
- boundaries the downstream PPT skill must not weaken.

The final bundle must expand every page's visible viewpoint fields. Do not
compress a page into `Page N: title / subtitle`. For each page, list
`所属章节` when applicable, `页面标题`, `标题说明`, and every `分析总结` bullet.

Save the proposed bundle before asking:

```text
<workspace-root>/QA/approval_bundle.md
```

Then run:

```powershell
python scripts/validate_ppt_content_brief.py <workspace-root>/QA/approval_bundle.md --approval-bundle-check
```

If validation fails, fix the bundle before showing it.

## Approval Prompt Shape

Use a compact prompt with these fields:

```text
落盘前请确认这组下游硬约束：
- 听众：...
- HTML review：路径 / 核心判断 / 证据边界
- SCQA：...
- 顶层总结页：标题 / 标题说明 / 分析总结
- 页数与口径：...
- 目录：...
- 逐页观点层：...
- 主证据图：...
- 不能说满的边界：...

是否批准我按这组约束写入 PPT Content Brief 和 Research Audit？
```

Do not write final files until the user approves, unless they requested an
unapproved draft.
