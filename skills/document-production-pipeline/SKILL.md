---
name: document-production-pipeline
description: Use this skill only when the user explicitly asks to create, compile, convert, polish, package, or deliver a finished downloadable document artifact such as PDF, DOCX, Markdown, or a multi-format document. Do not use it for brief chat answers, ordinary summaries, translation, proofreading, document planning, reusable Codex context briefs, post-implementation doc updates, Notion organization, image generation, spreadsheets-only work, or coding task prompts unless the user clearly wants a finished document file artifact.
---

# Document Production Pipeline

This Skill produces finished downloadable document artifacts from user requirements, source material, notes, research, screenshots, tables, existing text, or structured outlines.

The primary output is a real file artifact, not a chat-only answer, planning note, reusable Codex context brief, Notion organization task, or implementation prompt.

When the user does not specify an output format but clearly asks for a document file, default to `PDF`. When the user explicitly requests `DOCX`, `Markdown`, or multiple formats, follow the requested format.

## Strict activation requirements

Use this Skill only when all requirements are true:

1. The user wants a finished document artifact or a file deliverable.
2. The requested output format is explicit, or the wording clearly implies a document file, such as `PDF`, `DOCX`, `Markdown file`, `report`, `guide`, `handbook`, `manual`, `deliverable document`, or `downloadable file`.
3. The task requires document production work, such as structure, layout, citations, document metadata, file conversion, multi-format consistency, or QA validation.

Do not activate this Skill just because the request mentions `document`, `doc`, `Markdown`, `PDF`, `DOCX`, `summary`, `Notion`, `API`, `spec`, or `Codex`.

If the user asks only for a short chat answer, ordinary summary, translation, proofreading, outline, Notion organization, reusable Codex context brief, post-implementation memo update, spreadsheet workbook, coding task prompt, or direct implementation, route to the more appropriate workflow instead.

## When to use this skill

Use this Skill when the main deliverable is a finished file artifact, such as:

- creating a PDF, DOCX, Markdown, or multi-format document from provided material
- turning notes, research, screenshots, code explanations, tables, or outlines into a polished deliverable document
- compiling a tutorial, technical guide, report, comparison document, handbook, checklist, or reference manual
- converting an existing draft into a finished downloadable file
- producing a document that requires layout, table handling, citations, version metadata, or QA validation

Typical user wording includes:

- "將這段分析做成 PDF"
- "整理成 DOCX 教學文件"
- "同一份內容請輸出 PDF、DOCX 與 Markdown"
- "把這些資料做成正式文件並給我檔案"
- "產出可下載的技術文件"

## When not to use this skill

Do not use this Skill for:

- brief chat answers, ordinary explanations, or simple summaries without file output
- translation-only or proofreading-only tasks without a finished document artifact request
- document planning, outline brainstorming, or structure advice where no file deliverable is requested
- generic doc-to-Markdown conversion where the user only wants reusable Codex context; use Codex Context Brief Builder instead
- updating existing docs, Notion memos, changelogs, or context briefs after code changes; use Post-Implementation Doc Updater instead
- spreadsheet-only workbooks, tables, pivots, or Excel artifacts; use the spreadsheet workflow instead
- direct coding, debugging, refactoring, or coding task prompts
- image generation or editorial illustration tasks

If the requested result can be fully satisfied as a normal chat response and the user did not request a file, do not use this Skill.

## Pipeline contract

1. Confirm the document goal, audience, source material, output format, and non-negotiable constraints.
2. Load and follow [Document Production Guidelines](references/document-production-guidelines.md) for non-trivial documents.
3. Build a clear information architecture before writing or converting content.
4. Preserve user-provided facts, numbers, terminology, source boundaries, and requested language.
5. Do not invent unsupported experience, results, APIs, versions, citations, publication data, research findings, or file paths.
6. Use reliable sources when external facts are needed; verify unstable or current information before using it.
7. Create the actual requested file artifact rather than only pasting the document text in chat.
8. Run applicable deterministic QA scripts, then perform any available render / visual checks.
9. Only claim checks that were actually completed; mark unsupported checks as unverified.
10. Final response should provide the file link, completed validation, and unverified limitations.

## Inputs

Users may provide natural-language requirements rather than fixed fields. Common inputs include:

- topic and purpose
- target audience
- existing text, screenshots, tables, code snippets, notes, or attachments
- requested outline or sections
- language and writing style
- desired depth, page count, or length
- output format: PDF, DOCX, Markdown, or multiple formats
- citation / source requirements
- document version or program version
- layout, table, chart, TOC, or pagination requirements

Do not fill missing information as fact. Ask only when the missing detail blocks correctness, file creation, citation quality, target format, or user authorization.

## Format selection

