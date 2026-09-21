---
name: agent-governance
description: Audit, simplify, and restructure agent instructions and subagent guidance for a project or a portable handoff.
metadata:
  short-description: Agent governance, role boundaries, and instruction minimization
---

# Agent Governance

Keep the smallest instruction set that preserves task boundaries, contracts, and useful project knowledge. Prefer removing, merging, or relocating rules over adding them. User instructions override these defaults.

## Scope and evidence

- Keep audits and recommendations read-only; edit only when requested. Default edit scope is AGENTS.md, role configuration, and directly related governance documents. Do not expand into application code, dependencies, deployment, or external actions.
- When edits are requested, execute the authorized governance change through verification. Do not stop after producing a prompt, plan, or handoff unless the user explicitly requests that artifact instead of execution.
- Read the target guidance and relevant diffs before editing; preserve existing work. Start with narrow evidence and expand only to resolve a material gap. When available, resolve `scripts/scan_repo_structure.py` relative to this Skill and use it only when a structural inventory is useful; an unavailable helper does not block equivalent read-only discovery.
- Check current official OpenAI documentation for discovery, configuration, or model behavior being changed. Reuse applicable evidence already in context; distinguish documented behavior, project observations, and tentative recommendations.
- Write concise English unless the user or project requires another language. Preserve substantive constraints when shortening; do not invent roles, capabilities, paths, or results.

## Match the target context

- Judge where the guidance will apply, not just where this Skill runs.
- Inside a known project, use applicable instructions and current evidence. Remove duplicated inherited rules and blanket reading reminders; retain project-specific constraints and task-triggered references. Omission does not waive inherited requirements.
- Outside the project but preparing guidance for it, identify the supplied target and its known instruction layers. Do not copy project rules merely because authoring happens elsewhere. Verify files when accessible and authorized; otherwise label the result as a draft and identify unverified assumptions.
- For non-project or unknown environments, keep guidance self-contained and portable. Include only supplied constraints and necessary discovery directions; do not assume local files, tools, automatic AGENTS.md loading, or shared chat history. Clarify missing information only when it changes scope, placement, or correctness.

## Place and simplify rules

- Global or user-level guidance holds only explicitly durable cross-project preferences; a one-off choice remains task context. Repository guidance holds project-specific contracts and ownership; role files hold role differences; task prompts hold current authorization, progress, exceptions, concurrency, and stop points.
- Keep portable routing and verification principles at the global Skill layer, such as delegation cost, evidence honesty, proportional checks, and dependency safety. Keep named model defaults, framework/runtime versions, project commands, startup order, integration boundaries, and optional local runners in repository guidance or role files. Do not copy project-specific settings into the global Skill merely to centralize files.
- Treat paths, installed tools, versions, model availability, and runtime capabilities as environment facts to resolve when the task runs. Do not encode one computer's directory layout or tool set as a portable requirement; use relative workspace or Skill resources where practical.
- Keep a rule when it changes a meaningful decision, belongs at that layer, and is not reliably recoverable from source or tools. Merge repetition without weakening explicit requirements; retain exact wording when contractually significant.
- Audit accumulated guidance for old-model scaffolding, unconditional reading sequences, repeated status rituals, and blanket test instructions. More capable models can be hindered by obsolete recipes and conflicting detail; retain completion criteria, authority boundaries, and project contracts that still change decisions.
- Replace blanket rereads with relevant loading triggers. Linked references are not automatically loaded in full. Keep briefs for orientation and authoritative sources for contract questions.
- Before retiring a routing, validation, or handoff document, map every live reference and unique rule. Move stable shared rules to repository guidance, role-specific differences to role configuration, task-specific contracts to the narrowest triggered guide, and current status to task records. Delete the old file only after readback and dead-link checks; historical mentions may remain when they describe past state rather than a live instruction.
- Prefer existing formatters, tests, linters, or CI for mechanically enforceable checks. Do not add tooling or dependencies merely to reorganize instructions.
- Preserve safety, authorization, and public-contract boundaries. Avoid turning a past failure into a universal workflow or forcing fixed handoff formats, history lengths, task transitions, or output quotas without a concrete need.

## Delegation and model selection

