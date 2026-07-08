#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True

DEFAULT_INCLUDE = [
    "README.md",
    "00_START_HERE",
    "10_PLANNING",
    "20_TECHNICAL",
    "30_DECISIONS",
]
RAW_SUMMARY = "40_RAW/20_Planning/기획서 원문 요약.md"


def copy_path(root: Path, output: Path, rel: str) -> None:
    src = root / rel
    dst = output / rel
    if src.is_dir():
        for path in src.rglob("*"):
            if path.is_file():
                target = output / path.relative_to(root)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
    elif src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def write_manifest(output: Path, included: list[str]) -> None:
    lines = [
        "# Stable View Manifest",
        "",
        "이 폴더는 공유 가능한 stable view로 생성된 사본이다.",
        "",
        "## 포함 대상",
        "",
    ]
    for item in included:
        lines.append(f"- `{item}`")
    lines.extend([
        "",
        "## 제외 대상",
        "",
        "- `40_RAW` 전체",
        "- `.agents`",
        "- `.codex`",
        "- `skills`",
        "- `.venv`",
    ])
    (output / "STABLE_VIEW_MANIFEST.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="공유용 stable view를 생성한다.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--include-raw-summary", action="store_true")
    parser.add_argument("--clean", action="store_true", help="출력 폴더를 먼저 삭제")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output = Path(args.output).resolve()
    if output == root or root in output.parents and output.relative_to(root).parts[:1] in [("00_START_HERE",), ("10_PLANNING",), ("20_TECHNICAL",), ("30_DECISIONS",), ("40_RAW",)]:
        print("공식 KB 폴더 내부를 output으로 사용할 수 없음", file=sys.stderr)
        return 1
    if output.exists() and args.clean:
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    included = list(DEFAULT_INCLUDE)
    if args.include_raw_summary:
        included.append(RAW_SUMMARY)

    for item in included:
        if not (root / item).exists():
            print(f"경고: 포함 대상 없음: {item}", file=sys.stderr)
            continue
        copy_path(root, output, item)
    write_manifest(output, included)
    print(f"stable view generated: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
