from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

EXCLUDED_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".obsidian", ".agents", ".codex", "skills", "50_WORKING"}
EXCLUDED_PATH_PREFIXES = ("40_RAW/60_External_Artifacts/audit/",)


def iter_markdown(root: Path):
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        rel_text = str(rel).replace(os.sep, "/")
        if rel_text.startswith(EXCLUDED_PATH_PREFIXES):
            continue
        yield path


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace(os.sep, "/")


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
    raw = lines[1:end]
    data: dict[str, str] = {}
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
        if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:\s*", line):
            in_key = line.split(":", 1)[0].strip() == key
            after = line.split(":", 1)[1].strip()
            if in_key and after:
                values.append(after.strip('"').strip("'"))
            continue
        if in_key:
            stripped = line.strip()
            if stripped.startswith("-"):
                value = stripped[1:].strip().strip('"').strip("'")
                if value:
                    values.append(value)
    return values


def write_or_print(markdown: str, output: str | None) -> None:
    if output:
        out = Path(output).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
        print(f"generated: {out}")
    else:
        print(markdown, end="")