- When applicable user, project, or Skill guidance authorizes discretion, let the primary agent decide whether to delegate from the actual workload, independence, context-isolation value, and coordination cost. Prefer one agent for small or tightly coupled work. Delegate authorized, bounded work only when quality, elapsed time, or context isolation benefits outweigh coordination and integration costs; the main model and role availability alone are insufficient.
- Do not present subagents as a token-saving mechanism. Each subagent performs separate model and tool work, so use the fewest agents that provide a clear quality, elapsed-time, or context-isolation benefit.
- Parallelize independent work with clear ownership. Give workers the goal, necessary context, contracts, evidence pointers, constraints, acceptance criteria, and stop point. Use supported context-sharing options suited to the task. The primary agent owns integration and final acceptance; reuse verified findings and recheck material gaps or drift.
- Keep stable model-selection criteria in guidance and concrete defaults in maintained configuration. Preserve explicit user choices. Do not impose model rankings, fixed escalation chains, or profiles based solely on role labels.
- Assess model and reasoning together for the actual task, uncertainty, risk, tools, context, and verification burden. Meet quality requirements first, then compare latency and total cost, including retries and coordination. Treat unmeasured advantages as tentative.
- Make the effective model and reasoning deliberate at delegation time. Use supported explicit overrides or a verified suitable default; omitted settings can inherit the parent and may be unsuitable for the slice. A fresh context does not imply a different model. Keep portable skills model-agnostic and place provisional named choices in target-specific guidance.
- Route by the work: bounded extraction, confirmed-result documentation, deterministic renames, and clear mechanical code changes under an approved plan are candidates for lower-cost settings when their affected surface and verification are bounded. Behavioral conclusions, public-contract renames, cross-layer compatibility judgment, and new architecture decisions require separate assessment. Implementing an approved structural plan differs from designing it. Split independent mechanical execution from uncertain decisions when useful, and escalate only the unresolved slice.
- A high-capability main model neither requires main-only execution nor justifies delegation by itself. It may retain tightly coupled work and delegate independent lighter slices to supported lower-cost models, while remaining responsible for integration and final acceptance.
- Do not force delegation for small coupled documentation or edits. Before removing model pins, check the resulting inheritance behavior and provide a deliberate selection path; removing defaults is not cost optimization.
- Verify supported combinations in the target environment or current official documentation. Diagnose missing context, unclear requirements, and environment failures before attributing difficulty to model capability. A recommendation does not switch models or authorize delegation or configuration changes.

## Context continuity

- Do not impose a fixed number of compactions, messages, or elapsed hours for starting a new conversation. Continue one conversation while it owns one outcome and retained state remains reliable; first-class compaction exists to support long-running work.
- Recommend a new conversation for a distinct deliverable, repository, branch, or independent workstream, or when accumulated unrelated context causes repeated loss, contradiction, or recovery work. Do not create or switch conversations without the authority required by the active environment.
- Use a reusable Context Brief only for implementation contracts from identified specifications, APIs, schemas, integration guides, or acceptance criteria. Use a compact handoff for current task state; do not turn a transcript, progress log, or compaction recap into a Context Brief.
- Before an authorized switch, preserve only the durable state needed to resume: outcome, confirmed contracts, changed files, actual checks, unresolved boundaries, and the next concrete step.

## Verify and deliver

- Prefer the fastest, simplest checks sufficient for the change. Preserve explicit requirements and project gates; do not add builds, browser checks, or E2E as routine ceremony. Use functional browser checks when the changed behavior needs them, not merely because another check is blocked.
- Keep project validation commands and runtime matrices in repository guidance, not in a portable global Skill. Role files may add only the differences needed by that role and should point back to shared project rules instead of duplicating full procedures.
- Preserve project dependency restrictions. Report and skip checks blocked by missing dependencies; do not retry an unchanged blocker or install, repair, or upgrade dependencies without authorization. Continue independent checks and never count a skipped check as passed.
- Keep validation preferences at their proper scope. If the user or project excludes dedicated accessibility/ARIA checks, preserve that exclusion without weakening existing accessibility behavior or necessary functional checks. Do not turn one project's exclusion into a global default. Keep current missing-package status in task context rather than permanent rules.

- Review the final changes and run relevant format, reference, and configuration checks. Check renamed roles and their callers, and inspect ignored governance files directly. Preserve required project gates without adding unrelated application checks.
- Verify synchronized copies when requested. Do not claim runtime loading, behavior improvement, or cost savings from syntax checks alone.
- Report changed files, key decisions, actual checks, unresolved assumptions, and unverified boundaries in a task-proportionate format. Separate passed, failed, not-run, and blocked checks where relevant.
