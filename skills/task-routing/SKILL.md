---
name: task-routing
description: Choose between continuing a Codex task, creating a separate task, forking a conversation, and using subagents, then prepare a compact handoff when needed. Use for explicit routing questions or an authorized continuing coordinator, not ordinary implementation or AGENTS.md maintenance.
metadata:
  short-description: Task routing and context handoff
---

# Task Routing

Keep execution with the smallest owner that can complete and verify the outcome. A Planner title does not by itself require delegation, and a long conversation does not by itself require a new task.

## Check authority and capabilities

- Identify the current outcome, what the user authorized, whether a continuing coordinator role was assigned, and which decisions remain unresolved.
- Check whether the current environment actually supports creating tasks, forking conversations, using subagents, and choosing a checkout or worktree. This skill does not grant permission to use any of them. Create a separate user-owned task only when the user explicitly authorized that action; follow current user, project, and runtime limits for subagents and forks.
- If the selected route is unavailable or unauthorized, continue the work that remains in scope and describe the required handoff. Do not silently substitute a subagent for a requested user-owned task.
- Produce only a prompt or plan when the user requested that artifact. Otherwise complete authorized work or start the authorized execution route directly.

## Choose the owner

1. Continue in the current task when one outcome remains active, the steps depend on each other, or the task can still use its retained decisions reliably. A continuing Planner may directly complete small connected work and keep the current decisions, progress, and next-step order.
2. Create a separate task for a distinct, independently reviewable deliverable or a bounded phase that needs its own multi-turn implementation and follow-up. A continuing Planner can remain the coordinator, but must inspect the execution task's result before advancing its plan.
3. Fork a conversation when a different path needs the completed history of the current conversation. A fork carries that history; it does not clear stale context. When the aim is a clean context, use a fresh task with a compact handoff instead.
4. Use a subagent for a bounded slice inside the current task when independent ownership, parallel speed, or context isolation outweighs coordination and review cost. Keep dependent steps and shared-file edits with one owner. The parent integrates and verifies the returned work.
5. Use a temporary side conversation only for a focused detour that does not need a durable owner, when that feature is available.

Do not route work by a fixed number of turns, tokens, compactions, elapsed hours, or phase names. Resolve uncertain architecture or requirements with a capable owner before handing a known execution method to another agent. Do not claim a cost or quality gain without measured evidence.

## Transfer only useful state

- State the objective, confirmed decisions and source pointers, owned files or modules, must-preserve constraints, exclusions, acceptance criteria, unresolved questions, and stop condition. Include attempts and failure evidence when the next owner would otherwise repeat them.
- Name the execution environment: repository, branch, current checkout or new worktree, relevant uncommitted changes, and ignored or untracked instructions or files that must be present. Check the actual starting state; do not assume a new worktree inherits every local file.
- Send a compact task-specific handoff rather than the entire transcript or routine tool output. Fork only when carrying completed conversation history is useful.
- For a separate task, use the available task-management tools to follow its progress and read its final result. Check the relevant diff, verification, and open boundaries before integration; a completion message alone does not establish acceptance.
- A worktree handoff moves the same conversation and Git state between Local and Worktree. It is not a new task or a context reset. Keep project-specific document updates and model or role choices under their own instructions.
