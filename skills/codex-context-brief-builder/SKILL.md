---
name: codex-context-brief-builder
description: Use this skill only when the user explicitly provides or identifies source material such as a specification, API document, requirements document, design contract, schema, integration guide, SDK docs, or similar implementation contract and asks to convert it into a reusable Codex-readable Markdown context brief for future coding use. Do not use it for ordinary summaries, doc-to-Markdown conversion, casual explanations, formal document artifacts, direct coding, post-implementation doc updates, Notion organization, or coding task prompts unless the user clearly wants a reusable Codex context brief.
---

# Codex Context Brief Builder

This Skill converts source specifications, API documents, requirements documents, schemas, integration guides, SDK docs, or similar implementation-contract material into a reusable Markdown context brief for Codex or coding agents.

The goal is to avoid repeatedly uploading or pasting the full source document. The output preserves implementation-relevant contracts in a compact, stable Markdown file that can be reused as coding context.

The goal is not ordinary summarization, general document conversion, polished document production, implementation work, or post-implementation documentation synchronization.

## Subagent delegation

Delegate only a bounded extraction, contract check, or validation subtask. Pass a compact handoff with the task goal, named source files or excerpts, verified contracts, relevant constraints, expected result, and stop condition. Do not pass the full user conversation or make a subagent inherit it; point to the source artifact when more evidence is needed.

## Strict activation requirements

Use this Skill only when all requirements are true:

1. The user provides, uploads, links, names, or otherwise identifies source material to read.
2. The source material contains implementation-relevant contracts, such as API behavior, schema fields, validation rules, workflows, business rules, UI states, auth, permissions, error handling, integration steps, or acceptance criteria.
3. The user wants a reusable Markdown context brief for Codex, a coding agent, or future implementation work.

Do not activate this Skill just because the request mentions `document`, `Markdown`, `API`, `spec`, `Notion`, `summary`, `PDF`, `DOCX`, or `Codex`.

If the user only asks to convert a document into Markdown, summarize a document, organize Notion, generate a formal file, or update docs after code changes, route to the more appropriate workflow instead.

## When to use this skill

Use this Skill when the user asks to create a reusable Codex / coding-agent context brief from source material such as:

- API specifications, OpenAPI excerpts, endpoint documents, SDK docs, webhook docs, or integration guides
- product requirements, technical specifications, feature specs, acceptance criteria, or business rules
- database schemas, event schemas, JSON examples, request / response contracts, or validation rules
- UI / UX specs when they define implementation behavior, states, copy, accessibility, or layout constraints
- migration notes, architecture decision records, or existing system descriptions that Codex must reuse later

Typical user wording includes:

- "把這份 API 文件整理成 Codex 用的摘要 MD"
- "幫我把規格書轉成之後給 Codex 看的 context brief"
- "整理成可重複使用的 coding agent 背景文件"
- "這份文件太長，幫我壓成不失真的 Codex reference"
- "把這份 SDK 文件整理成之後實作時可重複引用的 Markdown"

## When not to use this skill

Do not use this Skill for:

- ordinary article summaries, reading notes, meeting notes, or research notes
- generic doc-to-Markdown conversion where the user does not request future Codex / coding-agent reuse
- direct coding, debugging, refactoring, or implementation work
- generating a task prompt for a single coding job; use Coding Task Prompt Builder instead
- updating docs or memos after implementation changes; use Post-Implementation Doc Updater instead
- polished PDF / DOCX / formal document production; use Document Production Pipeline instead
- general Notion organization, database cleanup, page sorting, or workspace restructuring
- unsupported source material that cannot be read, extracted, or verified enough to preserve contracts

If the request can be completed as a normal summary or document conversion without preserving implementation contracts for future Codex use, do not use this Skill.

## Input handling

Accept source material from uploaded files, pasted text, screenshots with readable content, repository files, or connector documents when available.

Before writing the brief:

1. Identify the source type, source boundary, and intended future coding use.
2. Confirm that the output target is a reusable Markdown context brief, not a formal document or a one-off task prompt.
3. Preserve exact contracts, names, endpoint paths, field names, enum values, status codes, constraints, and examples that affect implementation.
4. Compress prose, rationale, marketing text, screenshots, and repeated background content.
5. Keep uncertainty explicit. Never turn missing, ambiguous, extracted, or conflicting source information into confirmed facts.
6. If multiple source files are provided, keep their boundaries visible in the output when that helps future traceability.

Only ask follow-up questions when missing information affects source coverage, reusable scope, output target, or coding correctness.

## Source extraction workflow

When the source material is a PDF, DOCX, XLSX, CSV, TXT, Markdown, JSON, YAML, or similar file and script execution is available, extract text first instead of manually reading every page or sheet into context.

Use:

```bash
python scripts/extract_source_text.py <source-file> --out <extracted-source.md>
```

For quick inspection, stdout is acceptable:

```bash
python scripts/extract_source_text.py <source-file>
```

For an explicitly requested, bounded OCR fallback on uploaded scanned PDFs or embedded OOXML images:

```bash
python scripts/extract_source_text.py <source-file> --ocr-fallback --ocr-max-items 20 --ocr-lang eng
```

OCR is never the default. Use it only when native extraction is missing or insufficient, or when an important source image needs transcription. It first tries the optional `rapidocr` + `onnxruntime` Python packages listed in `requirements.txt`; their first use may provision local OCR models and their default model supports Chinese and English. If unavailable, it can use locally available Tesseract language data; `--ocr-lang` controls that Tesseract fallback. PDF OCR also requires Poppler `pdftoppm`. OCR-derived text includes source location, engine, and confidence, and must remain partial source coverage until verified against the original visual source.

Supported extraction targets:

