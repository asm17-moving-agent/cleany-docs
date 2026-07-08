#!/usr/bin/env python3
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path

from common import frontmatter_block, print_errors, read_text, repo_root_from_args

REQUIRED_SKILLS = [
    "office-to-markdown",
    "kb-doc-factory",
    "kb-ingest",
    "kb-review-pack",
    "kb-quality-checks",
    "kb-audit",
    "kb-maintenance",
    "kb-pr",
]

REQUIRED_SNIPPETS = {
    "kb-ingest": [
        "Raw 문서를 selected Decision처럼 취급하지 않는다",
        "사람 검토 없이 Decision을 `selected`로 바꾸지 않는다",
        "`review_status: needs-human-review`",
    ],
    "kb-review-pack": [
        "$kb-quality-checks",
        "$kb-audit",
        ".codex/prompts",
        "사람 검토 없이 `status: selected` 또는 `review_status: reviewed`로 바꾸지 않는다",
    ],
    "kb-quality-checks": [
        "Skill 검사",
        "deprecated `.codex/prompts`",
    ],
    "kb-pr": [
        "$kb-quality-checks",
        "draft PR",
    ],
}

FORBIDDEN_PATHS = [
    ".codex/prompts",
    "skills/kb-publish",
    ".agents/skills/kb-publish",
]


def check_skill_file(root: Path, skill_name: str, errors: list[str]) -> None:
    source = root / "skills" / skill_name / "SKILL.md"
    entrypoint = root / ".agents" / "skills" / skill_name / "SKILL.md"

    if not source.is_file():
        errors.append(f"skill 원본 없음: skills/{skill_name}/SKILL.md")
        return
    if not entrypoint.is_file():
        errors.append(f"Codex skill entrypoint 없음: .agents/skills/{skill_name}/SKILL.md")

    text, err = read_text(source)
    if err:
        errors.append(f"skills/{skill_name}/SKILL.md: {err}")
        return
    assert text is not None

    data, raw, fm_err = frontmatter_block(text)
    if fm_err:
        errors.append(f"skills/{skill_name}/SKILL.md: {fm_err}")
        return

    for key in ["name", "description", "tags"]:
        if key not in data:
            errors.append(f"skills/{skill_name}/SKILL.md: frontmatter 필수 key 누락: {key}")

    if data.get("name") != skill_name:
        errors.append(f"skills/{skill_name}/SKILL.md: name은 '{skill_name}'이어야 함")

    if not any(line.strip().startswith("-") for line in raw if "tags:" not in line):
        errors.append(f"skills/{skill_name}/SKILL.md: tags는 하나 이상의 값을 가져야 함")

    for snippet in REQUIRED_SNIPPETS.get(skill_name, []):
        if snippet not in text:
            errors.append(f"skills/{skill_name}/SKILL.md: 필수 workflow 안내 누락: {snippet}")


def main() -> int:
    root = repo_root_from_args(sys.argv)
    errors: list[str] = []

    for item in FORBIDDEN_PATHS:
        if (root / item).exists():
            errors.append(f"deprecated 또는 금지된 skill/prompt 경로 존재: {item}")

    for skill_name in REQUIRED_SKILLS:
        check_skill_file(root, skill_name, errors)

    return print_errors("skills", errors)


if __name__ == "__main__":
    raise SystemExit(main())
