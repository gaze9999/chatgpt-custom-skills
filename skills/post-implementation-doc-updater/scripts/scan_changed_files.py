#!/usr/bin/env python3
"""Classify changed files by likely documentation impact.

This script is a lightweight helper for Post-Implementation Doc Updater. It does
not prove behavior changed; it provides a compact first-pass map so the model can
avoid reading large diffs unnecessarily.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

DOC_EXTS = {".md", ".mdx", ".rst", ".txt", ".adoc"}
TEST_HINTS = {"test", "tests", "spec", "__tests__", "fixtures", "mocks"}
CONFIG_NAMES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "pyproject.toml",
    "poetry.lock",
    "dockerfile",
    "docker-compose.yml",
    "compose.yml",
    ".env.example",
}
PUBLIC_HINTS = {
    "api",
    "routes",
    "controllers",
    "schema",
    "schemas",
    "openapi",
    "swagger",
    "sdk",
    "cli",
    "commands",
    "config",
    "migration",
    "migrations",
    "public",
}
UI_HINTS = {"components", "pages", "views", "ui", "screens", "routes"}
DOC_HINTS = {"readme", "docs", "documentation", "memo", "notes", "changelog", "context", "brief"}


@dataclass
class FileImpact:
    path: str
    change_type: str
    category: str
    likely_doc_impact: str
    reason: str


def run_git(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout


def parse_name_status(text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0]
        path = parts[-1]
        rows.append((status, path))
    return rows


def changed_from_repo(repo: Path, base: str | None) -> list[tuple[str, str]]:
    if base:
        text = run_git(repo, ["diff", "--name-status", base, "HEAD"])
    else:
        staged = run_git(repo, ["diff", "--cached", "--name-status"])
        unstaged = run_git(repo, ["diff", "--name-status"])
        if not staged and not unstaged:
            staged = run_git(repo, ["diff", "--name-status", "HEAD~1", "HEAD"])
        text = staged + unstaged
    return parse_name_status(text)


def changed_from_diff(diff_file: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in diff_file.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("diff --git "):
            match = re.search(r" b/(.+)$", line)
            if match:
                rows.append(("M", match.group(1)))
    seen: set[str] = set()
    unique: list[tuple[str, str]] = []
    for status, path in rows:
        if path not in seen:
            unique.append((status, path))
            seen.add(path)
    return unique


def classify(path_text: str, status: str) -> FileImpact:
    path = Path(path_text)
    lower = path_text.lower()
    parts = set(path.parts)
    ext = path.suffix.lower()
    name = path.name.lower()

    if ext in DOC_EXTS or any(h in lower for h in DOC_HINTS):
        return FileImpact(path_text, status, "documentation", "yes", "documentation or memo file changed")

    if name in CONFIG_NAMES or any(part in {"config", ".github", "scripts"} for part in parts):
        return FileImpact(path_text, status, "configuration", "yes", "configuration, setup, automation, or script change may require docs")

    if any(h in lower for h in PUBLIC_HINTS):
        return FileImpact(path_text, status, "public-contract", "yes", "API, schema, CLI, config, migration, or public contract path")

    if any(h in lower for h in UI_HINTS):
        return FileImpact(path_text, status, "ui-or-route", "maybe", "UI or route change may affect user-facing docs or memo")

    if any(h in lower for h in TEST_HINTS):
        return FileImpact(path_text, status, "test", "no", "test or fixture change usually does not require docs")

    if ext in {".json", ".yaml", ".yml", ".toml"}:
        return FileImpact(path_text, status, "structured-data", "maybe", "structured data or metadata may affect configuration or contracts")

    if ext in {".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".java", ".cs", ".rb", ".php"}:
        return FileImpact(path_text, status, "source", "maybe", "source change may or may not affect documented behavior")

    return FileImpact(path_text, status, "other", "no", "no obvious documentation impact from path alone")


def render_text(items: list[FileImpact]) -> str:
    counts = {"yes": 0, "maybe": 0, "no": 0}
    for item in items:
        counts[item.likely_doc_impact] += 1
    lines = [
        "Changed file documentation impact summary",
        f"- yes: {counts['yes']}",
        f"- maybe: {counts['maybe']}",
        f"- no: {counts['no']}",
        "",
    ]
    for item in items:
        lines.append(f"- {item.path}")
        lines.append(f"  - change_type: {item.change_type}")
        lines.append(f"  - category: {item.category}")
        lines.append(f"  - likely_doc_impact: {item.likely_doc_impact}")
        lines.append(f"  - reason: {item.reason}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify changed files by likely documentation impact.")
    parser.add_argument("--repo", default=".", help="Repository root. Default: current directory.")
    parser.add_argument("--base", help="Optional base ref for git diff, e.g. origin/main or HEAD~1.")
    parser.add_argument("--diff-file", help="Optional unified diff / patch file to scan instead of git.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args()

    try:
        if args.diff_file:
            rows = changed_from_diff(Path(args.diff_file))
        else:
            rows = changed_from_repo(Path(args.repo).resolve(), args.base)
        items = [classify(path, status) for status, path in rows]
    except Exception as exc:  # noqa: BLE001
        payload = {"status": "error", "message": str(exc)}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: {exc}")
        return 2

    if args.json:
        print(json.dumps({"status": "ok", "files": [asdict(item) for item in items]}, ensure_ascii=False, indent=2))
    else:
        print(render_text(items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
