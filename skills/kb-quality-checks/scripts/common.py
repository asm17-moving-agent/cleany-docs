from __future__ import annotations

import os
import re
import sys

sys.dont_write_bytecode = True
from pathlib import Path
from typing import Iterable

EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".obsidian",
    "50_WORKING",
}


def repo_root_from_args(argv: list[str]) -> Path:
    if len(argv) >= 2:
        return Path(argv[1]).resolve()
    return Path.cwd().resolve()


def iter_markdown_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.md"):
        rel_parts = path.relative_to(root).parts
        if any(part in EXCLUDED_DIRS for part in rel_parts):
            continue
        yield path


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace(os.sep, "/")


def read_text(path: Path) -> tuple[str | None, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError as exc:
        return None, f"UTF-8로 읽을 수 없음: {exc}"


def frontmatter_block(text: str) -> tuple[dict[str, str], list[str], str | None]:
    """Return (top-level key/value map, raw lines, error). Simple YAML frontmatter parser."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return {}, [], "YAML frontmatter가 파일 시작에 없음"

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [], "YAML frontmatter 시작 구분자 오류"

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return {}, [], "YAML frontmatter 종료 구분자 없음"

    raw = lines[1:end_idx]
    data: dict[str, str] = {}
    for line in raw:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith(" ") or line.startswith("-"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data, raw, None


def strip_fenced_code(lines: list[str]) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    in_fence = False
    fence_marker = ""
    fence_re = re.compile(r"^\s*(```+|~~~+)")
    for idx, line in enumerate(lines, start=1):
        m = fence_re.match(line)
        if m:
            marker = m.group(1)[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            continue
        if not in_fence:
            result.append((idx, line))
    return result


def print_errors(title: str, errors: list[str]) -> int:
    if errors:
        print(f"FAIL {title}: {len(errors)}개 오류")
        for item in errors:
            print(f"- {item}")
        return 1
    print(f"OK {title}")
    return 0
