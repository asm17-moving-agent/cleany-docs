#!/usr/bin/env python3
from __future__ import annotations

import sys

sys.dont_write_bytecode = True
from pathlib import Path

from common import load_frontmatter, print_errors, read_text, repo_root_from_args


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

    data, fm_err = load_frontmatter(text)
    if fm_err:
        errors.append(f"skills/{skill_name}/SKILL.md: {fm_err}")
        return
    if data is None:
        errors.append(f"skills/{skill_name}/SKILL.md: YAML frontmatter가 파일 시작에 없음")
        return

    for key in ("name", "description"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"skills/{skill_name}/SKILL.md: {key}은 비어 있지 않은 문자열이어야 함")

    if data.get("name") != skill_name:
        errors.append(f"skills/{skill_name}/SKILL.md: name은 '{skill_name}'이어야 함")

    if entrypoint.is_file() and entrypoint.resolve() != source.resolve():
        errors.append(f"Codex skill entrypoint가 원본을 가리키지 않음: .agents/skills/{skill_name}")


def main() -> int:
    root = repo_root_from_args(sys.argv)
    errors: list[str] = []

    skills_root = root / "skills"
    entrypoints_root = root / ".agents" / "skills"
    if not skills_root.is_dir():
        errors.append("skill 원본 폴더 없음: skills")
        return print_errors("skills", errors)
    if not entrypoints_root.is_dir():
        errors.append("Codex skill entrypoint 폴더 없음: .agents/skills")
        return print_errors("skills", errors)

    source_names: set[str] = set()
    source_directories = (
        path
        for path in skills_root.iterdir()
        if path.is_dir() and not path.name.startswith((".", "__"))
    )
    for directory in sorted(source_directories):
        source_names.add(directory.name)
        check_skill_file(root, directory.name, errors)

    entrypoint_names = {path.name for path in entrypoints_root.iterdir()}
    for skill_name in sorted(entrypoint_names - source_names):
        errors.append(f"원본 없는 Codex skill entrypoint: .agents/skills/{skill_name}")

    return print_errors("skills", errors)


if __name__ == "__main__":
    raise SystemExit(main())
