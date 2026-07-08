#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CHECKS = [
    "check_structure.py",
    "check_formatting.py",
    "check_metadata.py",
    "check_links.py",
    "check_prompts.py",
]


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) >= 2 else Path.cwd().resolve()
    script_dir = Path(__file__).resolve().parent
    failed = 0

    for script in CHECKS:
        print(f"\n== {script} ==", flush=True)
        result = subprocess.run([sys.executable, str(script_dir / script), str(root)], text=True)
        if result.returncode != 0:
            failed = 1

    if failed:
        print("\nFAIL deterministic checks", flush=True)
        return 1
    print("\nOK deterministic checks", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
