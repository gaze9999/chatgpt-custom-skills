# Delegation and model routing

Use this reference only when governance work changes subagents, roles, worker ownership, or model and reasoning selection.

- Delegate only when current user, project, and environment policy allow it. The primary agent decides from workload, independence, context-isolation value, coordination cost, and acceptance burden.
- Keep small or tightly coupled work with one agent. Use the fewest workers that provide a clear quality, elapsed-time, or context-isolation benefit; subagents perform separate model and tool work and are not a token-saving claim.
- Parallelize only independent slices with disjoint ownership and no shared mutable state. Sequence dependent work and avoid duplicate investigation.
- Give a worker a self-contained goal, confirmed contracts, owned files or modules, must-preserve constraints, exclusions, evidence pointers, acceptance criteria, and stop condition. The primary agent owns integration and final acceptance.
- A substantial independent implementation may stay with one worker through discovery, edit, checks, and in-scope fixes. Prefer supported waiting and one batched final review over progress polling or repeated partial handoffs.
- Preserve explicit user model choices. Keep portable rules model-agnostic and concrete defaults in maintained configuration. Verify the target environment's supported models and reasoning levels from current official documentation.
- Route by uncertainty, risk, tools, public-contract impact, and verification burden rather than file count or role name. Account for retries, coordination, and integration when comparing cost or latency.
- Removing a model pin can cause inheritance; confirm the resulting effective configuration. A recommendation does not switch a model or grant delegation authority.
