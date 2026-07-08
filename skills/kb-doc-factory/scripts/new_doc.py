#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.dont_write_bytecode = True

TEMPLATES = {
    "planning": "90_TEMPLATES/Template - Planning Doc.md",
    "technical": "90_TEMPLATES/Template - Technical Doc.md",
    "decision": "90_TEMPLATES/Template - Decision.md",
    "meeting": "90_TEMPLATES/Template - Meeting Note.md",
    "research": "90_TEMPLATES/Template - Research Note.md",
    "raw-ingest": "90_TEMPLATES/Template - Raw Ingest Summary.md",
    "sprint": "90_TEMPLATES/Template - Sprint Brief.md",
    "jira": "90_TEMPLATES/Template - Jira Issue.md",
    "ai-log": "90_TEMPLATES/Template - AI Interaction Log.md",
}

DEFAULT_DIRS = {
    "planning": "10_PLANNING",
    "technical": "20_TECHNICAL",
    "meeting": "40_RAW/10_Meetings",
    "research": "40_RAW/40_Research",
    "raw-ingest": "40_RAW/00_Inbox",
    "sprint": "40_RAW/60_External_Artifacts/Sprint_Briefs",
    "jira": "40_RAW/60_External_Artifacts/Jira_Issue_Drafts",
    "ai-log": "40_RAW/70_AI_Interaction_Logs",
}


def parse_date(value: str | None) -> date:
    if not value:
        return date.today()
    return datetime.strptime(value, "%Y-%m-%d").date()


def yymmdd(d: date) -> str:
    return d.strftime("%y%m%d")


def sanitize_filename(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]", "-", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or "Untitled"


def default_output(kind: str, title: str, d: date, decision_type: str) -> Path:
    safe = sanitize_filename(title)
    yy = yymmdd(d)
    if kind == "decision":
        folder = "30_DECISIONS/Planning" if decision_type == "planning" else "30_DECISIONS/Technical"
        return Path(folder) / f"{yy} - {safe}.md"
    if kind == "meeting":
        return Path(DEFAULT_DIRS[kind]) / f"{yy} - {safe}.md"
    if kind == "research":
        return Path(DEFAULT_DIRS[kind]) / f"{yy} - {safe}.md"
    if kind == "raw-ingest":
        return Path(DEFAULT_DIRS[kind]) / f"{yy} - Raw Ingest Summary - {safe}.md"
    if kind == "sprint":
        return Path(DEFAULT_DIRS[kind]) / f"{yy} - Sprint Brief.md"
    if kind == "ai-log":
        return Path(DEFAULT_DIRS[kind]) / f"{yy} - {safe}.md"
    if kind == "jira":
        return Path(DEFAULT_DIRS[kind]) / f"Jira Issue - {safe}.md"
    return Path(DEFAULT_DIRS[kind]) / f"{safe}.md"


def replace_frontmatter_value(text: str, key: str, value: str) -> str:
    return re.sub(rf"^{re.escape(key)}:[ \t]*.*$", f"{key}: {value}", text, count=1, flags=re.MULTILINE)


def render(template: str, kind: str, title: str, d: date, decision_type: str) -> str:
    yy = yymmdd(d)
    iso = d.isoformat()
    text = template

    if kind == "planning":
        text = text.replace("# 문서 제목", f"# {title}")
        text = replace_frontmatter_value(text, "updated", iso)
    elif kind == "technical":
        text = text.replace("# 문서 제목", f"# {title}")
        text = replace_frontmatter_value(text, "updated", iso)
    elif kind == "decision":
        text = text.replace("# YYMMDD - 결정 제목", f"# {yy} - {title}")
        text = replace_frontmatter_value(text, "decision_type", decision_type)
        text = replace_frontmatter_value(text, "date", iso)
        text = replace_frontmatter_value(text, "updated", iso)
    elif kind == "meeting":
        text = text.replace("# YYMMDD - 회의 제목", f"# {yy} - {title}")
        text = replace_frontmatter_value(text, "date", iso)
    elif kind == "research":
        text = text.replace("# YYMMDD - 조사 제목", f"# {yy} - {title}")
        text = replace_frontmatter_value(text, "date", iso)
    elif kind == "raw-ingest":
        text = text.replace("# YYMMDD - Raw Ingest Summary", f"# {yy} - Raw Ingest Summary - {title}")
    elif kind == "sprint":
        text = text.replace("# YYMMDD - Sprint Brief", f"# {yy} - Sprint Brief")
        text = replace_frontmatter_value(text, "date", iso)
    elif kind == "ai-log":
        text = text.replace("# YYMMDD - AI 작업 제목", f"# {yy} - {title}")
        text = replace_frontmatter_value(text, "date", iso)
    elif kind == "jira":
        text = text.replace("# Jira Issue 제목", f"# {title}")

    return text.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="템플릿 기반 KB 문서를 생성한다.")
    parser.add_argument("kind", choices=sorted(TEMPLATES))
    parser.add_argument("title")
    parser.add_argument("--date", help="YYYY-MM-DD. 생략 시 오늘 날짜")
    parser.add_argument("--decision-type", choices=["planning", "technical"], default="planning")
    parser.add_argument("--output", "-o", help="출력 경로. 생략 시 kind별 기본 위치")
    parser.add_argument("--force", action="store_true", help="기존 파일 덮어쓰기")
    args = parser.parse_args()

    root = Path.cwd()
    d = parse_date(args.date)
    template_path = root / TEMPLATES[args.kind]
    if not template_path.is_file():
        print(f"템플릿 없음: {template_path}", file=sys.stderr)
        return 1

    output = Path(args.output) if args.output else default_output(args.kind, args.title, d, args.decision_type)
    output = output if output.is_absolute() else root / output
    if output.exists() and not args.force:
        print(f"이미 파일이 있음: {output}. 덮어쓰려면 --force 사용", file=sys.stderr)
        return 1

    content = render(template_path.read_text(encoding="utf-8"), args.kind, args.title, d, args.decision_type)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(f"created: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