- `.pdf`: tries optional `pypdf`, `pdfplumber`, `PyPDF2`, or `pdftotext` when available; optional OCR can process bounded rendered pages.
- `.docx`: extracts paragraphs, tables, headers, footers, footnotes, and endnotes from the OOXML package using Python standard library; optional OCR can process bounded Word media images.
- `.xlsx`: extracts worksheet cell values and shared strings from the OOXML package using Python standard library; optional OCR can process bounded Excel media images.
- `.pptx`: optional OCR can process bounded PowerPoint media images, but does not replace slide text extraction.
- `.csv` / `.tsv`: extracts rows into compact text lines.
- `.txt`, `.md`, `.markdown`, `.json`, `.yaml`, `.yml`: reads text directly with common encodings.

Use the extracted text as a working base, not as unquestioned truth. Mark source coverage as partial or unverified when extraction is missing, lossy, truncated, OCR-dependent, table-heavy, image-only, or structurally ambiguous.

`requirements.txt` contains the optional Python dependencies used by this reader. Use the bundled runtime first; install missing dependencies only with user authorization. System executables such as Poppler and Tesseract are deliberately not listed as pip dependencies.

Normal usage should execute the script directly. Do not read the script source into context unless the script fails or needs modification.

## Output contract

Create a real Markdown artifact when the environment supports file creation. If file creation is not available, output the Markdown content directly.

Recommended filename pattern:

```text
<source-or-project-name>_Codex_Context_Brief.md
```

Do not include a version number in the filename unless the user explicitly requests it. If the source document has a confirmed version, put it inside the Markdown metadata section.

The output must remain a Codex context brief. Do not expand it into a full tutorial, polished handout, general knowledge article, or formal PDF / DOCX-style document.

## Markdown structure

Use this structure when applicable. Omit sections with no useful content, but keep Metadata, Scope, Implementation-relevant summary, Implementation guidance for Codex, Open questions / unresolved items, and Source traceability unless truly inapplicable.

```markdown
# <Project / Feature / API> Codex Context Brief

## Metadata

- Source: <file / URL / pasted material / repository path>
- Source version: <confirmed version or "Unconfirmed">
- Brief date: <date if available>
- Intended use: <how Codex should use this brief>
- Source coverage: <complete / partial / unverified and why>

## Scope

<What this brief covers and what it does not cover.>

## Implementation-relevant summary

<Short summary of the system, feature, or integration from an implementation perspective.>

## Contracts and invariants

<Rules, constraints, guarantees, compatibility requirements, non-negotiable behavior.>

## API / Interface reference

### <Endpoint / Method / Component / Schema>

- Purpose:
- Method / path:
- Auth:
- Request:
- Response:
- Errors:
- Constraints:
- Example:
- Notes for Codex:

## Data model / schema

<Field names, types, required flags, enums, validation, relationships.>

## Workflows and state transitions

<User flows, backend flows, async jobs, webhook/event flows, edge cases.>

## Error handling and edge cases

<Errors, retries, idempotency, rate limits, pagination, nullability, fallback behavior.>

## Security, privacy, and permissions

<Auth, scopes, PII, secrets, access control, logging constraints.>

## Implementation guidance for Codex

<How Codex should use the brief during implementation. Include boundaries and common mistakes to avoid.>

## Open questions / unresolved items

<Unknowns, conflicts, missing source details, assumptions that need confirmation.>

## Source traceability

<Short source map, citations, page / section references, or repository paths when available.>
```

## Compression rules

Preserve:

- endpoint paths, method names, event names, component names, schema names, field names, enum values, status codes, and validation rules
- request / response examples when they prevent ambiguity
- security, auth, permission, rate limit, pagination, idempotency, and error-handling rules
- acceptance criteria, business rules, state transitions, edge cases, and observable UI behavior
- source version, date, coverage, and traceability when available

Compress or remove:

- marketing language, long introductions, repeated overview text, screenshots that do not define behavior, and implementation-irrelevant narrative
- duplicated examples that do not add new contract information
- outdated sections, unless they define compatibility risks or migration constraints

## Deterministic validation script

After producing a Markdown context brief, run the validator when script execution is available:

```bash
python scripts/validate_context_brief.py <brief.md>
```

For machine-readable output, use:

```bash
python scripts/validate_context_brief.py <brief.md> --json
```

For stricter release-quality checking, use:

```bash
python scripts/validate_context_brief.py <brief.md> --strict
```

The script checks Markdown structure, recommended context brief headings, balanced code fences, Codex intended-use markers, implementation-relevant signal categories, source coverage, source traceability markers, unresolved item markers, and common secret patterns.

Script limits:

- It does not verify that the source material actually supports the brief's claims.
- It does not guarantee full API correctness, completeness, or compatibility.
- `WARN` means the issue may be acceptable for a specific brief, but should be reviewed before reuse.

Normal usage should execute the script directly. Do not read the script source into context unless the script fails or needs modification.

## Codex usability rules

- Write for future coding use, not for general readers.
- Prefer precise bullets, tables, and compact examples over long prose.
- Keep implementation boundaries explicit.
- Mark assumptions as `Assumption`, missing details as `Open question`, and conflicting source content as `Conflict`.
- Mark extraction gaps as `Source coverage: partial` or `Source coverage: unverified`.
- Do not invent APIs, fields, errors, versions, behavior, dependencies, file paths, or tests.
- Do not include secrets, credentials, private tokens, or unnecessary personal data.
- If the source is too large, create the brief in passes and preserve source traceability.

## Final response

Keep the final response short. Include:

- generated Markdown file link or the produced Markdown content
- source coverage summary
- extraction result when source extraction script is used
- validator result when executed
- important unresolved questions or unverified parts
- whether the brief is suitable to reuse as Codex context
