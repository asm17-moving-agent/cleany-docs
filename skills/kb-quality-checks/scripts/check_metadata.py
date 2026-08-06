#!/usr/bin/env python3
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path

from common import frontmatter_block, iter_markdown_files, print_errors, read_text, rel, repo_root_from_args

SKIP_FRONTMATTER = {
    "README.md",
    "AGENTS.md",
    "skills/kb-quality-checks/skill.md",
}

SKIP_PREFIXES = (
    "skills/kb-quality-checks/scripts/",
)

FORBIDDEN_METADATA_KEYS = {"status", "ingest_status", "source_refs", "related_decisions"}


def required_keys_for(path: str) -> list[str]:
    if path.startswith("30_DECISIONS/Planning/") or path.startswith("30_DECISIONS/Technical/"):
        return ["date"]
    if path.startswith("90_TEMPLATES/"):
        if path.endswith("Template - Decision.md"):
            return ["date"]
        return []
    if (path.startswith("skills/") or path.startswith(".agents/skills/")) and path.endswith("/SKILL.md"):
        return ["name", "description", "tags"]
    return []


def main() -> int:
    root = repo_root_from_args(sys.argv)
    errors: list[str] = []

    for path in iter_markdown_files(root):
        r = rel(path, root)
        if r in SKIP_FRONTMATTER or any(r.startswith(prefix) for prefix in SKIP_PREFIXES):
            continue

        required = required_keys_for(r)
        text, err = read_text(path)
        if err:
            errors.append(f"{r}: {err}")
            continue
        assert text is not None

        has_frontmatter = text.startswith("---\n") or text.startswith("---\r\n")
        if not required and not has_frontmatter:
            continue

        data, _, fm_err = frontmatter_block(text)
        if fm_err:
            errors.append(f"{r}: {fm_err}")
            continue

        for key in required:
            if key not in data:
                errors.append(f"{r}: frontmatter 필수 key 누락: {key}")

        for key in sorted(FORBIDDEN_METADATA_KEYS):
            if key in data:
                errors.append(f"{r}: 상태와 문서 관계를 폴더, Git과 본문 링크로 관리하므로 metadata key를 사용하지 않음: {key}")

    return print_errors("metadata", errors)


if __name__ == "__main__":
    raise SystemExit(main())
