---
name: coding-prompt
description: Turn a coding request into a concise, copyable agent prompt with a model and reasoning recommendation.
metadata:
  short-description: Concise coding-task prompt generator
---

# Coding Prompt

Create a handoff-ready prompt from the user's task information. Do not execute the task. User instructions override these defaults.

## Compose the task

- Use the supplied goal, scope, evidence, contracts, constraints, acceptance criteria, and destination. Request missing information only when it materially affects the handoff.
- Preserve the requested deliverable and authority boundary. Reviews, diagnoses, and plans remain read-only unless implementation is requested. Do not add external actions or expand scope.
- Use supplied or already-loaded evidence. Inspect additional sources only when the user asks to incorporate them; do not scan a repository merely to shorten a prompt.
- State the intended behavior change, contracts to preserve, and observable acceptance criteria. Do not invent APIs, paths, versions, commands, mappings, or results.
- Keep uncertainty explicit. Block only work that depends on missing authorization, contracts, or required decisions; preserve independent work.
- Consolidate repeated requirements without weakening them. Retain prerequisites, exact messages, boundary values, regression cases, required checks, and stop points. Preserve wording verbatim only when requested or contractually significant.

## Match the execution context

- Judge where the prompt will run, not where it is written.
- In a known project with applicable instructions available, omit AGENTS.md reminders and duplicated reading triggers, Git, style, safety, and routine verification rules. Keep task-specific exceptions, branch expectations, ownership, and concurrent-work facts. Omission does not waive project rules.
- A prompt written outside the project but executed inside it needs the supplied project identity, not a copy of its rules. Referenced documents are read when applicable, not automatically in full.
- For an unknown or non-project destination, include enough supplied context, source pointers, constraints, and acceptance criteria to stand alone. Do not assume access to this chat, local files, tools, or instructions. If a repository is available but instruction discovery is uncertain, a brief instruction to discover applicable guidance is sufficient.

## Scope verification and handoff

- Choose the fastest, simplest checks sufficient for the requested behavior. Do not add builds, browser checks, or E2E unless needed or required; a blocked test does not by itself require browser fallback.
- Carry forward known dependency blockers and project restrictions without adding dependency repair. Skip unchanged blocked checks, continue independent verification, and report them as blocked rather than passed.
- Preserve explicit user/project exclusions for dedicated accessibility/ARIA checks while retaining existing accessibility behavior and needed functional checks. Keep such exclusions task-specific; do not infer a universal exemption or duplicate rules already available at the destination.

- Preserve requested checks and project gates. Otherwise match verification to behavior and risk; avoid unrelated checklists.
- Reference relevant existing tests or matrices while retaining new cases and expected outcomes. Reuse evidence only within its source and environment limits; require fresh checks where changes, failures, or gaps invalidate it. Component or fixture results do not prove live integration.
- Use original specifications for exact contracts or conflicting evidence; briefs and history provide orientation. Avoid blanket rereads.
- Include documentation targets or timing when requested or task-specific; do not duplicate established maintenance rules or broaden authorization.
- Keep separate batches and stop points distinct. Scale the output structure to the task and omit empty sections.

## Recommend a model and reasoning

- Complete the prompt first. Assess the resulting task and executor's role, uncertainty, risk, context, tools, coordination, and verification burden.
- Preserve explicit user selections. Otherwise recommend one supported model and reasoning combination using target-environment evidence or current official documentation. State unresolved availability rather than assuming the current session represents the destination.
- Establish required quality before comparing latency and total task cost, including handoffs, retries, and integration. Treat unmeasured advantages as tentative. Do not use fixed model rankings, escalation chains, or assume equal reasoning labels mean equal capability across models.
- Diagnose missing context, unclear requirements, and tool or environment failures before attributing difficulty to model capability. The currently running model is not a preference by default.
- A recommendation does not switch models, change configuration, or authorize delegation. Include worker ownership and integration responsibilities only when the task actually calls for delegation.

## Output

Use concise English by default unless the user requests another language or the target project requires it. Follow the user's requested format; otherwise return:

```text
[complete handoff-ready prompt]
```

Model recommendation: `<model>`
Reasoning: `<effort>`

Keep the complete prompt in one copyable fenced block, with the recommendation outside it. Use a different fence marker for nested code. Add a brief availability qualification only when needed.
