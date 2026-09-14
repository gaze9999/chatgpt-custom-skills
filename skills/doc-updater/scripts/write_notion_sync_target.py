#!/usr/bin/env python3
"""Append prepared blocks to one explicit Notion page after a version check."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def request_json(path: str, token: str, method: str = "GET", body: dict | None = None) -> dict:
    encoded = json.dumps(body).encode("utf-8") if body is not None else None
    request = Request(
        f"{API_BASE}{path}",
        data=encoded,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method=method,
    )
    with urlopen(request, timeout=30) as response:  # noqa: S310 - fixed HTTPS API base
        return json.loads(response.read().decode("utf-8"))


def load_blocks(path: Path) -> list[dict]:
    if path.suffix.lower() != ".json":
        raise ValueError("Block input must be a JSON file.")
    payload = json.loads(path.read_text(encoding="utf-8"))
    blocks = payload.get("children") if isinstance(payload, dict) else payload
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("Block input must be a non-empty JSON array or an object with a non-empty children array.")
    if not all(isinstance(block, dict) and block.get("object") == "block" and block.get("type") for block in blocks):
        raise ValueError("Each prepared child must be a Notion block object with object=block and a type.")
    return blocks


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append prepared blocks to one explicit Notion page. It never searches, deletes, moves, or replaces content."
    )
    parser.add_argument("--page-id", required=True, help="Exact Notion page ID.")
    parser.add_argument("--blocks-file", required=True, help="Uploaded JSON file containing a children array or block array.")
    parser.add_argument(
        "--expected-last-edited-time",
        required=True,
        help="last_edited_time returned by an immediate prior exact-target read.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate prepared blocks without contacting Notion.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args()
    try:
        blocks = load_blocks(Path(args.blocks_file))
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}) if args.json else f"ERROR: {exc}")
        return 2

    if args.dry_run:
        result = {"status": "dry-run", "page_id": args.page_id, "append_block_count": len(blocks)}
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else f"DRY-RUN: {result}")
        return 0

    token = os.environ.get("NOTION_TOKEN")
    if not token:
        message = "NOTION_TOKEN is required in the environment; the script never accepts or stores a token argument."
        print(json.dumps({"status": "error", "message": message}) if args.json else f"ERROR: {message}")
        return 2
    try:
        before = request_json(f"/pages/{args.page_id}", token)
        if before.get("last_edited_time") != args.expected_last_edited_time:
            message = "Target changed after it was read; re-read and merge before writing."
            print(json.dumps({"status": "conflict", "message": message}) if args.json else f"CONFLICT: {message}")
            return 3
        response = request_json(
            f"/blocks/{args.page_id}/children",
            token,
            method="PATCH",
            body={"children": blocks},
        )
        after = request_json(f"/pages/{args.page_id}", token)
    except HTTPError as exc:
        message = f"Notion API returned HTTP {exc.code}. Re-read the exact target before retrying."
        print(json.dumps({"status": "error", "message": message}) if args.json else f"ERROR: {message}")
        return 4
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        message = f"Notion write failed or could not be verified: {exc}. Re-read the exact target before retrying."
        print(json.dumps({"status": "error", "message": message}) if args.json else f"ERROR: {message}")
        return 4

    result = {
        "status": "ok",
        "page_id": args.page_id,
        "append_block_count": len(response.get("results", [])),
        "before_last_edited_time": before.get("last_edited_time"),
        "after_last_edited_time": after.get("last_edited_time"),
        "post_write_read": True,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else f"WROTE: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
