#!/usr/bin/env python3
"""Validate a post-implementation documentation update plan.

The validator checks plan structure and common risk markers. It is not a proof
that the plan is correct; it is a lightweight safety check before applying doc
or memo updates.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

RECOMMENDED_HEADINGS = [
    "Change evidence",
    "Impact summary",
    "Target updates",
    "No-update decisions",
    "Notion / Markdown sync",
    "Risks and unresolved items",
]
RISK_TERMS = [
    "breaking",
    "migration",
    "deprecated",
    "deprecation",
    "environment variable",
    "env",
    "config",
    "permission",
    "security",
    "auth",
    "token",
    "secret",
]
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]


@dataclass
class Check:
    level: str
    code: str
    message: str


def headings(markdown: str) -> list[str]:
    return [m.group(2).strip() for m in re.finditer(r"^(#{1,6})\s+(.+)$", markdown, re.MULTILINE)]


def check_plan(text: str) -> list[Check]:
    checks: list[Check] = []
    hs = headings(text)

    if not hs:
        checks.append(Check("FAIL", "headings", "No Markdown headings found."))
    else:
        checks.append(Check("PASS", "headings", f"Found {len(hs)} Markdown headings."))

    normalized = {h.lower() for h in hs}
    for required in ["Change evidence", "Impact summary", "Target updates"]:
        if required.lower() not in normalized:
            checks.append(Check("FAIL", "missing_required_heading", f"Missing required heading: {required}"))
        else:
            checks.append(Check("PASS", "required_heading", f"Found required heading: {required}"))

    for heading in RECOMMENDED_HEADINGS:
        if heading.lower() not in normalized:
            checks.append(Check("WARN", "missing_recommended_heading", f"Missing recommended heading: {heading}"))

    if "Open question" not in text and "Assumption" not in text and "Conflict" not in text:
        checks.append(Check("WARN", "uncertainty_markers", "No Open question / Assumption / Conflict markers found."))
    else:
        checks.append(Check("PASS", "uncertainty_markers", "Uncertainty markers are present."))

    if "notion" in text.lower() and "canonical" not in text.lower():
        checks.append(Check("WARN", "canonical_source", "Notion is mentioned but canonical source is not clearly marked."))

    if any(term in text.lower() for term in RISK_TERMS):
        if "Risk" not in text and "Risks" not in text:
            checks.append(Check("WARN", "risk_section", "Risk-like terms appear but no risk section is clearly labeled."))
        else:
            checks.append(Check("PASS", "risk_section", "Risk-like terms appear and a risk section is present."))

    if not re.search(r"\|.+\|.+\|", text):
        checks.append(Check("WARN", "tables", "No Markdown table found; concise impact and target tables are recommended."))

    secret_hits = []
    for pattern in SECRET_PATTERNS:
        secret_hits.extend(pattern.findall(text))
    if secret_hits:
        checks.append(Check("FAIL", "possible_secret", "Possible secret/token pattern found. Remove secrets before syncing docs."))
    else:
        checks.append(Check("PASS", "possible_secret", "No common secret token patterns found."))

    return checks


def summarize(checks: list[Check]) -> str:
    fail = sum(1 for c in checks if c.level == "FAIL")
    warn = sum(1 for c in checks if c.level == "WARN")
    status = "FAIL" if fail else "WARN" if warn else "PASS"
    lines = [f"SUMMARY {status}: {fail} fail, {warn} warn, {len(checks) - fail - warn} pass"]
    for check in checks:
        lines.append(f"{check.level} {check.code}: {check.message}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a post-implementation doc update plan.")
    parser.add_argument("plan", help="Markdown update plan path.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args()

    plan_path = Path(args.plan)
    if not plan_path.exists():
        payload = {"status": "error", "message": f"File not found: {plan_path}"}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: {payload['message']}")
        return 2

    text = plan_path.read_text(encoding="utf-8", errors="replace")
    checks = check_plan(text)
    fail = any(c.level == "FAIL" for c in checks)
    warn = any(c.level == "WARN" for c in checks)
    status = "fail" if fail else "warn" if warn else "pass"

    if args.json:
        print(json.dumps({"status": status, "checks": [asdict(c) for c in checks]}, ensure_ascii=False, indent=2))
    else:
        print(summarize(checks))

    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
