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

- Before changing agent guidance, consult current official OpenAI documentation, then apply explicit user instructions and verified project constraints.
- Retain a rule only when it is specific, durable, behavior-changing, correctly placed, and not duplicated. Otherwise remove or compress it.
- Write newly created or substantially rewritten agent instructions in concise English for token efficiency. Preserve the project language when it is an established requirement or the user explicitly requests it; never sacrifice precision, safety, or contract clarity for brevity.
- Start context narrowly: read only governance files and evidence directly relevant to the change. Expand only when the available evidence cannot establish the boundary or correctness. Do not attach full conversations or unrelated tool output to handoffs.
- Apply the execution policy below to this workflow and the governance rules being edited. Preserve explicit delegation requirements and project ownership boundaries.
- Do not invent roles, capabilities, routing, or future behavior. Update every reference when renaming a role.
- Do not commit, push, merge, or deploy unless explicitly requested.

## Token-aware execution

- Minimize expected total tokens while preserving correctness, contracts, and required verification. Prefer the primary agent when quality is comparable and delegation is unlikely to save tokens; use it as the default when savings are unclear.
- Make a brief qualitative comparison using available context: primary execution versus worker context and reasoning, handoff, repeated reads, coordination, integration, verification, and likely rework. Smaller main-thread context, lower model prices, and faster parallel completion do not alone prove fewer total tokens. Do not run a benchmark or produce a cost report unless requested.
- Keep small, tightly coupled, or already-understood work in the primary agent, including difficult tasks that a short deterministic check can resolve. Difficulty, file count, and role availability alone do not justify delegation.
- Delegate a bounded, independent slice when context isolation is expected to reduce total tokens at equal quality, or when necessary expertise or independent review materially improves required quality. Preserve explicit user requests; do not remove mandatory specialist or review boundaries merely to save tokens.
- Prefer one specialist and reuse it for related work. Use additional workers only for disjoint scopes with a clear benefit; do not recursively delegate without an explicit request.
- Pass only the goal, contracts, owned paths, evidence pointers, constraints, acceptance criteria, and stop condition. Use `fork_turns: none` when supported; never pass full history. Request concise results, evidence locations, changed files, and verification gaps. Reuse verified findings; recheck only drift, contradictions, or material gaps instead of repeating the worker's task.
- Keep estimates separate from measured usage. Do not infer token savings or equal quality from elapsed time, answer length, or one small test. Never reduce required validation to satisfy an unmeasured token target.

## Delivery and verification

Confirm parseable formats, consistent role names and path references, no stale names or paths, and no unrelated file changes. Report only completed checks and unresolved risks.
