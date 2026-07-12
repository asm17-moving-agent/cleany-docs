#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True

EXCLUDED_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".obsidian", "50_WORKING"}


def iter_markdown(root: Path):
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        yield path


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    if not text.startswith("---\n"):
        return {}, []
    lines = text.splitlines()
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return {}, []
    data: dict[str, str] = {}
    raw = lines[1:end]
    for line in raw:
        if not line.strip() or line.startswith(" ") or line.startswith("-"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data, raw


def frontmatter_list(raw: list[str], key: str) -> list[str]:
    values: list[str] = []
    in_key = False
    for line in raw:
        if line.startswith(" ") or line.startswith("-"):
            if in_key:
                stripped = line.strip()
                if stripped.startswith("-"):
                    value = stripped[1:].strip().strip('"').strip("'")
                    if value:
                        values.append(value)
            continue
        if ":" in line:
            current, after = line.split(":", 1)
            in_key = current.strip() == key
            if in_key and after.strip():
                values.append(after.strip().strip('"').strip("'"))
    return values


def cell(value: str) -> str:
    return value.replace("|", "\\|")


def generate(root: Path) -> str:
    lines = [
        "---",
        "type: metadata-report",
        "status: draft",
        "reviewers:",
        "  -",
        "ingest_status: raw",
        "updated:",
        "tags:",
        "  - metadata",
        "  - report",
        "---",
        "",
        "# Metadata Report",
        "",
        "| 파일 | type | status | reviewers | updated | tags |",
        "|---|---|---|---|---|---|",
    ]
    for path in iter_markdown(root):
        rel = str(path.relative_to(root)).replace("\\", "/")
        data, raw = parse_frontmatter(path.read_text(encoding="utf-8"))
        lines.append(
            "| "
            + " | ".join(
                [
                    cell(rel),
                    cell(data.get("type", "")),
                    cell(data.get("status", "")),
                    cell(", ".join(frontmatter_list(raw, "reviewers"))),
                    cell(data.get("updated", "")),
                    cell(", ".join(frontmatter_list(raw, "tags"))),
                ]
            )
            + " |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Markdown frontmatter metadata report를 생성한다.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output", "-o", help="출력 Markdown 파일. 생략하면 stdout")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    markdown = generate(root)
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
        print(f"generated: {output}")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
