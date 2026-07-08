#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from common import frontmatter_list, iter_markdown, parse_frontmatter, rel, write_or_print

TARGET_PREFIXES = ("10_PLANNING/", "20_TECHNICAL/", "30_DECISIONS/")


def generate(root: Path) -> str:
    lines = [
        "---",
        "type: audit-report",
        "status: draft",
        "review_status: needs-human-review",
        "ingest_status: raw",
        "tags:",
        "  - audit",
        "  - report",
        "---",
        "",
        "# Source Refs Report",
        "",
        "| 파일 | type | status | source_refs | 상태 |",
        "|---|---|---|---|---|",
    ]
    for path in iter_markdown(root):
        r = rel(path, root)
        if not r.startswith(TARGET_PREFIXES):
            continue
        data, raw = parse_frontmatter(path.read_text(encoding="utf-8"))
        refs = frontmatter_list(raw, "source_refs")
        status = "OK" if refs else "source_refs 없음"
        refs_text = "<br>".join(refs).replace("|", "\\|")
        lines.append(f"| {r} | {data.get('type', '')} | {data.get('status', '')} | {refs_text} | {status} |")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="source_refs 리포트를 생성한다.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    write_or_print(generate(Path(args.root).resolve()), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
