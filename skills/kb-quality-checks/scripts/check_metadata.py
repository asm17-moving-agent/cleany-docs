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

COMMON_STATUS_VALUES = {"", "draft", "reviewed", "selected", "dropped"}
COMMON_INGEST_VALUES = {"", "raw", "triaged", "converted", "reflected", "blocked"}


def required_keys_for(path: str) -> list[str]:
    if path.startswith("10_PLANNING/"):
        return ["status", "source_refs", "related_decisions"]
    if path.startswith("20_TECHNICAL/"):
        return ["status", "source_refs", "related_decisions"]
    if path.startswith("00_START_HERE/"):
        return ["status"]
    if path == "30_DECISIONS/00 - Decision Index.md":
        return ["status"]
    if path.startswith("30_DECISIONS/Planning/") or path.startswith("30_DECISIONS/Technical/"):
        return ["status", "date", "source_refs"]
    if path.startswith("40_RAW/"):
        return ["ingest_status"]
    if path.startswith("90_TEMPLATES/"):
        if path.endswith(("Template - Planning Doc.md", "Template - Technical Doc.md")):
            return ["status", "source_refs", "related_decisions"]
        if path.endswith("Template - Decision.md"):
            return ["status", "date", "source_refs"]
        return ["ingest_status"]
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
        if not required:
            continue

        text, err = read_text(path)
        if err:
            errors.append(f"{r}: {err}")
            continue
        assert text is not None

        data, _, fm_err = frontmatter_block(text)
        if fm_err:
            errors.append(f"{r}: {fm_err}")
            continue

        for key in required:
            if key not in data:
                errors.append(f"{r}: frontmatter 필수 key 누락: {key}")

        if "status" in data and data.get("status", "") not in COMMON_STATUS_VALUES:
            errors.append(f"{r}: 허용되지 않은 status 값: {data.get('status')}")
        if "ingest_status" in data and data.get("ingest_status", "") not in COMMON_INGEST_VALUES:
            errors.append(f"{r}: 허용되지 않은 ingest_status 값: {data.get('ingest_status')}")

    return print_errors("metadata", errors)


if __name__ == "__main__":
    raise SystemExit(main())
