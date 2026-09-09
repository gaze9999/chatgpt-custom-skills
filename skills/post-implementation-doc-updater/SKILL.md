---
name: post-implementation-doc-updater
description: Use this skill only when the user explicitly asks to update or synchronize existing documentation, Markdown notes, Notion memos, changelogs, API references, or Codex context briefs with concrete implementation-change evidence in the current task, such as code diffs, commits, pull requests, releases, migrations, completed refactors, changed-file lists, or pasted code-change summaries. Do not use it for general Notion work, ordinary document writing, standalone summaries, pre-implementation spec or API brief creation, direct coding, or coding task prompts. Do not update Notion unless the user explicitly names a Notion target for this implementation-backed update. Update both Notion and local Markdown only when both targets are explicitly requested or existing sync metadata clearly marks a bidirectional Notion-Markdown relationship.
---

# Post-Implementation Doc Updater

This Skill updates existing documentation and memo material after implementation changes. It is for keeping docs, Markdown notes, Notion memos, changelogs, API references, and Codex context briefs aligned with actual code changes.

The goal is not to write new documentation from scratch. The goal is to inspect a concrete implementation-change source, identify what existing documentation is affected, update only the necessary doc or memo surfaces, and avoid inventing behavior that is not supported by the change evidence.

## Strict activation requirements

Use this Skill only when all requirements are true:

1. The user explicitly asks to update, reconcile, sync, refresh, or align existing documentation / memo content.
2. The request is grounded in concrete implementation-change evidence available in the current task: a diff, commit, PR, release, migration, changed files, completed refactor, or pasted code-change summary.
3. There is at least one identifiable documentation or memo target, such as a repo Markdown file, README, changelog, docs path, API reference, Notion page, or Codex context brief.

Do not activate this Skill just because the request mentions `Notion`, `docs`, `Markdown`, `memo`, `API`, `Codex`, or `sync`.

If implementation evidence is missing, ask for the diff / commit / PR / release / migration note / changed-file list / code-change summary before proceeding as this Skill.

If the task can be completed by a general Notion workflow, document generation workflow, source-spec summarization workflow, or coding-prompt workflow without implementation-change evidence, do not use this Skill.

## When to use this skill

Use this Skill when the user asks to update existing docs or memos from implementation evidence such as:

- git diffs, commits, branches, pull requests, releases, or changed-file lists
- completed feature work, bug fixes, migrations, refactors, or configuration changes
- updated API contracts, request / response schemas, CLI commands, environment variables, setup steps, or deployment behavior
- user-facing behavior changes that should be reflected in README, docs, memo, Notion, changelog, or Codex context files

Typical user wording includes:

- "這次改版完幫我更新文件"
- "根據目前 diff 更新 memo"
- "根據 PR 內容更新這個 Notion release memo"
- "功能改完後同步更新 repo docs"
- "根據這次 commit，把本地 md 和 Notion memo 都更新"
- "更新 Codex context brief，讓它符合目前程式狀態"

## When not to use this skill

Do not use this Skill for:

- ordinary Notion page organization, database cleanup, folder/category sorting, or knowledge-base restructuring
- creating, writing, rewriting, polishing, summarizing, or translating documents without implementation-change evidence
- general Notion-to-Markdown or Markdown-to-Notion synchronization unrelated to code changes
- direct coding, debugging, refactoring, or implementation work
- turning a requirement into a coding prompt; use Coding Task Prompt Builder instead
- converting source specs or API docs into reusable Codex context before implementation; use Codex Context Brief Builder instead
- producing polished PDF / DOCX / formal document artifacts; use Document Production Pipeline instead
- casual summaries, meeting notes, research notes, or general explanations with no implementation-backed doc synchronization target

If the request can be completed by a general Notion/document skill without referencing code changes, do not use this Skill.

## Ambiguous request handling

Use the stricter interpretation when a request overlaps with other skills:

| User intent | Route |
|---|---|
| Read a spec / API doc and make a reusable Codex brief before coding | Codex Context Brief Builder |
| Make a polished PDF / DOCX / Markdown document artifact | Document Production Pipeline |
| Organize, move, rename, or classify Notion pages/databases | Notion workflow, not this Skill |
| Convert a coding requirement into a single task prompt | Coding Task Prompt Builder |
| Update existing docs or memos from a concrete implementation diff / PR / commit | This Skill |

When the user says only "更新文件" or "同步 Notion" without implementation evidence, ask for the missing change evidence or target instead of assuming this Skill applies.

## Inputs

Accept change evidence from:

- repository diffs, commits, branches, pull requests, release notes, or changed-file lists
- pasted code-change summaries
- existing Markdown docs, README files, changelogs, memo files, or Codex context briefs
- Notion pages or databases only when the user explicitly requests Notion updates for the implementation change
- an explicitly uploaded PDF only as optional implementation-change evidence; it is not a Markdown or Notion sync target

When evidence is incomplete, ask only for information that affects correctness, target location, or update authorization.

## Evidence confidence

Prefer direct implementation evidence over summaries:

