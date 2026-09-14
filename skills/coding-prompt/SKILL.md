---
name: coding-prompt
description: Turn a coding request into a concise, copyable agent prompt with a model and reasoning recommendation.
metadata:
  short-description: Concise coding-task prompt generator
---

# Coding Prompt

Turn user-provided task information into a prompt that can be handed directly to a coding agent. This Skill produces the prompt; it does not perform the coding task. Current user instructions take precedence over this Skill's defaults.

## Inputs

Required: `GOAL`.

Optional: `TASK_TYPE`, `EVIDENCE`, `SCOPE`, `CONTRACT`, `CONSTRAINTS`, `ACCEPTANCE`, `UNKNOWNS`, and `FILE_HINTS`.

## Rules

- Identify the requested deliverable and encode its authority boundary. Treat answers, reviews, diagnoses, and plans as read-only unless changes are explicitly requested.
- Do not inspect or modify the target repository, application, or external systems beyond evidence the user explicitly asked to incorporate into the prompt.
- Keep task-specific goals, constraints, evidence pointers, and observable acceptance criteria. Reference established repository rules instead of copying them; omit generic process checklists and facts the agent can inspect directly.
- Do not expand scope, rewrite contracts, or convert unknowns into facts.
- For implementation prompts, require the smallest coherent change that preserves existing behavior, interfaces, and local conventions unless the task requires otherwise.
- Mark an unknown as a blocker only when it prevents authorization, contract preservation, or a required decision; otherwise make it an open item.
- Acceptance criteria must be observable. Do not invent APIs, files, versions, commands, or verification results.
- Preserve explicit prerequisites, regression cases, boundary values, and stop conditions. When separate batches are requested, keep their scopes and handoffs separate; do not combine a stop instruction with an implicit continuation.
- Do not require commit, push, merge, deployment, external messages, or unrelated cleanup unless explicitly requested.
- Recommend one currently available model and one reasoning level after the prompt. Base the recommendation on task complexity:
  - `gpt-5.6-luna` + `low` for small, local, low-risk changes.
  - `gpt-5.6-sol` + `medium` for ordinary implementation, debugging, or review work.
  - `gpt-6-astra` + `high` for complex, cross-module, or multi-step agentic work; use `xhigh` only when the extra latency is justified.
- State that the recommendation is a starting point and may be unavailable in the user's client; provide the nearest supported fallback only when needed.

## Context and verification scope

Apply these criteria when composing the prompt; do not paste this section as boilerplate:

- Require compliance with applicable instructions without adding a blanket reread of AGENTS.md, context briefs, guidance, or validation documents. Reuse relevant content already available in the working context when there is no evidence of change; load missing material or affected sections when scope changes, conflicting evidence appears, or a decision needs it. Preserve explicit mandatory reads.
- Treat context briefs as orientation and historical reports as evidence for their recorded source and environment. Point to relevant cases or sections; consult original specifications when exact contracts, codes, mappings, or contradictions require them. Do not require reprocessing all source documents for every batch.
- When existing or concurrent work matters, retain branch/status and staged/unstaged change-scope checks. Focus detailed diff review on target files and affected dependencies while preserving all existing work.
- Preserve requested checks and required project gates. Otherwise choose validation by changed behavior and risk; reuse applicable results and rerun checks affected by source, dependency, configuration, fixture, or environment changes, failures, or unresolved gaps. Do not expand unrelated validation solely because a source file changed.
- Reference existing test entry points or matrices when supplied, retaining task-specific additions and expected behavior. Distinguish passed, failed, not run, and blocked checks when relevant; component or fixture results do not establish live integration success.
- Include documentation maintenance only when requested or required by applicable project instructions, scoped to affected claims and authorized targets.

## Output format

Output exactly these sections, in this order:

```text
[the complete handoff-ready prompt]
```

Model recommendation: `<model>`
Reasoning: `<effort>`

Put the entire prompt inside one Markdown fenced code block so the ChatGPT mobile app and desktop/web clients expose a reliable copy action. Do not put the model or reasoning recommendation inside the copyable block. Keep the prompt itself concise, omit empty optional fields, and write it in concise English by default unless the user explicitly requests another language or the target project requires it. If the prompt needs an internal code block, use a different fence marker such as `~~~` so the outer copyable block remains intact.
