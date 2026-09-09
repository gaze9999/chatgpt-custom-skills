---
name: coding-task-prompt-builder
description: Build concise, directly executable coding-task prompts from minimal inputs while preserving scope, contracts, and acceptance boundaries.
metadata:
  short-description: Concise coding-task prompt generator
---

# Coding Task Prompt Builder

Turn user-provided task information into a prompt that can be handed directly to a coding agent. Output only the prompt body, without tutorials, prefaces, or process recaps. Current user instructions take precedence.

## Inputs

Required: `GOAL`.

Optional: `TASK_TYPE`, `EVIDENCE`, `SCOPE`, `CONTRACT`, `CONSTRAINTS`, `ACCEPTANCE`, `UNKNOWNS`, and `FILE_HINTS`.

## Rules

- Keep only information that changes the task. Do not repeat repository rules or facts the agent can inspect directly.
- Do not expand scope, rewrite contracts, or convert unknowns into facts.
- Use minimal necessary changes for implementation. Treat diagnosis, review, and planning as read-only by default.
- Mark an unknown as a blocker only when it prevents authorization, contract preservation, or a required decision; otherwise make it an open item.
- Acceptance criteria must be observable. Do not invent APIs, files, versions, commands, or verification results.
- Do not require commit, push, or deployment unless explicitly requested.

Output a directly handoff-ready task prompt and omit empty optional fields.

Write the generated prompt in concise English by default. Use another language only when the user explicitly requests it or the target project requires it.
