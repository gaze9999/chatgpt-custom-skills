---
name: coding-task-prompt-builder
description: Build concise, directly executable coding-task prompts from minimal inputs while preserving scope, contracts, and acceptance boundaries.
metadata:
  short-description: Concise coding-task prompt generator
---

# Coding Task Prompt Builder

Turn user-provided task information into a prompt that can be handed directly to a coding agent. This Skill produces the prompt; it does not perform the coding task. Output only the prompt body, without tutorials, prefaces, or process recaps. Current user instructions take precedence over this Skill's defaults.

## Inputs

Required: `GOAL`.

Optional: `TASK_TYPE`, `EVIDENCE`, `SCOPE`, `CONTRACT`, `CONSTRAINTS`, `ACCEPTANCE`, `UNKNOWNS`, and `FILE_HINTS`.

## Rules

- Identify the requested deliverable and encode its authority boundary. Treat answers, reviews, diagnoses, and plans as read-only unless changes are explicitly requested.
- Do not inspect or modify the target repository, application, or external systems beyond evidence the user explicitly asked to incorporate into the prompt.
- Keep only information that changes the task. Do not repeat repository rules or facts the agent can inspect directly.
- Do not expand scope, rewrite contracts, or convert unknowns into facts.
- For implementation prompts, require the smallest coherent change that preserves existing behavior, interfaces, and local conventions unless the task requires otherwise.
- Mark an unknown as a blocker only when it prevents authorization, contract preservation, or a required decision; otherwise make it an open item.
- Acceptance criteria must be observable. Do not invent APIs, files, versions, commands, or verification results.
- Do not require commit, push, merge, deployment, external messages, or unrelated cleanup unless explicitly requested.

Output a directly handoff-ready task prompt and omit empty optional fields.

Write the generated prompt in concise English by default. Use another language only when the user explicitly requests it or the target project requires it.
