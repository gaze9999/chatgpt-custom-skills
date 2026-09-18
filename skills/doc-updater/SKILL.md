---
name: doc-updater
description: Update or synchronize existing documentation only when the user explicitly requests it, verifiable implementation-change evidence exists, and a target document is identified.
metadata:
  short-description: Minimize documentation updates from implementation evidence
---

# Doc Updater

Use completed implementation changes to minimally align README files, Markdown, changelogs, API references, Notion memos, or Codex context briefs with verifiable behavior. This is not a workflow for authoring new documentation from scratch.

## Activation

Use only when all conditions hold:

- The user explicitly requests an update, alignment, or synchronization of existing documentation.
- A diff, commit, PR, release, migration, changed-file list, or usable code-change summary is available.
- At least one concrete documentation target is identified.

When evidence or a target is missing, request only the information needed for correctness or authorization. Use another workflow for ordinary authoring, summaries, translation, Notion organization, coding prompts, pre-implementation briefs, or formal document artifacts.

## Workflow

- Treat diffs and changed files as the highest-confidence evidence. When only a user summary exists, mark resulting claims `summary-based`.
- Update only documents affected by public APIs, user-visible behavior, installation or configuration, deployment, migrations, compatibility, or established architecture descriptions. Internal refactors without behavior change normally do not require updates.
- Read only the necessary diff and target sections, then make the smallest supported change. Do not promote internal details to public guarantees or add secrets or unnecessary personal data.
- When a current-state document has a paired history or archive, keep the current document limited to current behavior, active work, unresolved decisions, and the latest verification boundary. Move superseded status, completed batches, dated execution details, old sync records, and obsolete navigation to history after confirming unique evidence is retained.
- When identifiers are reformatted, apply the requested scheme to current records, record the old-to-new mapping in history, and preserve historical identifiers and anchors unless the user explicitly requests a historical rewrite.
- When a compatible Python runtime is available, resolve bundled scripts relative to this Skill: use `scripts/scan_changed_files.py --repo <repo-root>` when impact discovery is needed, and for multiple targets use [Doc Update Rules](references/doc-update-rules.md) with `scripts/validate_doc_update_plan.py`. Otherwise use equivalent repository and document inspection; do not require installing the optional toolchain.

## Local-first updates

- Update local documentation by default. Do not read or write Notion unless the user explicitly requests Notion work; a general documentation-sync request is not enough.
- Existing page links, paired targets, prior sync arrangements, and `sync_mode: bidirectional` identify relationships, not permission to resume paused Notion synchronization.
- Complete authorized local updates without waiting for Notion access or alignment. Preserve sync metadata, but do not advance Notion sync timestamps or claim both copies are aligned.
- An explicit request to synchronize identified local and Notion targets is authorization for those targets; do not ask for duplicate confirmation. Resolve the exact targets and compare current content before writing, asking only if ambiguity would change scope or overwrite risk. Follow [Notion Sync Reader and Writer Contract](references/notion-sync-reader-writer-contract.md); do not blindly overwrite changes accumulated while sync was paused.
- For Markdown replacement, use the bundled inspection, dry-run, and SHA-256 helpers when compatible tooling is available, or an equivalent optimistic-concurrency check in the active environment.

## Delivery

Report evidence, local files changed, no-update decisions, and actual checks. When a Notion counterpart is relevant, state that it was intentionally not synchronized; do not treat this as a blocker for completed local work.
