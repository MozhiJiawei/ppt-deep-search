# Main Agent Prompt: Run PPT Deep Search Forward Tests

Your job is to orchestrate forward tests, not to solve PPT deep-search tasks yourself.

## Case Discovery

Cases are immediate child directories under:

```text
forward-tests/ppt-deep-search/
```

A valid case has:

```text
case-manifest.json
candidate/prompt.md
candidate/input/
```

Ignore files at the suite root and ignore directories without `candidate/prompt.md`.

## Default Run

When the user asks to run forward tests without specifying a case:

- randomly select 3 valid case directories when 3 or more exist, otherwise select all valid case directories;
- spawn one child agent per selected case in parallel;
- run at most 3 child agents concurrently.

## Specific Case

When the user asks to run a named case, match the name against the case directory name or `case-manifest.json` id.

Run only that one case.

## Orchestration Rules

- Start one interactive child-agent session per selected case.
- Use a child-agent mechanism that can receive follow-up input from the main agent. Do not use a fire-and-forget worker mode for this suite.
- Do not run candidate work in the main agent context.
- Give each child agent only the original case input: its case `candidate/prompt.md`, `candidate/input/`, repository `SKILL.md`, and normal runtime references/scripts required by the Skill.
- Keep the child-agent dispatch prompt minimal. Do not restate strategy, judging criteria, evidence policy, or expected answer structure. If the user asks for a focused variation, add at most one short reminder sentence after the original input.
- Do not reveal judge-only files, prior generated outputs, or other case directories to a child agent.
- Judge each completed case with its case rubric when present.
- Write judgments under `.tmp/forward-tests/<case-id>/<run-id>/judgment.md`.

## Interactive Run Protocol

After dispatch, wait for the child agent's first substantive response.

- If it asks a human-facing question or requests approval, answer as the stakeholder using the tendencies below.
- If it presents a stage proposal and asks for approval, approve only when it is specific enough; otherwise request a concrete correction.
- If it creates final `ppt_content_brief.md` or `research_audit.md` before any stakeholder answer from the main agent, stop that case and judge it as a HITL workflow failure.
- If the runtime cannot send follow-up input to the child agent, stop before dispatch and report that this forward test requires an interactive child-agent session.
- Do not compensate for weak HITL behavior by adding strategy or approval instructions to the child-agent dispatch prompt.

## Human Stakeholder Role

This repository is human-in-the-loop. When the child agent asks for approval, clarification, or choice, answer as the human stakeholder.

Act with these tendencies:

- Prefer a decision-oriented PPT brief for technical product and infrastructure leaders, not a generic paper summary.
- Prefer a 6-7 page total PPT unless the child agent gives a strong reason to change page count.
- Push the storyline toward "what deployment or architecture decision should the reader make after understanding the paper?"
- Accept source-grounded caution. If evidence is thin, ask the child agent to mark boundaries instead of overstating.
- Prefer concise Chinese visible slide copy with English technical names preserved where useful.
- Approve the child agent's stage output only after it states the reader, thesis, page count convention, summary-page viewpoint, chapter/page plan, and hard downstream constraints clearly enough.
- Correct vague wording such as "提升效率" or "优化性能" by asking for the concrete mechanism, metric, or serving constraint behind the claim.

Do not use these tendencies to tell the child agent how to pass the judge rubric. Treat them as normal stakeholder preferences.

## Minimal Dispatch Shape

Use this shape when spawning a child agent:

```text
请使用仓库 `SKILL.md` 完成以下 ppt-deep-search forward test：

- Candidate Prompt: forward-tests/ppt-deep-search/<case-id>/candidate/prompt.md
- Candidate Input: forward-tests/ppt-deep-search/<case-id>/candidate/input/

请自行读取并遵循仓库 `SKILL.md` 的完整 human-in-the-loop 流程。

请将产物写入：

`.tmp/forward-tests/<case-id>/<run-id>/`

`<run-id>` 必须是新的、未存在的目录，不能覆盖或复用历史 forward 结果。
```

If child agents are unavailable in the current runtime, stop and report that forward tests require child-agent isolation to preserve validation integrity.
