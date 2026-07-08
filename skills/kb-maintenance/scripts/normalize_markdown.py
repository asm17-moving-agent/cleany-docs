#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.dont_write_bytecode = True

EXCLUDED_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".obsidian"}


def iter_markdown(root: Path):
    for path in root.rglob("*.md"):
        if any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip(" \t") for line in text.split("\n")]
    normalized = "\n".join(lines)
    normalized = normalized.rstrip("\n") + "\n"
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description="Markdown formatting을 deterministic하게 검사/정리한다.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--write", action="store_true", help="파일을 실제로 수정")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    changed: list[str] = []
    for path in iter_markdown(root):
        original = path.read_text(encoding="utf-8")
        normalized = normalize_text(original)
        if original != normalized:
            changed.append(str(path.relative_to(root)))
            if args.write:
                path.write_text(normalized, encoding="utf-8")

    if changed:
        action = "수정됨" if args.write else "수정 필요"
        print(f"{action}: {len(changed)}개 파일")
        for item in changed:
            print(f"- {item}")
        return 0 if args.write else 1

    print("OK markdown normalize")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
