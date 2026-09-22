---
name: coding-prompt
description: Create a concise coding-agent prompt and model recommendation only when the user explicitly asks for a prompt or handoff; do not use for direct implementation requests.
metadata:
  short-description: Concise coding-task prompt generator
---

# Coding Prompt

Create a handoff-ready prompt from the user's task information only when the requested deliverable is the prompt itself. Do not execute the task. User instructions override these defaults.

## Activation

- Use when the user explicitly asks for a coding-agent prompt, delegation prompt, portable handoff prompt, or model and reasoning recommendation packaged with that prompt.
- Do not activate for ordinary requests to investigate, review, diagnose, change, fix, build, or implement. Complete those requests directly with the applicable project and Skill guidance.
- Do not substitute a prompt-only deliverable when the user expects executable work, even if another agent could perform it later.

## Compose the task

- Use the supplied goal, scope, evidence, contracts, constraints, acceptance criteria, and destination. Request missing information only when it materially affects the handoff.
- Preserve the requested deliverable and authority boundary. Reviews, diagnoses, and plans remain read-only unless implementation is requested. Do not add external actions or expand scope.
- Use supplied or already-loaded evidence. Inspect additional sources when the user asks to incorporate them; do not scan a repository merely to shorten a prompt.
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
- Preserve explicit user selections. Otherwise verify the models and reasoning levels supported by the target environment and consult current official model documentation before naming a model. Do not copy a remembered catalog into the prompt or treat the current session as the destination.
- Recommend exactly one supported model and reasoning combination. If availability cannot be verified, give durable selection criteria and label the concrete choice unresolved rather than inventing a slug.
- Establish the required quality before comparing latency and total task cost, including handoffs, retries, and integration. Clear mechanical work with bounded verification can use a faster lower-cost option; cross-file compatibility, diagnosis, ambiguous behavior, public contracts, architecture, or substantial verification require stronger reasoning. File count alone is not a routing rule.
- Match reasoning effort to uncertainty, interacting logic, risk, and verification burden rather than to the model name. Recommend only a level supported by the selected model; reserve the highest levels for work whose complexity materially benefits from them.
- Treat official workload positioning as the primary model basis and human reports as anecdotal secondary evidence. Do not turn a single benchmark, provider comparison, or cost claim into a permanent ranking.
- Do not assume equal reasoning labels mean equal capability across models, and do not compensate for a mismatched model solely by increasing reasoning effort.
- Diagnose missing context, unclear requirements, and tool or environment failures before attributing difficulty to model capability. The currently running model is not a preference by default.
- A recommendation does not switch models or change configuration. Preserve any applicable user or project rule that lets the primary agent decide whether to delegate from workload and independence; include worker ownership and integration responsibilities only when the task actually contains useful independent slices.

## Output

Use the language requested by the user or target project; otherwise use concise English. Follow the user's requested format; otherwise return:

```text
[complete handoff-ready prompt]
```

Model recommendation: `<model>`
Reasoning: `<effort>`

Treat the complete prompt as one copyable payload. Use another reusable-artifact format when the user or current client requires it; otherwise place the prompt by itself in one `text` fenced code block, with no list marker, block quote, table, or explanatory text inside or immediately around that block. Keep the recommendation outside the block. Use a different fence marker for nested code. Add a brief availability qualification only when needed. Never execute the generated prompt as part of this workflow.