1. Diff hunks and changed files: highest confidence.
2. PR or commit plus changed-file list: high confidence.
3. Release note or migration note tied to code changes: medium confidence.
4. User-provided implementation summary without diff: usable but mark as summary-based.

Do not claim a behavior changed unless the evidence supports it. When only a summary is available, label the resulting documentation update as based on supplied summary rather than verified diff.

## Change impact rules

Update documentation when the change affects:

- public API, endpoint, SDK, CLI, schema, event, or integration behavior
- user-facing behavior, UI state, validation, copy, flow, accessibility, or permissions
- setup, install, build, run, deploy, environment variables, configuration, or migration steps
- breaking changes, compatibility constraints, limitations, deprecations, or known risks
- documented architecture, file structure, module boundaries, or agent / automation behavior

Usually do not update documentation for:

- internal refactors with no observable behavior change
- tests only, formatting only, lint-only changes, or internal variable renames
- dependency or version changes that do not affect setup, compatibility, or public behavior
- generated files or build artifacts without user-facing relevance

When unsure, mark the update as `maybe` and explain what evidence is missing.

## Notion update gate

Do not read, search, or update broad Notion workspaces just because the request mentions docs, memo, or sync. For a permitted target, use the exact-target reader and writer rules in [Notion Sync Reader and Writer Contract](references/notion-sync-reader-writer-contract.md). An uploaded Notion JSON snapshot may be inspected locally, but it does not authorize a live Notion write.

Use Notion only when at least one of these is true:

- the user explicitly asks to update a Notion page, Notion database item, or Notion memo for this implementation change
- the user provides a Notion target or the current context already contains a specific Notion target
- existing Markdown metadata clearly links the target to Notion, such as `notion_page_id`

If Notion is not explicitly in scope, leave Notion unchanged and mention that only repo / Markdown documentation was updated.

## Notion and Markdown dual-update rule

Do not update both Notion and local Markdown by default.

Update both Notion and local Markdown only when one of these is true:

- the user explicitly asks to update both Notion and local Markdown
- the user provides both a Notion target and a Markdown target for the same implementation-backed update
- the target Markdown frontmatter or existing metadata contains a Notion page ID and `sync_mode: bidirectional`

If only one side is named, update only that side and mention that the other side was left unchanged.

If both sides changed independently, do not overwrite either side automatically. Produce a conflict note and ask for direction or present a merge plan.

## Canonical source strategy

Prefer a version-controlled Markdown file as the canonical source when both local Markdown and Notion are involved.

Default strategy:

1. Update repo Markdown / docs first.
2. Mirror or summarize the relevant update into Notion only when dual-update conditions are met.
3. Keep Notion and Markdown content semantically aligned, but do not assume identical formatting.
4. Preserve Notion page IDs, Markdown frontmatter, source links, and last-synced metadata when present.

If the user explicitly identifies Notion as the canonical source, follow that direction and mark the chosen canonical source in the update summary.

## Recommended workflow

1. Identify implementation-change evidence, target documentation surfaces, and requested write scope.
2. If the request lacks implementation-change evidence, do not proceed as this Skill; ask for the diff / PR / commit / change summary or route to the more appropriate document or Notion workflow.
3. When repository scanning is available, run `scripts/scan_changed_files.py` before reading large diffs manually.
4. Load [Doc Update Rules](references/doc-update-rules.md) when making non-trivial doc or memo updates.
5. Classify changed files by doc impact: `yes`, `maybe`, or `no`.
6. Read only the relevant diffs and current doc sections needed for the update.
7. Produce a minimal doc update plan before broad edits.
8. Update only affected docs, memos, changelogs, Notion pages, or Codex context briefs.
9. Run `scripts/validate_doc_update_plan.py` when a plan is produced.
10. Report changed files, skipped doc surfaces, unresolved questions, and validation status.

## Deterministic helper scripts

Use scripts as short-output helpers. Execute them directly; do not read the script source into context unless a script fails or needs modification.

Scan changed files:

```bash
python scripts/scan_changed_files.py --repo <repo-root>
```

Scan a specific diff file:

```bash
python scripts/scan_changed_files.py --diff-file <diff.patch>
```

Validate an update plan:

```bash
python scripts/validate_doc_update_plan.py <doc-update-plan.md>
```

Machine-readable output:

```bash
python scripts/scan_changed_files.py --repo <repo-root> --json
python scripts/validate_doc_update_plan.py <doc-update-plan.md> --json
```

## Sync target readers and writers

Before a dual Markdown / Notion update, inspect the one explicit Markdown target:

```bash
python scripts/inspect_markdown_sync_target.py <target.md> --json
```

The reader reports the target's SHA-256, frontmatter, heading structure, Notion page IDs / URLs, and `sync_mode`. It does not scan a directory or write a file.

To replace an explicitly approved Markdown target, first preserve the reader's SHA-256 and prepare the full replacement content as a UTF-8 file. Use a dry run before the real write:

```bash
python scripts/write_markdown_sync_target.py <target.md> --content-file <replacement.md> --expected-sha256 <reader-sha256> --dry-run
python scripts/write_markdown_sync_target.py <target.md> --content-file <replacement.md> --expected-sha256 <reader-sha256>
```

