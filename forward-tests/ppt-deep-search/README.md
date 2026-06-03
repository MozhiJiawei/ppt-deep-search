# PPT Deep Search Forward Tests

Forward tests are human-orchestrated child-agent runs for checking whether the runtime Skill can conduct human-in-the-loop research and produce a PPT-ready Content Brief plus Research Audit from realistic source material.

## Cases

Each case lives under:

```text
forward-tests/ppt-deep-search/<case-id>/
```

Required candidate-facing files:

- `case-manifest.json`
- `candidate/prompt.md`
- `candidate/input/`

Optional judge-facing files:

- `fixture-manifest.md`
- `judge/rubric.md`

## Running Semantics

Forward tests do not need a Node runner. They are main-agent orchestration prompts, but they do require an interactive child-agent session:

- When the user asks to run forward without specifying a case, the main agent randomly chooses up to 3 case directories and starts one child agent per case.
- The max child-agent concurrency is 3.
- When the user asks to run a named case, the main agent starts exactly one child agent for that case.
- Each child agent receives only that case's `candidate/prompt.md`, `candidate/input/`, repository `SKILL.md`, and normal runtime references/scripts required by the Skill.
- Judge-only files stay in the main agent context.
- The main agent must wait for each child agent's human-facing question or approval request and answer it as the stakeholder.
- If a child agent writes final artifacts before any main-agent stakeholder answer, stop that case and record it as a HITL failure.
- Do not launch a fire-and-forget worker that cannot receive follow-up input; use an interactive child-agent/session runner.

Case names are the directory names under:

```text
forward-tests/ppt-deep-search/
```

Use `main-agent-prompt.md` for the exact orchestration wording.

## Human-In-The-Loop Semantics

Unlike one-shot downstream PPT generation tests, this suite tests a human-in-the-loop Skill. The main agent must act as the human stakeholder when the child agent asks questions. It should answer with product intent, audience preference, judgment calls, and corrections, while avoiding strategy coaching or judge-rubric leakage.

The main agent is not allowed to treat the child agent as a fire-and-forget worker. The first useful child-agent response should be a question, an approval gate, or an explicit statement that the research frame is already fully specified. If the child agent silently assumes approvals, that behavior is the test result, not something to repair by adding more candidate prompt text.

## Minimal Prompt Principle

Forward tests measure whether the runtime Skill can elicit and shape the brief through its normal workflow. The child-agent dispatch prompt should contain only:

- the candidate prompt path;
- the candidate input directory;
- the instruction to follow repository `SKILL.md`;
- the required output directory under `.tmp/forward-tests/<case-id>/<run-id>/`;
- at most one short user-requested reminder sentence for that run.

Do not include strategy explanations, judging criteria, expected answer structure, evidence-selection policy, approval scripts, or summaries of previous failures in the child-agent dispatch prompt. Keep those in `fixture-manifest.md`, `judge/rubric.md`, or the main agent's judgment context only.

In Codex, also keep the child context isolated:

- Do not use full-history forking for the candidate child. A fork may leak judge-side context, previous user critiques, or main-agent hypotheses into the candidate run.
- Spawn the child with a fresh minimal prompt and the required paths.
- If the child says it cannot find `multi_agent_v1.spawn_agent`, remind it once that it is already the spawned candidate child and should continue without spawning another agent.
