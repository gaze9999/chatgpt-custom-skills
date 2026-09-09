#!/usr/bin/env python3
"""Read bounded text from one uploaded PDF as documentation-update evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def inspect(pdf_path: Path, max_pages: int) -> dict:
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("PDF input must be an explicitly uploaded .pdf file.")
    if not pdf_path.is_file():
        raise ValueError(f"PDF input not found: {pdf_path}")
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("pypdf is required to inspect uploaded PDFs.") from exc

    data = pdf_path.read_bytes()
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    pages = []
    for index, page in enumerate(reader.pages[:max_pages], start=1):
        pages.append({"page": index, "text": page.extract_text() or ""})
    return {
        "status": "ok",
        "source": {
            "path": str(pdf_path.resolve()),
            "sha256": hashlib.sha256(data).hexdigest(),
            "page_count": total_pages,
            "pages_read": len(pages),
            "complete": len(pages) == total_pages,
            "text_extraction_only": True,
            "pages": pages,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read bounded text from one uploaded PDF. It does not render, modify, or treat the PDF as a sync target."
    )
    parser.add_argument("pdf", help="Explicit uploaded PDF to inspect.")
    parser.add_argument("--max-pages", type=int, default=20, help="Maximum pages to extract (1-500). Default: 20.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args()
    if not 1 <= args.max_pages <= 500:
        parser.error("--max-pages must be between 1 and 500.")
    try:
        result = inspect(Path(args.pdf), args.max_pages)
    except (OSError, RuntimeError, ValueError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}) if args.json else f"ERROR: {exc}")
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        source = result["source"]
        print(f"PDF evidence source: {source['path']}")
        print(f"- sha256: {source['sha256']}")
        print(f"- pages_read: {source['pages_read']} of {source['page_count']}")
        print(f"- complete: {source['complete']}")
        print("- text_extraction_only: true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
