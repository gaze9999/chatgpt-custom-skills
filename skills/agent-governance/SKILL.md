---
name: agent-governance
description: Audit, simplify, or restructure AGENTS.md, subagent roles, model routing, and instruction layering for a project or portable setup. Use for agent-governance work, not ordinary application implementation or general code review.
metadata:
  short-description: Agent governance, role boundaries, and instruction minimization
---

# Agent Governance

Keep the smallest instruction set that preserves authorization, contracts, project knowledge, and completion criteria. Prefer removing, merging, or relocating rules over adding them.

## Scope and evidence

- Treat an audit or recommendation as read-only. Edit only when requested, normally within `AGENTS.md`, role configuration, and directly related governance documents; do not expand into application code or external actions.
- When edits are requested, complete and verify them. Deliver only a prompt, plan, review, report, or handoff when the user explicitly requests that artifact.
- Read applicable instruction layers, role files, live references, Git status, and relevant diffs before editing. Preserve concurrent work and inspect ignored governance files directly.
- Consult current official OpenAI documentation when changing discovery, configuration, model, reasoning, or subagent behavior. Label human reports as anecdotal and project observations as local evidence.

## Put each rule at the narrowest durable layer

| Layer | Keep here |
|---|---|
| Global or user | Stable cross-project preferences, safety boundaries, execution and evidence principles |
| Repository root | Cross-module architecture and contracts, shared safety, generic ownership, common verification |
| Nested repository | Directory-specific runtime, commands, conventions, public interfaces, and focused checks |
| Role | Only behavior or restrictions that differ for that role |
| Task guide or Skill reference | Procedures needed only for a specific task type |
| Current task | Goal, authorization, progress, exceptions, concurrency, blockers, stop condition |

- Judge where guidance will execute, not where it is authored. Do not copy project rules into portable guidance merely because the file is being edited outside that project.
- Treat paths, installed tools, versions, model availability, and environment reachability as facts to resolve at runtime unless they are verified project contracts.
- Linked references should have clear loading triggers. Do not require unconditional reading of entire documentation folders.

## Simplify without losing decisions

- Keep a rule only when it changes a meaningful decision, belongs at that layer, and is not reliably recoverable from source, configuration, or tooling.
- Merge inherited duplicates and repeated workflow prose while preserving exact contractual wording, authorization gates, public-interface boundaries, and project-specific completion criteria.
- Remove old-model scaffolding, fixed output quotas, repeated status rituals, blanket rereads, unconditional checklists, and failure-specific workarounds that no longer change a decision.
- Prefer repository tooling, tests, linters, or CI for mechanically enforceable behavior. Do not add dependencies merely to reorganize instructions.
- Before retiring a guide or role, map all live references and unique rules. Move surviving content first, then verify dead links and callers; historical mentions may remain when they are not live instructions.
- Preserve explicit user choices and safety boundaries. Never claim that a shorter file improves quality, cost, or runtime behavior without measured evidence.

## Load detailed guidance only when needed

- When creating, splitting, or relocating global, root, nested, or tool-specific agent instructions, read [instruction-layering.md](references/instruction-layering.md).
- When changing delegation, worker ownership, subagent context, or model/reasoning routing, read [delegation-routing.md](references/delegation-routing.md).
- When changing compaction, task switching, handoffs, memory, or Context Brief policy, read [context-continuity.md](references/context-continuity.md).

## Verify and deliver

- Review the final instruction hierarchy for contradictions, unreachable references, duplicated authority, ambiguous ownership, and rules placed above their valid scope.
- Run relevant syntax, metadata, reference, and repository checks. Use application builds or E2E only when governance changes affect application behavior.
- If synchronized copies were requested, compare paths and content after the copy. Syntax checks do not prove that a client reloaded the new guidance.
- Report changed files, rules retained or moved, rules removed, actual checks, unresolved assumptions, and any runtime behavior not verified.
