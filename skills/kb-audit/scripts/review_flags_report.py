#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from common import iter_markdown, rel, write_or_print

FLAGS = ["검토 필요", "추가 확인 필요", "추가 정의 필요", "placeholder", "TODO", "미정"]
DEFAULT_TARGET_PREFIXES = (
    "10_PLANNING/",
    "20_TECHNICAL/",
    "30_DECISIONS/Planning/",
    "30_DECISIONS/Technical/",
    "40_RAW/",
)


def is_default_target(path: str) -> bool:
    return path.startswith(DEFAULT_TARGET_PREFIXES)


def generate(root: Path, include_guides: bool = False) -> str:
    rows: list[tuple[str, int, str, str]] = []
    pattern = re.compile("|".join(re.escape(flag) for flag in FLAGS), re.IGNORECASE)
    for path in iter_markdown(root):
        relative_path = rel(path, root)
        if not include_guides and not is_default_target(relative_path):
            continue
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), start=1):
            match = pattern.search(line)
            if match:
                snippet = line.strip().replace("|", "\\|")[:180]
                rows.append((relative_path, line_no, match.group(0), snippet))

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
        "---",
        "",
        "# Review Flags Report",
        "",
        "| 파일 | 줄 | 플래그 | 내용 |",
        "|---|---:|---|---|",
    ]
    for file_path, line_no, flag, snippet in rows:
        lines.append(f"| {file_path} | {line_no} | {flag} | {snippet} |")
    if not rows:
        lines.append("|  |  |  | 검토 플래그 없음 |")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="검토 필요 플래그 리포트를 생성한다.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output", "-o")
    parser.add_argument(
        "--include-guides",
        action="store_true",
        help="README, AGENTS, 00_START_HERE 같은 운영 안내 문서까지 포함한다.",
    )
    args = parser.parse_args()
    write_or_print(generate(Path(args.root).resolve(), include_guides=args.include_guides), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
