---
name: codex-context-brief-builder
description: Convert explicitly provided implementation-contract material into reusable Codex Markdown context briefs; do not use for ordinary summaries or one-off coding tasks.
metadata:
  short-description: Create concise, traceable coding context briefs
---

# Codex Context Brief Builder

Compress specifications, API documentation, schemas, integration guides, or acceptance criteria into reusable Markdown context briefs for later implementation. Preserve exact contracts and source traceability; do not create ordinary summaries, formal document artifacts, or implementation changes.

## Activation

Use only when all conditions hold:

- The user provides or explicitly identifies readable source material.
- The material contains implementation-relevant contracts, such as behavior, fields, workflows, permissions, error handling, or acceptance criteria.
- The user wants a reusable Codex or coding-agent Markdown context brief.

Use the appropriate workflow instead for generic document conversion, ordinary summaries, Notion organization, formal PDF/DOCX output, a single coding prompt, or post-implementation documentation updates.

## Workflow

- Confirm source boundaries, intended use, and deliverable. Ask only when a gap affects correctness or coverage.
- Preserve names, paths, fields, enums, status codes, validation, security and permissions, errors, constraints, examples, and acceptance criteria.
- Compress marketing copy, repeated background, and implementation-irrelevant narrative. Do not turn gaps, conflicts, or OCR text into confirmed facts.
- Exclude secrets, credentials, private tokens, and unnecessary personal data unless the user explicitly requests retention. Preserve only the minimum source detail required for implementation.
- Preserve source boundaries across multiple inputs. For large material, extract only task-relevant sections.

## On-demand tools

- For PDF, DOCX, XLSX, or other structured files, run `scripts/extract_source_text.py <source-file>` first. Add `--ocr-fallback` only when native extraction cannot recover scanned content or essential images.
- Mark coverage as `partial` or `unverified` when OCR, tables, or extraction are insufficient, and retain source locations.
- Run `scripts/validate_context_brief.py <brief.md>` after creating the brief; use `--json` when machine-readable output is needed.

## Output contract

When writing is available, create a Markdown file named `<source-or-project-name>_Codex_Context_Brief.md`. Include Metadata, Scope, implementation summary, Contracts and invariants, implementation guidance, open items, and source traceability; add API, data-model, workflow, error, or security sections only when applicable.

In the final response, provide the output location, source coverage, completed checks, and material unresolved items.
