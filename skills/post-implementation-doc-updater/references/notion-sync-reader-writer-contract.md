# Notion Sync Reader and Writer Contract

Use this contract only for a concrete implementation-backed documentation update after the Post-Implementation Doc Updater activation gate has passed.

## Scope and access

- Use an explicit uploaded Notion JSON snapshot for offline reading, or the available Notion connector / first-party tool for live reading and writing. Do not add a personal access token, secret, or connector credential to this repository, a script argument, a document, or a log.
- Read or write only a page, database item, or memo named by the user, linked by the explicit Markdown target, or already identified in the current task.
- A Markdown reference authorizes Notion access only when its metadata contains a concrete `notion_page_id` and `sync_mode: bidirectional`; a URL alone requires user confirmation.
- Do not search, crawl, enumerate, or classify a broad Notion workspace to discover a sync target.

## Reader procedure

1. Read the exact target before planning an update. For an uploaded snapshot, run python scripts/inspect_notion_sync_target.py with that one JSON file and, when known, its page ID.
2. Record page ID or URL, title, relevant content blocks, child-page or database-item boundary, and any source / last-synced metadata.
3. Compare only the implementation-relevant sections with the canonical Markdown target. Treat Notion formatting as presentation; compare meaning, links, identifiers, tables, and constraints.
4. If the uploaded snapshot is incomplete, a connector truncates content, returns unknown blocks, or cannot read the exact target, stop and report that the Notion side is unverified.
5. If the Markdown and Notion sides have independent changes, report a conflict and do not overwrite either side.

## Writer procedure

1. Confirm a specific target and dual-update authorization before writing.
2. Fetch the exact target immediately before the write; use that snapshot as the concurrency baseline. The append-only script requires its last-edited time and an environment-only NOTION_TOKEN, while connector updates should use the connector's current page snapshot.
3. Apply the smallest exact replacement that aligns the implementation-backed change. Preserve page IDs, unrelated sections, page hierarchy, source links, and intentional Notion-only formatting.
4. Do not create, delete, move, or reorganize pages or database items unless the user explicitly asks.
5. Re-fetch the same target after writing. Verify the expected markers, content coverage, and no truncation or unexpected block conversion.
6. Report the target, changed section, canonical source, post-write verification, and any unverified layout or connector limitation.

The scripted writer accepts only prepared Notion child-block JSON and appends it. It cannot replace, delete, move, or reorganize existing blocks or pages. Use it only when an append is the smallest exact update.

## Failure handling

- Authentication failure, timeouts, rate limits, and ambiguous write results do not prove that no change occurred. Re-read the exact target before any retry.
- Never retry a broad workspace read or overwrite a target to resolve ambiguity.
- If a write cannot be verified, label it unverified and stop rather than claiming synchronization completed.
