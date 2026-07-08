#!/usr/bin/env python3
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path

from common import print_errors, read_text, repo_root_from_args

PROMPTS = [
    ".codex/prompts/summarize-raw.md",
    ".codex/prompts/draft-decision.md",
    ".codex/prompts/update-docs.md",
    ".codex/prompts/sprint-brief.md",
    ".codex/prompts/review-docs.md",
]

REQUIRED_SNIPPETS = [
    "## Codex skill prompt 우선",
    "## 결정적 검사",
    "$kb-quality-checks",
    "$kb-ingest",
    "Codex 문서 작성 워크플로우",
]


def main() -> int:
    root = repo_root_from_args(sys.argv)
    errors: list[str] = []

    for item in PROMPTS:
        path = root / item
        if not path.is_file():
            errors.append(f"Codex prompt 없음: {item}")
            continue
        text, err = read_text(path)
        if err:
            errors.append(f"{item}: {err}")
            continue
        assert text is not None
        for snippet in REQUIRED_SNIPPETS:
            if snippet not in text:
                errors.append(f"{item}: 결정적 검사 안내 누락: {snippet}")

    return print_errors("prompts", errors)


if __name__ == "__main__":
    raise SystemExit(main())
