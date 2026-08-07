#!/usr/bin/env python3
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

from common import print_errors, repo_root_from_args

REQUIRED_DIRS = [
    "00_START_HERE",
    "10_PLANNING",
    "20_TECHNICAL",
    "30_DECISIONS",
    "40_RAW",
    "40_RAW/assets",
    "90_TEMPLATES",
]

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
]


def main() -> int:
    root = repo_root_from_args(sys.argv)
    errors: list[str] = []

    for item in REQUIRED_DIRS:
        if not (root / item).is_dir():
            errors.append(f"필수 폴더 없음: {item}")

    for item in REQUIRED_FILES:
        if not (root / item).is_file():
            errors.append(f"필수 파일 없음: {item}")

    return print_errors("structure", errors)


if __name__ == "__main__":
    raise SystemExit(main())