The writer refuses to replace a target whose SHA-256 changed after inspection. It has no directory mode, no automatic merge, and no Git commit / push behavior.

For an uploaded Notion page snapshot or API export, inspect one explicit JSON file:

    python scripts/inspect_notion_sync_target.py <uploaded-notion-snapshot.json> --page-id <optional-page-id> --json

The reader reports the uploaded snapshot SHA-256, page ID, URL, last-edited time, properties, direct-block count, and completeness markers. It does not accept tokens, connect to Notion, search a workspace, or write to Notion. It validates only the supplied snapshot, not the current remote Notion page.

For a live Notion update, use the available connector only after the Notion gate and dual-update rule pass. Follow [Notion Sync Reader and Writer Contract](references/notion-sync-reader-writer-contract.md): read the exact target before writing, make the smallest exact change, then re-read the same target. Do not store tokens or emulate a Notion client in a local script.

When an explicit append-only Notion update is authorized, the scripted writer accepts only a page ID, uploaded prepared Notion block JSON, an immediate prior last-edited time, and an environment-only token:

    NOTION_TOKEN=<environment-only-token> python scripts/write_notion_sync_target.py --page-id <page-id> --blocks-file <prepared-blocks.json> --expected-last-edited-time <reader-time> --dry-run
    NOTION_TOKEN=<environment-only-token> python scripts/write_notion_sync_target.py --page-id <page-id> --blocks-file <prepared-blocks.json> --expected-last-edited-time <reader-time> --json

It appends prepared blocks only after the last-edited-time guard passes, then re-reads the page. It does not search, delete, move, replace existing blocks, create pages, or accept a token argument.

When the user uploads a PDF as optional evidence, inspect its bounded text extraction:

    python scripts/inspect_pdf_sync_source.py <uploaded.pdf> --max-pages 20 --json
    python scripts/inspect_pdf_sync_source.py <uploaded.pdf> --max-pages 20 --ocr-fallback --ocr-lang eng --json

The PDF reader reports a source SHA-256, page count, extraction bound, page text, and reader engine. It prefers `pypdf`, with `pdfplumber` as a Python-library fallback. With `--ocr-fallback`, it uses optional `rapidocr` + `onnxruntime` first for pages with insufficient native text, then Tesseract only when RapidOCR is unavailable, and retains OCR text, engine, and confidence separately. It does not render, edit, or infer visual layout, and it does not authorize a documentation or Notion write by itself.

Script limits:

- The changed-file scanner classifies likely doc impact from file paths and diff hints; it does not prove behavior changed.
- The plan validator checks structure and risk markers; it does not verify that every claim is fully supported by the diff.
- The Markdown reader reports only one explicitly named file; it does not establish that Notion access is authorized.
- The Markdown writer is a guarded full-file replacement; it does not merge concurrent changes or verify factual alignment.
- The Notion reader / writer contract depends on an available connector and cannot validate Notion permissions, rendering, or workspace-wide consistency.
- OCR is optional. The local `requirements.txt` provides the Python OCR path; its first use may provision local OCR models and its default model supports Chinese and English. `--ocr-lang` applies to the Tesseract system-level fallback. OCR-derived page text is partial evidence and does not verify tables, layout, handwriting, stamps, or image semantics.
- Script `WARN` entries must be reviewed before applying documentation updates.

## Update plan structure

Use this concise plan when the update is more than a trivial one-file doc edit:

```markdown
# Post-Implementation Doc Update Plan

## Activation gate

- Existing doc / memo update requested:
- Implementation-change evidence present:
- Target surface identified:
- Notion explicitly in scope:
- Dual Notion / Markdown update authorized:

## Change evidence

- Source:
- Range / commit / PR:
- Evidence coverage:
- Evidence confidence:

## Impact summary

| Area | Impact | Evidence | Doc action |
|---|---|---|---|

## Target updates

| Target | Action | Reason | Status |
|---|---|---|---|

## No-update decisions

| Change | Reason docs are not updated |
|---|---|

## Notion / Markdown sync

- Canonical source:
- Markdown target:
- Notion target:
- Dual-update authorization:
- Conflict handling:

## Risks and unresolved items

- Open question:
- Assumption:
- Conflict:
```

## Writing rules

- Tie every meaningful doc update to visible implementation evidence.
- Do not turn internal implementation details into public-facing promises unless the behavior is actually part of the public contract.
- Mark breaking changes, migrations, compatibility limits, deprecations, and operational risks explicitly.
- Preserve exact API names, config keys, field names, paths, command names, and version constraints.
- Keep docs concise; do not add long explanations when a small changelog or memo update is enough.
- Do not overwrite Notion or Markdown content blindly when both sides changed; produce a conflict note instead.
- Do not include secrets, private tokens, credentials, or unnecessary personal data.

## Final response

Keep the final response short. Include:

- implementation-change evidence used
- documentation or memo targets updated
- no-update decisions worth mentioning
- Notion / Markdown sync result when applicable, including whether both sides were explicitly authorized
- validation result and unverified items
