#!/usr/bin/env python3
"""Markdown structure validator for Document Production Pipeline."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
VERSION_RE = re.compile(r"文件版本\s*[:：]\s*v\d+\b", re.IGNORECASE)


def result(status: str, check: str, detail: str) -> None:
    print(f"{status}: {check} - {detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Markdown document structure.")
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    path = args.file

    failures = 0
    warnings = 0

    if not path.is_file():
        result("FAIL", "file", "file does not exist")
        return 2

    if path.suffix.lower() not in {".md", ".markdown"}:
        result("FAIL", "extension", "expected .md or .markdown")
        return 2

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    headings: list[tuple[int, int, str]] = []
    in_fence = False
    fence_token = None

    for lineno, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            token = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = None
            continue

        if in_fence:
            continue

        match = HEADING_RE.match(line)
        if match:
            headings.append((lineno, len(match.group(1)), match.group(2)))

    if headings:
        result("PASS", "headings", f"found {len(headings)} headings")
    else:
        warnings += 1
        result("WARN", "headings", "no ATX headings detected")

    jumps: list[str] = []
    previous_level = None
    for lineno, level, title in headings:
        if previous_level is not None and level > previous_level + 1:
            jumps.append(f"line {lineno}: H{previous_level} -> H{level} ({title})")
        previous_level = level

    if jumps:
        failures += 1
        result("FAIL", "heading-hierarchy", "; ".join(jumps[:5]))
    else:
        result("PASS", "heading-hierarchy", "no skipped heading levels detected")

    if in_fence:
        failures += 1
        result("FAIL", "code-fences", "unclosed fenced code block")
    else:
        result("PASS", "code-fences", "fenced code blocks are balanced")

    trailing = [str(i) for i, line in enumerate(lines, start=1) if line.endswith((" ", "\t"))]
    if trailing:
        warnings += 1
        result("WARN", "trailing-whitespace", f"lines: {', '.join(trailing[:10])}")
    else:
        result("PASS", "trailing-whitespace", "none detected")

    if VERSION_RE.search(text):
        result("PASS", "document-version", "vX document version detected")
    else:
        warnings += 1
        result("WARN", "document-version", "no '文件版本：vX' pattern detected")

    print(f"SUMMARY: failures={failures} warnings={warnings}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
