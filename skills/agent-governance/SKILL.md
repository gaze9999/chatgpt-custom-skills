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
- Read the target guidance and relevant diffs before editing; preserve existing work. Start with narrow evidence and expand only to resolve a material gap. Use `scripts/scan_repo_structure.py` when a structural inventory is useful, not as a mandatory step.
- Check current official OpenAI documentation for discovery, configuration, or model behavior being changed. Reuse applicable evidence already in context; distinguish documented behavior, project observations, and tentative recommendations.
- Write concise English unless the user or project requires another language. Preserve substantive constraints when shortening; do not invent roles, capabilities, paths, or results.

## Match the target context

- Judge where the guidance will apply, not just where this Skill runs.
- Inside a known project, use applicable instructions and current evidence. Remove duplicated inherited rules and blanket reading reminders; retain project-specific constraints and task-triggered references. Omission does not waive inherited requirements.
- Outside the project but preparing guidance for it, identify the supplied target and its known instruction layers. Do not copy project rules merely because authoring happens elsewhere. Verify files when accessible and authorized; otherwise label the result as a draft and identify unverified assumptions.
- For non-project or unknown environments, keep guidance self-contained and portable. Include only supplied constraints and necessary discovery directions; do not assume local files, tools, automatic AGENTS.md loading, or shared chat history. Clarify missing information only when it changes scope, placement, or correctness.

## Place and simplify rules

- Global guidance holds durable cross-project preferences; repository guidance holds project-specific contracts and ownership; role files hold role differences; task prompts hold temporary scope and acceptance criteria.
- Keep a rule when it changes a meaningful decision, belongs at that layer, and is not reliably recoverable from source or tools. Merge repetition without weakening explicit requirements; retain exact wording when contractually significant.
- Replace blanket rereads with relevant loading triggers. Linked references are not automatically loaded in full. Keep briefs for orientation and authoritative sources for contract questions.
- Prefer existing formatters, tests, linters, or CI for mechanically enforceable checks. Do not add tooling or dependencies merely to reorganize instructions.
- Preserve safety, authorization, and public-contract boundaries. Avoid turning a past failure into a universal workflow or forcing fixed handoff formats, history lengths, task transitions, or output quotas without a concrete need.

## Delegation and model selection

- Prefer one agent for small or tightly coupled work. Delegate authorized, bounded work when quality, elapsed time, or context isolation benefits outweigh coordination and integration costs; role availability alone is insufficient.
- Parallelize independent work with clear ownership. Give workers the goal, necessary context, contracts, evidence pointers, constraints, acceptance criteria, and stop point. Use supported context-sharing options suited to the task. The primary agent owns integration and final acceptance; reuse verified findings and recheck material gaps or drift.
- Keep stable model-selection criteria in guidance and concrete defaults in maintained configuration. Preserve explicit user choices. Do not impose model rankings, fixed escalation chains, or profiles based solely on role labels.
- Assess model and reasoning together for the actual task, uncertainty, risk, tools, context, and verification burden. Meet quality requirements first, then compare latency and total cost, including retries and coordination. Treat unmeasured advantages as tentative.
- Verify supported combinations in the target environment or current official documentation. Diagnose missing context, unclear requirements, and environment failures before attributing difficulty to model capability. A recommendation does not switch models or authorize delegation or configuration changes.

## Verify and deliver

- Review the final changes and run relevant format, reference, and configuration checks. Check renamed roles and their callers, and inspect ignored governance files directly. Preserve required project gates without adding unrelated application checks.
- Verify synchronized copies when requested. Do not claim runtime loading, behavior improvement, or cost savings from syntax checks alone.
- Report changed files, key decisions, actual checks, unresolved assumptions, and unverified boundaries in a task-proportionate format. Separate passed, failed, not-run, and blocked checks where relevant.
