#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True

EXCLUDED_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".obsidian", "50_WORKING"}
EXCLUDED_PREFIXES = {"skills/kb-quality-checks/scripts", "skills/office-to-markdown/scripts", "skills/kb-maintenance/scripts"}


def should_include(path: Path, root: Path, include_tools: bool) -> bool:
    rel = path.relative_to(root)
    rel_str = str(rel).replace("\\", "/")
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if not include_tools and (rel_str.startswith("skills/") or rel_str.startswith(".agents/") or rel_str.startswith(".codex/")):
        return False
    if not include_tools and rel_str == "AGENTS.md":
        return False
    if not include_tools and any(rel_str.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    return True


def generate(root: Path, include_tools: bool) -> str:
    groups: dict[str, list[str]] = defaultdict(list)
    for path in sorted(root.rglob("*.md")):
        if not should_include(path, root, include_tools):
            continue
        rel = path.relative_to(root)
        folder = str(rel.parent).replace("\\", "/") if str(rel.parent) != "." else "."
        groups[folder].append(rel.name)

    lines = [
        "---",
        "type: file-index",
        "status: draft",
        "review_status: needs-human-review",
        "updated:",
        "tags:",
        "  - start-here",
        "  - file-index",
        "  - generated",
        "---",
        "",
        "# File Index",
        "",
        "이 문서는 deterministic script로 생성한 Markdown 파일 색인이다.",
        "",
    ]
    for folder in sorted(groups):
        title = "루트" if folder == "." else folder
        lines.extend([f"## {title}", ""])
        for name in groups[folder]:
            target = name if folder == "." else f"{folder}/{name}"
            lines.append(f"- [{name}]({target.replace(' ', '%20')})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Markdown 파일 색인을 생성한다.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output", "-o", help="출력 Markdown 파일. 생략하면 stdout")
    parser.add_argument("--include-tools", action="store_true", help="skills, .agents, .codex 문서도 포함")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    markdown = generate(root, args.include_tools)
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