- If the user clearly asks for a document file but omits the format, output `PDF` by default.
- If the user asks for `DOCX`, output an editable Word document.
- If the user asks for `Markdown`, `MD`, or a `.md` file, output Markdown.
- If the user asks for multiple formats, build from one canonical content source and keep facts, structure, terminology, numbers, and citations aligned.
- Do not silently convert between formats when it would remove content, citations, tables, or layout-critical information.

## Document content rules

- Start from information architecture, then expand details.
- For technical or instructional documents, prefer concept → implementation and abstract → concrete reading order.
- Add examples, templates, checklists, diagrams, or tables only when they improve understanding.
- Keep similar examples in the same chapter or subsection.
- Explain terms when first needed, but do not repeat stacked definitions.
- Preserve user-provided facts, dates, numbers, domain terms, technical level, and core intent.
- Avoid filler, empty sections, speculative claims, and unsupported conclusions.
- Avoid the phrasing pattern `不是 OO，而是 XX` and similar repetitive contrast framing.

## Document metadata and filenames

- Keep filenames concise, recognizable, and suitable for academic or technical documents.
- Do not include version numbers in filenames unless the user explicitly requests it.
- Put version information inside the document.
- Include `文件版本`; default new documents to `v1` when the user does not specify.
- Use document versions as `v1`, `v2`, `v3`, etc.
- Include `程式版本` only when the document concerns software and the program version is confirmable.
- Format program versions as `x.xxx.xxx`, for example `1.004.012`.
- Do not invent program versions.

## Layout and format requirements

### PDF

- Ensure text renders correctly, especially Traditional Chinese, Japanese, and other actual document characters.
- Prefer selectable text and portable font handling; do not turn pages into images unless unavoidable.
- Check TOC page numbers, heading positions, table pagination, whitespace, clipping, and character rendering when rendering tools are available.

### DOCX

- Use native Word Heading styles for heading hierarchy.
- Use native Word TOC fields and `PAGE` / `NUMPAGES` fields when page numbers are needed.
- Enable field updates on open when appropriate, but still mark actual Word pagination as unverified unless rendered or opened in a compatible environment.
- Use repeat header rows for unavoidable cross-page tables.
- Keep headings with following content when possible.

### Markdown

- Use a clean, continuous heading hierarchy.
- Do not simulate fixed PDF / Word pagination.
- Keep Markdown portable and readable.
- Use tables only when they improve comparison or scanning.

## Citations and research

- External sources must directly support the claims they are attached to.
- Technical content should prioritize official documentation, standards, source repositories, and primary technical references.
- Research, science, medical, health, pharmacy, psychology, and evidence-based professional content must use APA 7 style with in-text citations and final references when the document calls for formal citation.
- Include DOI links when available and relevant for APA references.
- Do not use unsupported secondary summaries as primary evidence when primary sources are required.
- Mark unverified or conflicting information explicitly.

## Deterministic QA scripts

`scripts/` contains repeatable structural checks. Execute scripts directly; do not read script source into context unless a script fails or needs modification.

Run the script matching each output format:

```text
PDF      → python scripts/validate_pdf.py <file.pdf>
DOCX     → python scripts/validate_docx.py <file.docx>
Markdown → python scripts/validate_markdown.py <file.md>
```

For APA 7 documents, also run:

```text
python scripts/validate_apa7.py <canonical.md>
```

Use `--require-doi` only when DOI presence is known to be required:

```text
python scripts/validate_apa7.py <canonical.md> --require-doi
```

Script outputs use `PASS`, `WARN`, `FAIL`, `INFO`, and `SUMMARY`. Summarize only necessary results in the final response.

Script limits:

- `validate_pdf.py` checks basic PDF structure only; it cannot replace visual QA for fonts, clipping, TOC pagination, table breaks, or whitespace.
- `validate_docx.py` checks OOXML structure, headings, TOC / page fields, update fields, and table headers; it cannot replace Word pagination QA.
- `validate_markdown.py` checks heading hierarchy, code fences, and version markers; it does not validate factual correctness.
- `validate_apa7.py` is a heuristic citation and DOI-format check; it does not validate bibliographic metadata or source support.

## QA expectations

Before finalizing, check what the environment supports:

- file exists and opens or is structurally valid
- appropriate deterministic script was executed
- all `FAIL` results were fixed or clearly reported
- important `WARN` results were reviewed
- heading hierarchy and TOC structure are consistent
- tables, figures, and code blocks are not unnecessarily split or clipped
- fonts and multilingual characters render correctly when visual QA is possible
- document metadata and filename rules are followed
- multi-format outputs are factually aligned
- unsupported render, pagination, font, or visual checks are explicitly marked unverified

## Output behavior

- If inputs are sufficient, create the requested file artifact directly.
- If the user asks for a document file but omits format, create PDF.
- If the user asks for multiple formats, deliver all requested formats when supported.
- Do not just paste the full document text and claim a file was created.
- Do not expose internal reasoning or generation process.
- Final response should list file links, format notes, completed validation, and unverified checks.
