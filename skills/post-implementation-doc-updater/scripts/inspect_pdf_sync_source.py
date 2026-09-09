#!/usr/bin/env python3
"""Read bounded text from one uploaded PDF as documentation-update evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from ocr_fallback import ocr_fallback


def inspect(pdf_path: Path, max_pages: int, use_ocr_fallback: bool, ocr_lang: str) -> dict:
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("PDF input must be an explicitly uploaded .pdf file.")
    if not pdf_path.is_file():
        raise ValueError(f"PDF input not found: {pdf_path}")
    data = pdf_path.read_bytes()
    reader_engine = "pypdf"
    try:
        from pypdf import PdfReader

        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        pages = [
            {"page": index, "text": page.extract_text() or ""}
            for index, page in enumerate(reader.pages[:max_pages], start=1)
        ]
    except Exception as pypdf_error:
        try:
            import pdfplumber
            with pdfplumber.open(str(pdf_path)) as pdf:
                total_pages = len(pdf.pages)
                pages = [
                    {"page": index, "text": page.extract_text() or ""}
                    for index, page in enumerate(pdf.pages[:max_pages], start=1)
                ]
        except Exception as pdfplumber_error:
            raise RuntimeError(
                "PDF inspection failed with both pypdf and pdfplumber. "
                f"pypdf: {pypdf_error}; pdfplumber: {pdfplumber_error}"
            ) from pdfplumber_error
        reader_engine = "pdfplumber"
    ocr_status = "not_requested"
    ocr_error = None
    if use_ocr_fallback:
        blank_pages = {item["page"] for item in pages if len(item["text"].strip()) < 20}
        if blank_pages:
            try:
                records, ocr_status = ocr_fallback(pdf_path, max_pages, ocr_lang)
                by_page = {int(str(record["location"]).rsplit(" ", 1)[-1]): record for record in records}
                for item in pages:
                    record = by_page.get(item["page"])
                    if item["page"] in blank_pages and record and record["text"]:
                        item["ocr_text"] = record["text"]
                        item["ocr_confidence"] = record["confidence"]
            except (RuntimeError, ValueError) as exc:
                ocr_status = "unavailable"
                ocr_error = str(exc)
        else:
            ocr_status = "not_needed"
    return {
        "status": "ok",
        "source": {
            "path": str(pdf_path.resolve()),
            "sha256": hashlib.sha256(data).hexdigest(),
            "page_count": total_pages,
            "pages_read": len(pages),
            "complete": len(pages) == total_pages,
            "text_extraction_only": True,
            "ocr_fallback": ocr_status,
            "ocr_error": ocr_error,
        "pages": pages,
        "reader_engine": reader_engine,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read bounded text from one uploaded PDF. It does not render, modify, or treat the PDF as a sync target."
    )
    parser.add_argument("pdf", help="Explicit uploaded PDF to inspect.")
    parser.add_argument("--max-pages", type=int, default=20, help="Maximum pages to extract (1-500). Default: 20.")
    parser.add_argument("--ocr-fallback", action="store_true", help="OCR pages with insufficient native text when Tesseract is available.")
    parser.add_argument("--ocr-lang", default="eng", help="Installed Tesseract language code. Default: eng.")
    parser.add_argument("--json", action="store_true", help="Emit JSON only.")
    args = parser.parse_args()
    if not 1 <= args.max_pages <= 500:
        parser.error("--max-pages must be between 1 and 500.")
    try:
        result = inspect(Path(args.pdf), args.max_pages, args.ocr_fallback, args.ocr_lang)
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
        print(f"- ocr_fallback: {source['ocr_fallback']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
