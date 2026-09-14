#!/usr/bin/env python3
"""Read one explicit Markdown sync target without changing it."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)
NOTION_URL_RE = re.compile(r"https?://(?:www\.)?notion\.so/[^\s)>]+", re.IGNORECASE)


@dataclass
class MarkdownTarget:
    path: str
    sha256: str
    bytes: int
    frontmatter: dict[str, str]
    headings: list[dict[str, object]]
    notion_page_ids: list[str]
    notion_urls: list[str]
    sync_mode: str | None


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    values: dict[str, str] = {}
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def page_ids(frontmatter: dict[str, str], text: str) -> list[str]:
    values = [
        value
        for key, value in frontmatter.items()
        if key.lower() in {"notion_page_id", "notion-page-id", "notion_id", "notion-id"}
    ]
    values.extend(re.findall(r"(?im)^\s*(?:notion[ _-]?(?:page[ _-]?)?id)\s*[:=]\s*([0-9a-f-]{32,36})\s*$", text))
    return list(dict.fromkeys(values))


def inspect(path: Path) -> MarkdownTarget:
    if path.suffix.lower() not in {".md", ".markdown", ".mdx"}:
        raise ValueError("Target must be a Markdown file (.md, .markdown, or .mdx).")
    if not path.is_file():
        raise ValueError(f"Markdown target not found: {path}")
    data = path.read_bytes()
    text = data.decode("utf-8", errors="replace")
    frontmatter = parse_frontmatter(text)
    headings = [
        {"level": len(match.group(1)), "text": match.group(2).strip()}
        for match in HEADING_RE.finditer(text)
    ]
    urls = list(dict.fromkeys(NOTION_URL_RE.findall(text)))
    return MarkdownTarget(
        path=str(path.resolve()),
        sha256=hashlib.sha256(data).hexdigest(),
        bytes=len(data),
        frontmatter=frontmatter,
        headings=headings,
        notion_page_ids=page_ids(frontmatter, text),
        notion_urls=urls,
        sync_mode=frontmatter.get("sync_mode") or frontmatter.get("sync-mode"),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect one explicit Markdown sync target without writing it.")
    parser.add_argument("file", help="Explicit Markdown file to inspect.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args()
    try:
        result = inspect(Path(args.file))
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False) if args.json else f"ERROR: {exc}")
        return 2
    payload = asdict(result)
    if args.json:
        print(json.dumps({"status": "ok", "target": payload}, ensure_ascii=False, indent=2))
    else:
        print(f"Markdown sync target: {payload['path']}")
        print(f"- sha256: {payload['sha256']}")
        print(f"- headings: {len(payload['headings'])}")
        print(f"- notion_page_ids: {', '.join(payload['notion_page_ids']) or 'none'}")
        print(f"- sync_mode: {payload['sync_mode'] or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
