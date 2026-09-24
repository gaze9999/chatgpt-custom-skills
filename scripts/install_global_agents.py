#!/usr/bin/env python3
"""Check or install the repository's global Codex AGENTS.md."""

from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, help="Override CODEX_HOME or ~/.codex.")
    parser.add_argument("--install", action="store_true", help="Install if missing or identical.")
    parser.add_argument("--replace", action="store_true", help="Back up and replace a different installed file; requires --install.")
    args = parser.parse_args()
    if args.replace and not args.install:
        parser.error("--replace requires --install")

    source = Path(__file__).resolve().parents[1] / "agents" / "AGENTS.md"
    if not source.is_file():
        parser.error(f"source missing: {source}")
    home = (args.codex_home or Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")).expanduser().resolve()
    if home == Path(home.anchor) or home == source.parent.parent or source.parent.parent in home.parents:
        parser.error("Codex home must not be a filesystem root or inside this repository")
    target = home / "AGENTS.md"
    if target.is_symlink():
        parser.error(f"target is a symlink; review it manually: {target}")
    if target.exists() and not target.is_file():
        parser.error(f"target is not a file: {target}")

    if target.is_file() and target.read_bytes() == source.read_bytes():
        print(f"CURRENT {target}")
        return 0
    if not args.install:
        print(f"{'DIFFERENT' if target.exists() else 'MISSING'} {target}")
        return 1
    if target.exists() and not args.replace:
        print(f"DIFFERENT {target}; review or use --install --replace")
        return 1
    home.mkdir(parents=True, exist_ok=True)
    if target.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = home / "backups" / "codex-setup" / stamp / "AGENTS.md"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)
        print(f"BACKUP {backup}")

    with tempfile.NamedTemporaryFile(dir=home, prefix="AGENTS.md.", suffix=".tmp", delete=False) as file:
        temporary = Path(file.name)
        file.write(source.read_bytes())
    try:
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"INSTALLED {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
