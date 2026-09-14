---
name: post-implementation-doc-updater
description: Update or synchronize existing documentation only when the user explicitly requests it, verifiable implementation-change evidence exists, and a target document is identified.
metadata:
  short-description: Minimize documentation updates from implementation evidence
---

# Post-Implementation Doc Updater

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
- Run `scripts/scan_changed_files.py --repo <repo-root>` when impact discovery is needed. For multiple targets, use [Doc Update Rules](references/doc-update-rules.md) and validate the concise plan with `scripts/validate_doc_update_plan.py`.

## Notion and Markdown

- Do not read or write Notion unless Notion is explicitly requested.
- Only access a precise Notion target when the user identifies it or the Markdown target has an explicit relationship. Follow [Notion Sync Reader and Writer Contract](references/notion-sync-reader-writer-contract.md).
- Do not synchronize both systems by default. Do so only with explicit authorization, both targets, or `sync_mode: bidirectional` in Markdown.
- Before writing, use the relevant `inspect_*` script. For Markdown replacement, dry-run and verify SHA-256 first. Re-read a live Notion target immediately after writing.

## Delivery

Report the evidence used, updated targets, no-update decisions, Notion and Markdown synchronization outcome, and completed or skipped checks.
