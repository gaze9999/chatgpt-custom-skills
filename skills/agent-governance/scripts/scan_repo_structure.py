#!/usr/bin/env python3
"""Scan a repository and print a concise structure report for agent governance work.

This script intentionally reads directory entries and selected small metadata only.
It does not parse source files or dump file contents, so the model can inspect a
compact repo map before deciding which files are worth reading.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_MAX_DEPTH = 4
DEFAULT_MAX_FILES_PER_DIR = 40
DEFAULT_MAX_SIZE_BYTES = 512 * 1024

ALWAYS_SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".github",
    ".codex",
    ".cache",
    ".tmp",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "tmp",
    "temp",
    "__pycache__",
}

DEFAULT_SKIP_GLOBS = {
    "*.zip",
    "*.tar",
    "*.tar.gz",
    "*.tgz",
    "*.log",
    "*.tmp",
    "*.temp",
    ".DS_Store",
    "Thumbs.db",
}

IMPORTANT_ROOT_FILES = {
    "AGENTS.md",
    "README.md",
    ".gitignore",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
}

IMPORTANT_SKILL_FILES = {
    "SKILL.md",
    "agents/openai.yaml",
}


@dataclass(frozen=True)
class Entry:
    path: Path
    is_dir: bool
    size: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a compact repository structure report for agent governance."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Repository root to scan. Defaults to current directory.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=DEFAULT_MAX_DEPTH,
        help=f"Maximum directory depth to print. Default: {DEFAULT_MAX_DEPTH}.",
    )
    parser.add_argument(
        "--max-files-per-dir",
        type=int,
        default=DEFAULT_MAX_FILES_PER_DIR,
        help=f"Maximum entries to print per directory. Default: {DEFAULT_MAX_FILES_PER_DIR}.",
    )
    parser.add_argument(
        "--max-size-bytes",
        type=int,
        default=DEFAULT_MAX_SIZE_BYTES,
        help="Files larger than this are reported as large artifacts."
        f" Default: {DEFAULT_MAX_SIZE_BYTES}.",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files and directories except hard-skipped generated folders.",
    )
    return parser.parse_args()


def should_skip(path: Path, root: Path, include_hidden: bool) -> bool:
    name = path.name
    rel = path.relative_to(root)

    if path.is_dir() and name in ALWAYS_SKIP_DIRS:
        return True

    if not include_hidden and name.startswith("."):
        normalized = str(rel).replace(os.sep, "/")
        if normalized not in IMPORTANT_ROOT_FILES:
            return True

    for pattern in DEFAULT_SKIP_GLOBS:
        if fnmatch.fnmatch(name, pattern):
            return True

    return False


def safe_iterdir(path: Path) -> list[Path]:
    try:
        return sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
    except OSError:
        return []


def collect_entries(root: Path, max_depth: int, include_hidden: bool) -> list[Entry]:
    entries: list[Entry] = []

    def walk(current: Path, depth: int) -> None:
        if depth > max_depth:
            return
        for child in safe_iterdir(current):
            if should_skip(child, root, include_hidden):
                continue
            try:
                is_dir = child.is_dir()
                size = 0 if is_dir else child.stat().st_size
            except OSError:
                continue
            entries.append(Entry(child.relative_to(root), is_dir, size))
            if is_dir:
                walk(child, depth + 1)

    walk(root, 1)
    return entries


def list_root_files(root: Path) -> list[str]:
    files: list[str] = []
    for child in safe_iterdir(root):
        if child.is_file():
            files.append(child.name)
    return sorted(files, key=str.lower)


def list_skills(root: Path) -> list[Path]:
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return []
    return [path for path in safe_iterdir(skills_dir) if path.is_dir()]


def rel_exists(base: Path, relative: str) -> bool:
    return (base / relative).exists()


def count_files(path: Path) -> int:
    total = 0
    for current, dirs, files in os.walk(path):
        dirs[:] = [directory for directory in dirs if directory not in ALWAYS_SKIP_DIRS]
        total += len(files)
    return total


def find_large_files(root: Path, entries: Iterable[Entry], max_size_bytes: int) -> list[Entry]:
    return [entry for entry in entries if not entry.is_dir and entry.size > max_size_bytes]


def print_tree(entries: list[Entry], max_files_per_dir: int) -> None:
    by_parent: dict[Path, list[Entry]] = {}
    for entry in entries:
        by_parent.setdefault(entry.path.parent, []).append(entry)

    def emit(parent: Path, prefix: str = "") -> None:
        children = by_parent.get(parent, [])
        shown = children[:max_files_per_dir]
        for index, entry in enumerate(shown):
            connector = "└── " if index == len(shown) - 1 and len(children) <= max_files_per_dir else "├── "
            suffix = "/" if entry.is_dir else ""
            size = "" if entry.is_dir else f" ({entry.size} B)"
            print(f"{prefix}{connector}{entry.path.name}{suffix}{size}")
            if entry.is_dir:
                child_prefix = prefix + ("    " if connector == "└── " else "│   ")
                emit(entry.path, child_prefix)
        hidden_count = len(children) - len(shown)
        if hidden_count > 0:
            print(f"{prefix}└── ... {hidden_count} more entries omitted")

    emit(Path("."))


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    if not root.exists() or not root.is_dir():
        print(f"FAIL root_not_found: {root}")
        return 1

    entries = collect_entries(root, args.max_depth, args.include_hidden)
    skills = list_skills(root)
    root_files = list_root_files(root)
    large_files = find_large_files(root, entries, args.max_size_bytes)

    print("REPOSITORY STRUCTURE SCAN")
    print(f"root: {root}")
    print(f"root_files: {', '.join(root_files) if root_files else 'none'}")
    print(f"skills_count: {len(skills)}")
    print("")

    print("IMPORTANT ROOT FILES")
    for name in sorted(IMPORTANT_ROOT_FILES):
        status = "found" if (root / name).exists() else "missing"
        print(f"- {name}: {status}")
    print("")

    print("SKILLS")
    if not skills:
        print("- none")
    for skill in skills:
        print(f"- {skill.name}")
        for relative in sorted(IMPORTANT_SKILL_FILES):
            print(f"  - {relative}: {'found' if rel_exists(skill, relative) else 'missing'}")
        for directory in ("agents", "assets", "references", "scripts"):
            directory_path = skill / directory
            if directory_path.is_dir():
                print(f"  - {directory}/: found ({count_files(directory_path)} files)")
            else:
                print(f"  - {directory}/: missing")
    print("")

    print("LARGE FILES")
    if not large_files:
        print("- none")
    for entry in large_files[:20]:
        print(f"- {entry.path} ({entry.size} B)")
    if len(large_files) > 20:
        print(f"- ... {len(large_files) - 20} more omitted")
    print("")

    print("TREE")
    print_tree(entries, args.max_files_per_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
