#!/usr/bin/env python3
from __future__ import annotations

import re
import sys

sys.dont_write_bytecode = True
from pathlib import Path
from urllib.parse import unquote

from common import (
    iter_markdown_files,
    print_errors,
    read_text,
    rel,
    repo_root_from_args,
    strip_fenced_code,
)

MD_LINK_RE = re.compile(r"!?\[[^\]]*\]\((<[^>]+>|.*?)\)")
WIKI_LINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
STANDARD_LINK_PREFIXES = (
    "00_START_HERE/",
    "10_PLANNING/",
    "20_TECHNICAL/",
    "30_DECISIONS/",
)


def is_external(target: str) -> bool:
    lower = target.lower()
    return lower.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//"))


def normalize_markdown_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        target = target[1:target.index(">")]
    elif " \"" in target:
        target = target.split(" \"", 1)[0]
    elif " '" in target:
        target = target.split(" '", 1)[0]
    return unquote(target)


def safe_exists(root: Path, candidates: list[Path]) -> bool:
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
            resolved.relative_to(root)
        except (OSError, ValueError):
            continue
        if resolved.exists():
            return True
    return False


def markdown_target_exists(root: Path, current_file: Path, target: str) -> bool:
    if not target or target.startswith("#") or is_external(target):
        return True
    path_part = target.split("#", 1)[0].split("?", 1)[0]
    if not path_part:
        return True
    return safe_exists(root, [current_file.parent / path_part])


def wiki_target_exists(root: Path, current_file: Path, raw: str) -> bool:
    target = unquote(raw.split("|", 1)[0].split("#", 1)[0].strip())
    if not target or is_external(target):
        return True

    base = Path(target)
    candidates: list[Path] = []
    if base.suffix:
        candidates.extend([root / base, current_file.parent / base])
    else:
        candidates.extend([root / f"{target}.md", current_file.parent / f"{target}.md"])
        candidates.extend(
            path for path in iter_markdown_files(root) if path.name == f"{base.name}.md"
        )
    return safe_exists(root, candidates)


def main() -> int:
    root = repo_root_from_args(sys.argv)
    errors: list[str] = []

    for path in iter_markdown_files(root):
        text, err = read_text(path)
        r = rel(path, root)
        if err:
            errors.append(f"{r}: {err}")
            continue
        assert text is not None

        for line_no, line in strip_fenced_code(text.splitlines()):
            for match in MD_LINK_RE.finditer(line):
                target = normalize_markdown_target(match.group(1))
                if not markdown_target_exists(root, path, target):
                    errors.append(f"{r}:{line_no}: Markdown 링크/이미지 대상 없음: {target}")
            for match in WIKI_LINK_RE.finditer(line):
                target = match.group(1)
                if r.startswith(STANDARD_LINK_PREFIXES):
                    errors.append(
                        f"{r}:{line_no}: 공식 문서는 Obsidian wiki link 대신 "
                        f"표준 Markdown 링크 사용: [[{target}]]"
                    )
                    continue
                if not wiki_target_exists(root, path, target):
                    errors.append(f"{r}:{line_no}: Wiki 링크/임베드 대상 없음: [[{target}]]")

    return print_errors("references", errors)


if __name__ == "__main__":
    raise SystemExit(main())
