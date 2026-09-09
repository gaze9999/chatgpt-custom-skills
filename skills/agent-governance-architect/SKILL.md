---
name: agent-governance-architect
description: Audit, simplify, and restructure repository AGENTS.md and subagent guidance; retain only project- or role-specific, durable rules that change behavior.
metadata:
  short-description: Agent governance, role boundaries, and instruction minimization
---

# Agent Governance Architect

Place agent instructions at the correct layer with the smallest rule set that preserves execution, ownership boundaries, and safety. Prefer removing, moving, or compressing rules over adding them.

## Scope

- By default, modify only `AGENTS.md`, `.codex/agents/*`, `agents/*`, and directly related governance documents.
- Do not modify application code, dependencies, build, or deployment configuration unless explicitly requested.
- When repository structure must be verified, run `scripts/scan_repo_structure.py`. Treat observable configuration and implementation as evidence, not document claims.

## Layering

- Global instructions contain only cross-repository, durable principles.
- Repository `AGENTS.md` contains only project-specific architecture, ownership, verification, and safety constraints.
- Subagent guidance contains only role differences, handoff content, and exclusions. The primary agent retains integration and final decisions.
- One-off requirements, migration details, and temporary restrictions belong in the current task prompt.

## Operating rules

- Retain a rule only when it is specific, durable, behavior-changing, correctly placed, and not duplicated. Otherwise remove or compress it.
- Write newly created or substantially rewritten agent instructions in concise English for token efficiency. Preserve the project language when it is an established requirement or the user explicitly requests it; never sacrifice precision, safety, or contract clarity for brevity.
- Start context narrowly: read only governance files and evidence directly relevant to the change. Expand only when the available evidence cannot establish the boundary or correctness. Do not attach full conversations or unrelated tool output to handoffs.
- Delegate only when a subtask has a clear boundary, can run independently, or reduces context cost. Handoffs include only the needed scope, contract, evidence, and stop condition.
- Do not invent roles, capabilities, routing, or future behavior. Update every reference when renaming a role.
- Do not commit, push, merge, or deploy unless explicitly requested.

## Delivery and verification

Confirm parseable formats, consistent role names and path references, no stale names or paths, and no unrelated file changes. Report only completed checks and unresolved risks.
