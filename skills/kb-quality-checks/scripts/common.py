from __future__ import annotations

import os
import re
import sys

import yaml

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
    ".codex",
}


def repo_root_from_args(argv: list[str]) -> Path:
    if len(argv) >= 2:
        return Path(argv[1]).resolve()
    return Path.cwd().resolve()


def iter_markdown_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
        for filename in sorted(files):
            if filename.endswith(".md"):
                yield Path(current) / filename


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace(os.sep, "/")


def read_text(path: Path) -> tuple[str | None, str | None]:
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError as exc:
        return None, f"UTF-8로 읽을 수 없음: {exc}"


def frontmatter_text(text: str) -> tuple[str | None, str | None]:
    """Return the YAML frontmatter text and a delimiter error, if any."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        if text.startswith("---"):
            return None, "YAML frontmatter 시작 구분자는 단독 '---' 라인이어야 함"
        return None, None

    lines = text.splitlines()
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx]) + "\n", None
    return None, "YAML frontmatter 종료 구분자 없음"


def load_frontmatter(text: str) -> tuple[dict[str, object] | None, str | None]:
    """Parse YAML frontmatter as a top-level mapping."""
    raw, error = frontmatter_text(text)
    if error or raw is None:
        return None, error

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, f"YAML 문법 오류: {exc}"

    if data is None:
        return {}, None
    if not isinstance(data, dict):
        return None, "YAML frontmatter 최상위 값은 mapping이어야 함"
    return data, None


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
