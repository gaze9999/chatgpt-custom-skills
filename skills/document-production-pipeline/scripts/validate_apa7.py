#!/usr/bin/env python3
"""Heuristic APA 7 presence validator for scientific/medical documents.

This does not prove that references are bibliographically correct. It checks for
basic signals required by the Document Production Pipeline: reference section,
in-text citations, DOI normalization, and likely incomplete DOI forms.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REFERENCE_HEADINGS = (
    "references",
    "reference",
    "參考資料",
    "參考文獻",
    "引用文獻",
)
IN_TEXT_RE = re.compile(r"\([A-ZÀ-ÖØ-Ý][^()]{0,80}?,\s*(?:19|20)\d{2}[a-z]?\)")
NARRATIVE_RE = re.compile(r"\b[A-ZÀ-ÖØ-Ý][A-Za-zÀ-ÖØ-öø-ÿ'’-]+\s+\((?:19|20)\d{2}[a-z]?\)")
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
DOI_URL_RE = re.compile(r"https://doi\.org/10\.\d{4,9}/\S+", re.IGNORECASE)
OLD_DOI_PREFIX_RE = re.compile(r"\bdoi:\s*10\.\d{4,9}/\S+", re.IGNORECASE)


def result(status: str, check: str, detail: str) -> None:
    print(f"{status}: {check} - {detail}")


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".markdown", ".txt"}:
        return path.read_text(encoding="utf-8")
    raise ValueError("This validator currently accepts Markdown or plain-text canonical content.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check basic APA 7 citation signals.")
    parser.add_argument("file", type=Path, help="Markdown or plain-text canonical document")
    parser.add_argument("--require-doi", action="store_true", help="Fail when no DOI URL is present")
    args = parser.parse_args()

    path = args.file
    failures = 0
    warnings = 0

    if not path.is_file():
        result("FAIL", "file", "file does not exist")
        return 2

    try:
        text = extract_text(path)
    except (UnicodeDecodeError, ValueError) as exc:
        result("FAIL", "input", str(exc))
        return 2

    lower = text.lower()
    found_heading = next((h for h in REFERENCE_HEADINGS if h.lower() in lower), None)
    if found_heading:
        result("PASS", "reference-section", f"detected heading/label: {found_heading}")
    else:
        failures += 1
        result("FAIL", "reference-section", "no recognizable References/參考資料 section detected")

    parenthetical = len(IN_TEXT_RE.findall(text))
    narrative = len(NARRATIVE_RE.findall(text))
    citation_count = parenthetical + narrative
    if citation_count:
        result("PASS", "in-text-citations", f"detected at least {citation_count} author-year citation patterns")
    else:
        failures += 1
        result("FAIL", "in-text-citations", "no author-year citation pattern detected")

    doi_tokens = DOI_RE.findall(text)
    doi_urls = DOI_URL_RE.findall(text)
    old_doi = OLD_DOI_PREFIX_RE.findall(text)

    if doi_urls:
        result("PASS", "doi-format", f"found {len(doi_urls)} https://doi.org/... DOI URLs")
    elif doi_tokens:
        warnings += 1
        result("WARN", "doi-format", "DOI detected but not normalized to https://doi.org/... form")
    else:
        status = "FAIL" if args.require_doi else "INFO"
        if args.require_doi:
            failures += 1
        result(status, "doi-format", "no DOI detected; acceptable only when cited sources genuinely have no DOI")

    if old_doi:
        warnings += 1
        result("WARN", "legacy-doi-prefix", f"found {len(old_doi)} legacy 'doi:' forms; prefer https://doi.org/...")
    else:
        result("PASS", "legacy-doi-prefix", "none detected")

    result("INFO", "scope", "this is a heuristic presence check; verify author names, dates, titles, journal metadata, italics, punctuation, and source support separately")
    print(f"SUMMARY: failures={failures} warnings={warnings}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
