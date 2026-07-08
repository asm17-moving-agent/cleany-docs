#!/usr/bin/env python3
from __future__ import annotations

import re
import sys

sys.dont_write_bytecode = True
from pathlib import Path

from common import iter_markdown_files, print_errors, read_text, rel, repo_root_from_args, strip_fenced_code


def main() -> int:
    root = repo_root_from_args(sys.argv)
    errors: list[str] = []
    fence_re = re.compile(r"^\s*(```+|~~~+)")

    for path in iter_markdown_files(root):
        text, err = read_text(path)
        r = rel(path, root)
        if err:
            errors.append(f"{r}: {err}")
            continue

        assert text is not None
        if "\r\n" in text:
            errors.append(f"{r}: CRLF 대신 LF newline을 사용해야 함")
        if text and not text.endswith("\n"):
            errors.append(f"{r}: 파일 끝 newline 누락")

        lines = text.splitlines()
        for idx, line in enumerate(lines, start=1):
            if line.rstrip(" \t") != line:
                errors.append(f"{r}:{idx}: trailing whitespace 존재")

        for idx, line in strip_fenced_code(lines):
            if "\t" in line:
                errors.append(f"{r}:{idx}: 코드 블록 밖 tab 문자 사용")

        in_fence = False
        fence_marker = ""
        for line in lines:
            m = fence_re.match(line)
            if not m:
                continue
            marker = m.group(1)[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
        if in_fence:
            errors.append(f"{r}: 닫히지 않은 fenced code block 존재")

        if text.startswith("---"):
            if not (text.startswith("---\n") or text.startswith("---\r\n")):
                errors.append(f"{r}: frontmatter 시작 구분자는 단독 '---' 라인이어야 함")
            elif len([line for line in lines if line.strip() == "---"]) < 2:
                errors.append(f"{r}: frontmatter 종료 구분자 누락")

    return print_errors("formatting", errors)


if __name__ == "__main__":
    raise SystemExit(main())
