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
    "30_DECISIONS/Planning",
    "30_DECISIONS/Technical",
    "40_RAW",
    "40_RAW/00_Inbox",
    "40_RAW/10_Meetings",
    "40_RAW/20_Planning",
    "40_RAW/30_Technical_Notes",
    "40_RAW/40_Research",
    "40_RAW/50_Mentor_Feedback",
    "40_RAW/60_External_Artifacts",
    "90_TEMPLATES",
    ".agents",
    ".agents/skills",
    ".agents/skills/kb-quality-checks",
    ".agents/skills/kb-ingest",
    ".agents/skills/office-to-markdown",
    ".agents/skills/kb-maintenance",
    ".agents/skills/kb-doc-factory",
    ".agents/skills/kb-audit",
    ".agents/skills/kb-review-pack",
    ".agents/skills/kb-pr",
    "skills/kb-quality-checks",
    "skills/kb-quality-checks/scripts",
    "skills/office-to-markdown",
    "skills/office-to-markdown/scripts",
    "skills/kb-maintenance",
    "skills/kb-maintenance/scripts",
    "skills/kb-doc-factory",
    "skills/kb-doc-factory/scripts",
    "skills/kb-audit",
    "skills/kb-audit/scripts",
    "skills/kb-review-pack",
    "skills/kb-pr",
]

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "pyproject.toml",
    "uv.lock",
    ".gitignore",
    "00_START_HERE/00 - README.md",
    "00_START_HERE/01 - Reading Guide.md",
    "00_START_HERE/02 - Current Status.md",
    "00_START_HERE/03 - Glossary.md",
    "10_PLANNING/00 - Project Brief.md",
    "10_PLANNING/01 - Problem and Users.md",
    "10_PLANNING/02 - Target Scenario.md",
    "10_PLANNING/04 - Scope and Non-Goals.md",
    "10_PLANNING/05 - Success Criteria.md",
    "10_PLANNING/08 - Questions.md",
    "20_TECHNICAL/00 - Technical Overview.md",
    "20_TECHNICAL/01 - System Concept.md",
    "20_TECHNICAL/03 - Rule-based VLA Architecture.md",
    "20_TECHNICAL/04 - Robot Platform XLeRobot.md",
    "20_TECHNICAL/05 - Navigation and Mapping.md",
    "20_TECHNICAL/06 - Edge Runtime Jetson Orin.md",
    "20_TECHNICAL/07 - Data and Evaluation.md",
    "20_TECHNICAL/08 - Safety and Risk.md",
    "30_DECISIONS/00 - Decision Index.md",
    "30_DECISIONS/Planning/.gitkeep",
    "30_DECISIONS/Technical/.gitkeep",
    "40_RAW/00_Inbox/.gitkeep",
    "40_RAW/10_Meetings/.gitkeep",
    "40_RAW/20_Planning/기획서 원문 요약.md",
    "40_RAW/30_Technical_Notes/.gitkeep",
    "40_RAW/40_Research/.gitkeep",
    "40_RAW/50_Mentor_Feedback/.gitkeep",
    "90_TEMPLATES/Template - Planning Doc.md",
    "90_TEMPLATES/Template - Technical Doc.md",
    "90_TEMPLATES/Template - Decision.md",
    "90_TEMPLATES/Template - Meeting Note.md",
    "90_TEMPLATES/Template - Research Note.md",
    "90_TEMPLATES/Template - Raw Ingest Summary.md",
    "90_TEMPLATES/Template - Sprint Brief.md",
    "90_TEMPLATES/Template - Jira Issue.md",
    "90_TEMPLATES/Template - AI Interaction Log.md",
    ".agents/skills/kb-quality-checks/SKILL.md",
    ".agents/skills/kb-ingest/SKILL.md",
    ".agents/skills/office-to-markdown/SKILL.md",
    ".agents/skills/kb-maintenance/SKILL.md",
    ".agents/skills/kb-doc-factory/SKILL.md",
    ".agents/skills/kb-audit/SKILL.md",
    ".agents/skills/kb-review-pack/SKILL.md",
    ".agents/skills/kb-pr/SKILL.md",
    "skills/README.md",
    "skills/kb-ingest/SKILL.md",
    "skills/kb-quality-checks/SKILL.md",
    "skills/kb-quality-checks/scripts/run_checks.py",
    "skills/kb-quality-checks/scripts/check_formatting.py",
    "skills/kb-quality-checks/scripts/check_metadata.py",
    "skills/kb-quality-checks/scripts/check_yaml.py",
    "skills/kb-quality-checks/scripts/check_structure.py",
    "skills/kb-quality-checks/scripts/check_links.py",
    "skills/kb-quality-checks/scripts/check_skills.py",
    "skills/kb-quality-checks/scripts/common.py",
    "skills/office-to-markdown/SKILL.md",
    "skills/office-to-markdown/scripts/office_to_markdown.py",
    "skills/kb-maintenance/SKILL.md",
    "skills/kb-maintenance/scripts/normalize_markdown.py",
    "skills/kb-maintenance/scripts/generate_file_index.py",
    "skills/kb-maintenance/scripts/metadata_report.py",
    "skills/kb-doc-factory/SKILL.md",
    "skills/kb-doc-factory/scripts/new_doc.py",
    "skills/kb-audit/SKILL.md",
    "skills/kb-audit/scripts/common.py",
    "skills/kb-audit/scripts/review_flags_report.py",
    "skills/kb-audit/scripts/source_refs_report.py",
    "skills/kb-audit/scripts/decision_inventory.py",
    "skills/kb-audit/scripts/audit_all.py",
    "skills/kb-review-pack/SKILL.md",
    "skills/kb-pr/SKILL.md",
]

FORBIDDEN_NAMES = {"CLAUDE.md"}
FORBIDDEN_DIRS = {".claude", "50_WORKING", "kb-publish", "prompts"}
SKIP_DIRS = {".git", ".venv", ".obsidian", ".codex"}


def main() -> int:
    root = repo_root_from_args(sys.argv)
    errors: list[str] = []

    for item in REQUIRED_DIRS:
        if not (root / item).is_dir():
            errors.append(f"필수 폴더 없음: {item}")

    for item in REQUIRED_FILES:
        if not (root / item).is_file():
            errors.append(f"필수 파일 없음: {item}")

    for path in root.iterdir():
        if path.name in SKIP_DIRS:
            continue
        for nested in path.rglob("*"):
            if nested.name in FORBIDDEN_NAMES:
                errors.append(f"금지 파일 존재: {nested.relative_to(root)}")
            if nested.is_dir() and nested.name in FORBIDDEN_DIRS:
                errors.append(f"금지 폴더 존재: {nested.relative_to(root)}")

    return print_errors("structure", errors)


if __name__ == "__main__":
    raise SystemExit(main())
