#!/usr/bin/env python3
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from common import (
    iter_markdown_files,
    load_frontmatter,
    print_errors,
    read_text,
    rel,
    repo_root_from_args,
)

OFFICIAL_PREFIXES = ("10_PLANNING/", "20_TECHNICAL/", "30_DECISIONS/")
STATUS_VALUES = {"draft", "reviewed", "selected", "dropped"}
INGEST_STATUS_VALUES = {"raw", "triaged", "converted", "reflected", "blocked"}
LIST_FIELDS = ("source_refs", "related_decisions")


def main() -> int:
    root = repo_root_from_args(sys.argv)
    errors: list[str] = []

    for path in iter_markdown_files(root):
        r = rel(path, root)
        text, err = read_text(path)
        if err:
            errors.append(f"{r}: {err}")
            continue
        assert text is not None

        data, fm_err = load_frontmatter(text)
        if fm_err:
            errors.append(f"{r}: {fm_err}")
            continue

        is_official = r.startswith(OFFICIAL_PREFIXES)
        if data is None:
            if is_official:
                errors.append(f"{r}: 공식 문서에 status frontmatter가 없음")
            continue

        if is_official and "status" not in data:
            errors.append(f"{r}: 공식 문서의 frontmatter에 status가 없음")

        if "status" in data and data["status"] not in STATUS_VALUES:
            errors.append(f"{r}: 허용되지 않은 status 값: {data.get('status')}")
        if "ingest_status" in data and data["ingest_status"] not in INGEST_STATUS_VALUES:
            errors.append(f"{r}: 허용되지 않은 ingest_status 값: {data.get('ingest_status')}")

        for key in LIST_FIELDS:
            value = data.get(key)
            if value is not None and not isinstance(value, list):
                errors.append(f"{r}: {key}는 list여야 함")
            elif isinstance(value, list) and any(
                item is not None and not isinstance(item, str) for item in value
            ):
                errors.append(f"{r}: {key} 항목은 문자열이어야 함")

        source_file = data.get("source_file")
        if source_file is not None and not isinstance(source_file, str):
            errors.append(f"{r}: source_file은 문자열이어야 함")

        supersedes = data.get("supersedes")
        if supersedes is not None and not isinstance(supersedes, (str, list)):
            errors.append(f"{r}: supersedes는 문자열 또는 list여야 함")

    return print_errors("metadata", errors)


if __name__ == "__main__":
    raise SystemExit(main())
