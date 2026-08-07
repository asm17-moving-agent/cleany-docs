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

FORBIDDEN_METADATA_KEYS = {"status", "ingest_status", "source_refs", "related_decisions"}
DECISION_PREFIXES = ("30_DECISIONS/Planning/", "30_DECISIONS/Technical/")
RELATION_FIELDS = ("supersedes", "superseded_by")


def requires_date(path: str) -> bool:
    return path.startswith(DECISION_PREFIXES) or path == "90_TEMPLATES/Template - Decision.md"


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

        if data is None:
            if requires_date(r):
                errors.append(f"{r}: Decision 문서에 date frontmatter가 없음")
            continue

        for key in sorted(FORBIDDEN_METADATA_KEYS):
            if key in data:
                errors.append(f"{r}: 상태와 문서 관계를 폴더, Git과 본문 링크로 관리하므로 metadata key를 사용하지 않음: {key}")

        if requires_date(r) and "date" not in data:
            errors.append(f"{r}: Decision 문서의 frontmatter에 date가 없음")
        elif r.startswith(DECISION_PREFIXES) and not data.get("date"):
            errors.append(f"{r}: Decision 문서의 date가 비어 있음")

        for key in RELATION_FIELDS:
            value = data.get(key)
            if value is not None and not isinstance(value, (str, list)):
                errors.append(f"{r}: {key}는 문자열 또는 list여야 함")
            elif isinstance(value, list) and any(not isinstance(item, str) for item in value):
                errors.append(f"{r}: {key} 항목은 문자열이어야 함")

    return print_errors("metadata", errors)


if __name__ == "__main__":
    raise SystemExit(main())
