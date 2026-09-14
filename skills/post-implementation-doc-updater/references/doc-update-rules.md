# Doc Update Rules

Use these rules only when updating documentation or memos after concrete implementation changes.

This reference is not for general Notion organization, ordinary document writing, standalone summaries, pre-implementation spec summarization, Markdown / Notion synchronization unrelated to code changes, or polished document artifact production.

## Hard activation gate

Before using the post-implementation updater, all conditions must be true:

1. The user requested an update, sync, refresh, reconciliation, or alignment of existing documentation, memo, changelog, API reference, Notion page, Markdown file, or Codex context brief.
2. The update is grounded in implementation-change evidence available in the current task: diff, commit, PR, release, migration, changed files, completed refactor, or pasted code-change summary.
3. At least one target surface is identifiable: a repo docs path, README, changelog, Markdown file, Notion page/database item, API reference, or Codex context brief.

If any condition is missing, do not proceed as a post-implementation update. Ask for the missing evidence or target, or route to the appropriate document, Notion, context-brief, or coding-prompt workflow.

Do not activate this workflow solely because the request mentions `Notion`, `docs`, `Markdown`, `memo`, `API`, `Codex`, `release`, or `sync`.

## Evidence-first policy

Documentation updates must be grounded in observable implementation evidence:

- diff hunks
- changed file paths
- commit / PR descriptions
- existing docs that name the affected feature, API, workflow, or configuration
- release notes or migration notes supplied by the user
- user-provided code-change summaries when no direct diff is available

Evidence confidence:

| Evidence | Confidence | Rule |
|---|---|---|
| Diff hunks + changed files | Highest | May update confirmed behavior when the diff supports it. |
| PR / commit + changed-file list | High | Use commit text carefully; inspect relevant files when available. |
| Release or migration note tied to code changes | Medium | Mark unsupported details as unresolved. |
| User-provided implementation summary only | Lower | Label updates as summary-based and avoid claiming direct verification. |

Do not invent behavior, file paths, flags, APIs, versions, or user-facing guarantees.

## Routing boundaries

Use the stricter route when the request overlaps with other workflows:

| User intent | Correct workflow |
|---|---|
| Read a spec / API doc and make a reusable Codex brief before coding | Codex Context Brief Builder |
| Make a polished PDF / DOCX / Markdown artifact | Document Production Pipeline |
| Organize, move, rename, classify, or restructure Notion pages/databases | Notion workflow, not this Skill |
| Convert a coding requirement into a single task prompt | Coding Task Prompt Builder |
| Update existing docs or memos from a concrete diff / PR / commit / release / migration | Post-Implementation Doc Updater |

## Impact classification

Use `yes`, `maybe`, or `no` for documentation impact.

### `yes`

Use `yes` when the change affects documented contracts or user-observable behavior:

- public API, endpoint, SDK, CLI, event, schema, or integration contract
- environment variable, config key, setup command, build command, deploy step, or migration path
- user-facing UI behavior, validation, permissions, copy, state, error, or workflow
- breaking change, compatibility change, limitation, deprecation, or operational risk

### `maybe`

Use `maybe` when the file path or diff suggests a possible doc impact but the behavior is not clear:

- internal module restructuring that may affect architecture docs
- UI refactor touching labels or state names
- dependency upgrade with possible setup or compatibility impact
- generated type changes without visible source context

### `no`

Use `no` when the change is unlikely to require docs:

- tests only
- formatting only
- lint-only changes
- internal variable rename with no public contract impact
- generated artifacts with no semantic change
- local tooling changes not exposed to users or maintainers

## Documentation target selection

Choose the smallest documentation surface that keeps knowledge aligned.

| Change type | Likely target |
|---|---|
| user-facing feature | README, docs, memo, Notion page only if requested |
| public API change | API reference, Codex context brief, changelog |
| config / env change | setup docs, deployment docs, README |
| breaking change | changelog, migration guide, release note |
| internal architecture change | architecture doc, Codex context brief, memo |
| bug fix with user-visible effect | changelog or memo when relevant |

Do not create a new documentation surface unless the user asks for a new doc/memo or no existing target can represent the necessary update. Prefer patching the smallest existing section.

## Notion usage gate

Do not search, read, or update broad Notion workspaces just because Notion is connected or mentioned near docs/memo/sync language.

Use Notion only when at least one condition is true:

- the user explicitly asks to update a Notion page, Notion database item, or Notion memo for the implementation change
- the user provides a specific Notion target or the current context already contains one
- existing Markdown metadata clearly links the target to Notion, such as `notion_page_id`

If Notion is not explicitly in scope, leave it unchanged and state that only repo / Markdown documentation was updated.

## Markdown and Notion sync

Prefer Markdown as canonical when the content belongs to a repo and should be versioned.

Use Notion as canonical only when the user says the Notion page or database is the source of truth.

Update both Markdown and Notion only when at least one condition is true:

- the user explicitly asks to update both Markdown and Notion
- the user provides both Markdown and Notion targets for the same implementation-backed update
- existing metadata clearly indicates bidirectional sync, such as `notion_page_id` plus `sync_mode: bidirectional`

If only one side is named, update only that side and state that the other side was intentionally left unchanged.

When both Markdown and Notion need updates:

1. Identify the canonical source.
2. Update the canonical source first.
3. Mirror or summarize the relevant content to the secondary surface.
4. Preserve page IDs, frontmatter, URLs, and sync metadata when present.
5. If both sides changed independently, do not overwrite automatically; produce a conflict note.

## Safe update style

- Use concise language.
- Preserve exact public names: endpoint paths, fields, enums, config keys, commands, file paths, and error names.
- Separate confirmed behavior from assumptions.
- Mark unresolved items with `Open question`.
- Mark unsupported or conflicting evidence with `Conflict`.
- Avoid documenting speculative future behavior.
- Avoid leaking secrets, tokens, credentials, or unnecessary personal data.

## Validation expectations

Before finalizing, confirm:

- the hard activation gate is satisfied
- every meaningful doc change traces back to implementation evidence
- evidence confidence is stated when the evidence is indirect or summary-based
- every affected target is listed in the update plan or final summary
- important no-update decisions are recorded
- breaking changes and migrations are clearly marked
- Notion was only used when explicitly in scope
- dual Notion / Markdown updates were explicitly authorized or supported by sync metadata
- Notion and Markdown targets are semantically aligned when both are updated
- unverified items are explicitly labeled
