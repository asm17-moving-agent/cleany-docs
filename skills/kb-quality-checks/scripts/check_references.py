#!/usr/bin/env python3
from __future__ import annotations

import re
import sys

sys.dont_write_bytecode = True
from pathlib import Path
from urllib.parse import unquote

from common import (
    iter_markdown_files,
    load_frontmatter,
    print_errors,
    read_text,
    rel,
    repo_root_from_args,
    strip_fenced_code,
)

MD_LINK_RE = re.compile(r"!?\[[^\]]*\]\((<[^>]+>|.*?)\)")
WIKI_LINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
METADATA_REF_FIELDS = ("source_refs", "related_decisions", "source_file", "supersedes")
REPO_PATH_PREFIXES = (
    "00_START_HERE/",
    "10_PLANNING/",
    "20_TECHNICAL/",
    "30_DECISIONS/",
    "40_RAW/",
    "90_TEMPLATES/",
    "skills/",
    ".agents/",
    ".github/",
)
ROOT_FILES = {"README.md", "AGENTS.md", "pyproject.toml", "uv.lock"}


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


def metadata_values(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def is_symbolic_reference(target: str) -> bool:
    stripped = target.strip()
    return stripped.startswith("[") and stripped.endswith("]")


def looks_like_repo_path(target: str) -> bool:
    return target in ROOT_FILES or target.startswith(REPO_PATH_PREFIXES)


def looks_like_relative_path(target: str) -> bool:
    return target.startswith(("./", "../")) or "/" in target or bool(Path(target).suffix)


def metadata_target_exists(
    root: Path,
    current_file: Path,
    field: str,
    raw_target: str,
) -> bool:
    target = unquote(raw_target.strip()).split("#", 1)[0]
    if not target or is_external(target) or is_symbolic_reference(target):
        return True

    if field == "source_file":
        candidates = [
            root / target,
            current_file.parent / target,
            current_file.parent / "assets" / target,
        ]
    elif field == "source_refs" and not looks_like_repo_path(target):
        if not looks_like_relative_path(target):
            return True
        candidates = [current_file.parent / target]
    else:
        candidates = [root / target]
    return safe_exists(root, candidates)


def check_frontmatter_references(
    root: Path,
    path: Path,
    text: str,
    errors: list[str],
) -> None:
    data, fm_err = load_frontmatter(text)
    if fm_err or data is None:
        return

    r = rel(path, root)
    for field in METADATA_REF_FIELDS:
        for target in metadata_values(data.get(field)):
            if not metadata_target_exists(root, path, field, target):
                errors.append(f"{r}: {field} 대상 없음: {target}")


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

        check_frontmatter_references(root, path, text, errors)

        for line_no, line in strip_fenced_code(text.splitlines()):
            for match in MD_LINK_RE.finditer(line):
                target = normalize_markdown_target(match.group(1))
                if not markdown_target_exists(root, path, target):
                    errors.append(f"{r}:{line_no}: Markdown 링크/이미지 대상 없음: {target}")
            for match in WIKI_LINK_RE.finditer(line):
                target = match.group(1)
                if not wiki_target_exists(root, path, target):
                    errors.append(f"{r}:{line_no}: Wiki 링크/임베드 대상 없음: [[{target}]]")

    return print_errors("references", errors)


if __name__ == "__main__":
    raise SystemExit(main())
