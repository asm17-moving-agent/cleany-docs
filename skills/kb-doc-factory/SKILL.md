---
name: kb-doc-factory
description: 끌리니 KB의 템플릿 기반 문서를 LLM 없이 생성한다. Planning과 Technical 반영안, 실제 Decision 기록, Meeting, Research, Sprint Brief, Jira Issue 및 AI Log 문서 틀을 만들 때 사용한다.
tags:
  - skill
  - template
  - doc-factory
compatibility: Python 3.11 이상, 외부 패키지 불필요
---

# KB Doc Factory

이 skill은 `90_TEMPLATES`의 템플릿을 사용해 새 Markdown 문서를 deterministic하게 생성한다.

## 사용 원칙

- 템플릿 치환과 파일 생성만 수행한다.
- 기획/기술 내용을 자동 작성하지 않는다.
- Raw에서 Planning/Decision 내용으로 변환할 때는 `$kb-ingest`를 사용한다.
- 생성된 Planning, Technical 및 Decision 문서는 검토 중인 반영안이며 사람 검토 전에는 현재 기준이 아니다.
- Decision 문서는 실제 결정이 확인된 경우에만 생성한다.
- 이미 파일이 있으면 기본적으로 덮어쓰지 않는다.

## 사용법

Planning 문서 반영안:

```bash
uv run python skills/kb-doc-factory/scripts/new_doc.py planning "운영자 페르소나" --output "10_PLANNING/06 - Operator Persona.md"
```

Technical 문서 반영안:

```bash
uv run python skills/kb-doc-factory/scripts/new_doc.py technical "관제 대시보드 개념" --output "20_TECHNICAL/09 - Dashboard Concept.md"
```

Decision 기록:

```bash
uv run python skills/kb-doc-factory/scripts/new_doc.py decision "MVP 범위 확정" --decision-type planning --date 2026-07-08
```

회의록:

```bash
uv run python skills/kb-doc-factory/scripts/new_doc.py meeting "MVP 범위 회의" --date 2026-07-08
```

조사 노트:

```bash
uv run python skills/kb-doc-factory/scripts/new_doc.py research "무인 스터디카페 현장 조사" --date 2026-07-08
```

## 지원 kind

- `planning`
- `technical`
- `decision`
- `meeting`
- `research`
- `raw-ingest`
- `sprint`
- `jira`
- `ai-log`
