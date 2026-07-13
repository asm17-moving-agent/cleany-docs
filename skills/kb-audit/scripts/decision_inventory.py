#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from common import iter_markdown, parse_frontmatter, rel, write_or_print


def first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def generate(root: Path) -> str:
    lines = [
        "---",
        "type: audit-report",
        "status: draft",
        "reviewers:",
        "  -",
        "ingest_status: raw",
        "tags:",
        "  - audit",
        "  - report",
        "  - decision",
        "---",
        "",
        "# Decision Inventory",
        "",
        "| 파일 | 제목 | decision_type | status | date |",
        "|---|---|---|---|---|",
    ]
    count = 0
    for path in iter_markdown(root):
        r = rel(path, root)
        if not (r.startswith("30_DECISIONS/Planning/") or r.startswith("30_DECISIONS/Technical/")):
            continue
        text = path.read_text(encoding="utf-8")
        data, raw = parse_frontmatter(text)
        title = first_heading(text).replace("|", "\\|")
        lines.append(
            f"| {r} | {title} | {data.get('decision_type', '')} | {data.get('status', '')} | {data.get('date', '')} |"
        )
        count += 1
    if count == 0:
        lines.append("|  |  |  |  | Decision 문서 없음 |")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Decision inventory를 생성한다.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    write_or_print(generate(Path(args.root).resolve()), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
