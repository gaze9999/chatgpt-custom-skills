#!/usr/bin/env python3
"""Validate a Codex context brief Markdown file.

This script performs lightweight structural checks only. It does not verify that
source material actually supports the brief's claims.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


REQUIRED_HEADINGS = {
    "metadata",
    "scope",
    "implementation-relevant summary",
    "implementation guidance for codex",
    "open questions / unresolved items",
    "source traceability",
}

IMPLEMENTATION_SIGNAL_PATTERNS = [
    r"\bapi\b",
    r"\bendpoint\b",
    r"\bmethod\b",
    r"\bpath\b",
    r"\bauth\b",
    r"\brequest\b",
    r"\bresponse\b",
    r"\berror\b",
    r"\bschema\b",
    r"\bfield\b",
    r"\benum\b",
    r"\bstatus code\b",
    r"\bvalidation\b",
    r"\bconstraint\b",
    r"\bidempotenc",
    r"\bpagination\b",
    r"\brate limit\b",
    r"\bpermission\b",
    r"\bsecurity\b",
    r"\bworkflow\b",
    r"\bacceptance criteria\b",
]

UNRESOLVED_MARKERS = (
    "Open question",
    "Assumption",
    "Conflict",
    "Unconfirmed",
    "TBD",
    "TODO",
)


@dataclass
class Check:
    status: str
    name: str
    message: str


def emit(checks: list[Check], as_json: bool) -> None:
    if as_json:
        status = "fail" if any(c.status == "FAIL" for c in checks) else "pass"
        if status == "pass" and any(c.status == "WARN" for c in checks):
            status = "warn"
        print(json.dumps({"status": status, "checks": [asdict(c) for c in checks]}, ensure_ascii=False, indent=2))
        return

    for check in checks:
        print(f"{check.status} {check.name}: {check.message}")

    if any(c.status == "FAIL" for c in checks):
        print("SUMMARY: FAIL")
    elif any(c.status == "WARN" for c in checks):
        print("SUMMARY: WARN")
    else:
        print("SUMMARY: PASS")


def normalized_headings(text: str) -> list[str]:
    headings: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            heading = re.sub(r"\s+", " ", match.group(2).strip().lower())
            headings.append(heading)
    return headings


def check_code_fences(text: str) -> Check:
    fence_count = sum(1 for line in text.splitlines() if line.strip().startswith("```"))
    if fence_count % 2 == 0:
        return Check("PASS", "code_fences", "fenced code blocks are balanced")
    return Check("FAIL", "code_fences", "fenced code blocks are not balanced")


def check_title(headings: list[str]) -> Check:
    if not headings:
        return Check("FAIL", "title", "no Markdown headings found")
    if "codex context brief" in headings[0]:
        return Check("PASS", "title", "top heading identifies a Codex context brief")
    return Check("WARN", "title", "top heading does not explicitly include 'Codex Context Brief'")


def check_required_headings(headings: list[str]) -> list[Check]:
    found = set(headings)
    checks: list[Check] = []
    for heading in sorted(REQUIRED_HEADINGS):
        if heading in found:
            checks.append(Check("PASS", f"heading:{heading}", "required heading found"))
        else:
            checks.append(Check("WARN", f"heading:{heading}", "recommended heading missing; acceptable only if not applicable"))
    return checks


def check_source_traceability(text: str) -> Check:
    lower = text.lower()
    has_source = any(marker in lower for marker in ("source:", "source version:", "source coverage:", "repository path", "page", "section", "url"))
    if has_source:
        return Check("PASS", "source_traceability", "source metadata or traceability markers found")
    return Check("WARN", "source_traceability", "no clear source metadata or source traceability markers found")


def check_source_coverage(text: str) -> Check:
    if re.search(r"(?im)^\s*-?\s*source coverage\s*:", text):
        return Check("PASS", "source_coverage", "source coverage marker found")
    return Check("WARN", "source_coverage", "no Source coverage marker found; mark complete / partial / unverified")


def check_codex_intended_use(text: str) -> Check:
    lower = text.lower()
    has_intended_use = re.search(r"(?im)^\s*-?\s*intended use\s*:", text) is not None
    mentions_codex = "codex" in lower or "coding agent" in lower or "coding-agent" in lower
    if has_intended_use and mentions_codex:
        return Check("PASS", "codex_intended_use", "intended use and Codex / coding-agent marker found")
    if mentions_codex:
        return Check("WARN", "codex_intended_use", "Codex / coding-agent marker found, but Intended use metadata is missing")
    return Check("WARN", "codex_intended_use", "no clear Codex / coding-agent intended-use marker found")


def check_implementation_signals(text: str) -> Check:
    lower = text.lower()
    matches = sum(1 for pattern in IMPLEMENTATION_SIGNAL_PATTERNS if re.search(pattern, lower))
    if matches >= 3:
        return Check("PASS", "implementation_signals", f"found {matches} implementation-relevant signal categories")
    return Check("WARN", "implementation_signals", f"only found {matches} implementation-relevant signal categories")


def check_unresolved_items(text: str) -> Check:
    if any(marker.lower() in text.lower() for marker in UNRESOLVED_MARKERS):
        return Check("PASS", "unresolved_markers", "unresolved / assumption markers are explicit")
    return Check("WARN", "unresolved_markers", "no explicit unresolved, assumption, conflict, or unconfirmed markers found")


def check_summary_only_shape(text: str) -> Check:
    lower = text.lower()
    generic_markers = ("introduction", "conclusion", "background", "overview")
    codex_markers = ("implementation guidance for codex", "contracts and invariants", "api / interface reference", "data model / schema")
    generic_count = sum(1 for marker in generic_markers if marker in lower)
    codex_count = sum(1 for marker in codex_markers if marker in lower)
    if codex_count >= 1:
        return Check("PASS", "brief_shape", "Codex-oriented structure markers found")
    if generic_count >= 2:
        return Check("WARN", "brief_shape", "document looks like a generic summary; ensure it is a Codex context brief")
    return Check("WARN", "brief_shape", "few Codex-oriented structure markers found")


def check_secrets(text: str) -> Check:
    patterns = [
        r"sk-[A-Za-z0-9_-]{20,}",
        r"ghp_[A-Za-z0-9_]{20,}",
        r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----",
        r"(?i)\b(api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}",
    ]
    for pattern in patterns:
        if re.search(pattern, text):
            return Check("FAIL", "secrets", "possible secret or credential pattern found")
    return Check("PASS", "secrets", "no common secret patterns found")


def validate(path: Path, strict: bool = False) -> list[Check]:
    checks: list[Check] = []
    if not path.exists():
        return [Check("FAIL", "file", f"file not found: {path}")]
    if path.suffix.lower() not in {".md", ".markdown", ".txt"}:
        checks.append(Check("WARN", "extension", "expected Markdown-like file extension"))

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return [Check("FAIL", "content", "file is empty")]

    headings = normalized_headings(text)
    checks.append(check_title(headings))
    checks.extend(check_required_headings(headings))
    checks.append(check_code_fences(text))
    checks.append(check_codex_intended_use(text))
    checks.append(check_source_traceability(text))
    checks.append(check_source_coverage(text))
    checks.append(check_implementation_signals(text))
    checks.append(check_summary_only_shape(text))
    checks.append(check_unresolved_items(text))
    checks.append(check_secrets(text))

    if strict:
        checks = [
            Check("FAIL", c.name, c.message) if c.status == "WARN" else c
            for c in checks
        ]
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a reusable Codex context brief Markdown file.")
    parser.add_argument("path", help="Path to the Markdown context brief")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    checks = validate(Path(args.path), strict=args.strict)
    emit(checks, args.json)
    return 1 if any(c.status == "FAIL" for c in checks) else 0


if __name__ == "__main__":
    sys.exit(main())
