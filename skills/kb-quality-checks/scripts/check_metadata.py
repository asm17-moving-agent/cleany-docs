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

COMMON_REVIEW_VALUES = {"", "needs-human-review", "reviewed"}
COMMON_STATUS_VALUES = {"", "draft", "selected", "deprecated", "superseded", "active"}
COMMON_INGEST_VALUES = {"", "raw", "triaged", "converted", "reflected", "blocked"}


def required_keys_for(path: str) -> list[str]:
    if path.startswith("10_PLANNING/"):
        return ["type", "status", "review_status", "source_refs", "related_decisions", "related_jira", "updated", "tags"]
    if path.startswith("20_TECHNICAL/"):
        return ["type", "status", "review_status", "source_refs", "related_decisions", "related_jira", "updated", "tags"]
    if path.startswith("00_START_HERE/"):
        return ["type", "status", "review_status", "updated", "tags"]
    if path == "30_DECISIONS/00 - Decision Index.md":
        return ["type", "status", "review_status", "updated", "tags"]
    if path.startswith("30_DECISIONS/Planning/") or path.startswith("30_DECISIONS/Technical/"):
        return [
            "type",
            "decision_type",
            "status",
            "review_status",
            "date",
            "source_refs",
            "reflected_in",
            "related_jira",
            "updated",
            "tags",
        ]
    if path.startswith("40_RAW/"):
        return ["type", "review_status", "ingest_status", "tags"]
    if path.startswith("90_TEMPLATES/"):
        return ["type", "tags"]
    if (path.startswith("skills/") or path.startswith(".agents/skills/")) and path.endswith("/SKILL.md"):
        return ["name", "description", "tags"]
    return []


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


def expected_type(path: str) -> str | None:
    if path.startswith("10_PLANNING/"):
        return "planning"
    if path.startswith("20_TECHNICAL/"):
        return "technical"
    if path == "30_DECISIONS/00 - Decision Index.md":
        return "decision-index"
    if path.startswith("30_DECISIONS/Planning/") or path.startswith("30_DECISIONS/Technical/"):
        return "decision"
    return None


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

        data, raw, fm_err = frontmatter_block(text)
        if fm_err:
            errors.append(f"{r}: {fm_err}")
            continue

        for key in required:
            if key not in data:
                errors.append(f"{r}: frontmatter 필수 key 누락: {key}")

        if "tags" in required and "tags" in data and not frontmatter_list(raw, "tags"):
            errors.append(f"{r}: tags는 하나 이상의 값을 가져야 함")

        exp_type = expected_type(r)
        if exp_type and data.get("type") != exp_type:
            errors.append(f"{r}: type은 '{exp_type}'이어야 함, 현재 '{data.get('type', '')}'")

        if "status" in data and data.get("status", "") not in COMMON_STATUS_VALUES:
            errors.append(f"{r}: 허용되지 않은 status 값: {data.get('status')}")
        if "review_status" in data and data.get("review_status", "") not in COMMON_REVIEW_VALUES:
            errors.append(f"{r}: 허용되지 않은 review_status 값: {data.get('review_status')}")
        if "ingest_status" in data and data.get("ingest_status", "") not in COMMON_INGEST_VALUES:
            errors.append(f"{r}: 허용되지 않은 ingest_status 값: {data.get('ingest_status')}")

        if r.startswith("30_DECISIONS/Planning/") and data.get("decision_type") not in {"", "planning"}:
            errors.append(f"{r}: Planning Decision의 decision_type은 planning이어야 함")
        if r.startswith("30_DECISIONS/Technical/") and data.get("decision_type") not in {"", "technical"}:
            errors.append(f"{r}: Technical Decision의 decision_type은 technical이어야 함")

    return print_errors("metadata", errors)


if __name__ == "__main__":
    raise SystemExit(main())
