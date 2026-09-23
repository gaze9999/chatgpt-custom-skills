# Delegation and model routing

Use this reference only when governance work changes subagents, roles, worker ownership, or model and reasoning selection.

- Delegate only when current user, project, and environment policy allow it. The primary agent decides from workload, independence, context-isolation value, coordination cost, and acceptance burden.
- Keep small or tightly coupled work with one agent. Use the fewest workers that provide a clear quality, elapsed-time, or context-isolation benefit; subagents perform separate model and tool work and are not a token-saving claim.
- Parallelize only independent slices with disjoint ownership and no shared mutable state. Sequence dependent work and avoid duplicate investigation.
- Give a worker a self-contained goal, confirmed contracts, owned files or modules, must-preserve constraints, exclusions, evidence pointers, acceptance criteria, and stop condition. The primary agent owns integration and final acceptance.
- A substantial independent implementation may stay with one worker through discovery, edit, checks, and in-scope fixes. Prefer supported waiting and one batched final review over progress polling or repeated partial handoffs.
- Preserve explicit user model choices. Keep portable rules model-agnostic and concrete defaults in maintained configuration. Verify the target environment's supported models and reasoning levels from current official documentation.
- Decide whether a slice executes a known approach or must determine the approach. Assign bounded execution to an efficient supported model; use a stronger reasoner when the root cause, architecture, or cross-system impact is unresolved. A difficult but bounded problem may need more effort without needing a broader model.
- Select a suitable model and reasoning level from the initial uncertainty, risk, tools, public-interface impact, and verification burden rather than stepping through every level. Account for retries, coordination, and integration when comparing cost or latency; do not claim savings without measured evidence.
- Pass confirmed findings to the next worker so it does not repeat the same investigation. Stop and reroute when attempts repeat the same failure, ownership expands, context is lost, or a new architecture decision is required; include facts, attempts, evidence, open questions, and affected files.
- Add a separate reviewer only when independent review adds meaningful coverage. The primary agent accepts the integrated result after focused verification, not solely from a worker's completion claim.
- Removing a model pin can cause inheritance; confirm the resulting effective configuration. A recommendation does not switch a model or grant delegation authority.
