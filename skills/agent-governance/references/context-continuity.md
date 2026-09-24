# Context continuity

Use this reference only when governance work changes compaction, task switching, handoffs, memory, or Context Brief behavior.

- Do not impose a fixed number of messages, compactions, tokens, or elapsed hours for starting another task. Continue while one outcome remains active and retained state is reliable.
- A long-lived coordinator can retain decisions, progress, and next-step ordering while an authorized separate task owns a bounded phase. A title such as Planner does not by itself change the current task's execution responsibility.
- Keep one coupled outcome in its current task through implementation and verification. With explicit user authorization, create a separate user-owned task for a distinct deliverable, repository, branch, or independent multi-turn workstream, or when unrelated accumulated context causes repeated recovery, contradiction, or lost constraints. A prompt-only step is unnecessary when direct execution is authorized.
- Fork a task when a new direction needs its completed conversation history. Forking carries that history and is not a context reset; use a fresh task with a compact handoff to leave stale history behind. Use a temporary side conversation only for a focused detour that does not need its own durable owner.
- Distinguish conversational transfer from a worktree handoff: the latter moves the same task and Git state between checkouts. Before starting a task or fork, confirm its checkout, starting Git state, uncommitted changes, ignored instructions, and file ownership; do not assume they transfer by default.
- Subagents serve bounded slices inside the current task when the delegation rules apply. For a separate task, pass confirmed facts and acceptance criteria, then read its result and inspect the relevant work before integrating it into the coordinator's progress.
- Use a Context Brief only for reusable implementation contracts from identified specifications, APIs, schemas, integration guides, or acceptance criteria. It is not a transcript, progress recap, or routine compaction artifact.
- Use a compact handoff for current task state. Preserve only the outcome, confirmed contracts, changed files, actual checks, unresolved boundaries, and next concrete step needed to resume.
- Reuse verified evidence within its source and environment limits. Recheck facts that may have changed or whose original scope does not cover the new task.
