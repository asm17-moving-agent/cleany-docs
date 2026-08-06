#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from common import iter_markdown, rel, write_or_print

TARGET_PREFIXES = ("10_PLANNING/", "20_TECHNICAL/", "30_DECISIONS/")
EXCLUDED_PATHS = {"30_DECISIONS/00 - Decision Index.md"}
SECTION_RE = re.compile(r"^##(?:\s+\d+\.)?\s+출처\s*$")
NEXT_SECTION_RE = re.compile(r"^##\s+")


def source_items(text: str) -> list[str]:
    lines = text.splitlines()
    start = next((index for index, line in enumerate(lines) if SECTION_RE.match(line)), None)
    if start is None:
        return []

    items: list[str] = []
    for line in lines[start + 1:]:
        if NEXT_SECTION_RE.match(line):
            break
        stripped = line.strip()
        if stripped.startswith("- ") and stripped[2:].strip():
            items.append(stripped[2:].strip())
    return items


def generate(root: Path) -> str:
    lines = [
        "# References Report",
        "",
        "| 파일 | 출처 수 | 결과 |",
        "|---|---|---|",
    ]
    for path in iter_markdown(root):
        relative = rel(path, root)
        if relative in EXCLUDED_PATHS or not relative.startswith(TARGET_PREFIXES):
            continue
        items = source_items(path.read_text(encoding="utf-8"))
        result = "OK" if items else "출처 없음"
        lines.append(f"| {relative} | {len(items)} | {result} |")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="본문 출처 리포트를 생성한다.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    write_or_print(generate(Path(args.root).resolve()), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
