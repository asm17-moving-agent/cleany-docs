#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

REPORTS = [
    ("review_flags_report", "review-flags-report.md", "Review Flags Report"),
    ("source_refs_report", "source-refs-report.md", "Source Refs Report"),
    ("decision_inventory", "decision-inventory.md", "Decision Inventory"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="KB audit 리포트를 일괄 출력하거나 생성한다.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--output-dir", "-o", help="지정하면 리포트를 파일로 생성한다. 생략하면 stdout으로 출력한다.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    script_dir = Path(__file__).resolve().parent

    if not args.output_dir:
        sys.path.insert(0, str(script_dir))
        for module_name, _, title in REPORTS:
            module = importlib.import_module(module_name)
            print(f"<!-- BEGIN {title} -->")
            print(module.generate(root).rstrip())
            print(f"<!-- END {title} -->")
            print()
        return 0

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    failed = 0
    for module_name, name, _ in REPORTS:
        out = output_dir / name
        script = f"{module_name}.py"
        result = subprocess.run([sys.executable, str(script_dir / script), str(root), "--output", str(out)], text=True)
        if result.returncode != 0:
            failed = 1
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
