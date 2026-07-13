---
name: kb-quality-checks
description: 끌리니 기획 KB의 결정적 검사를 실행한다. Markdown formatting, Obsidian YAML metadata, 필수 폴더/파일 구조, 내부 링크, repo skill 구조를 확인할 때 사용한다.
tags:
  - skill
  - quality-checks
  - validation
compatibility: Python 3.11 이상, uv project 환경 사용, 외부 패키지 불필요
---

# KB Quality Checks

이 skill은 끌리니 기획 KB에서 사람이 검토하기 전에 자동으로 확인할 수 있는 결정적 검사를 모아둔다.

## 언제 사용하나

다음 작업 후 사용한다.

- Markdown 문서 생성 또는 수정
- Obsidian YAML frontmatter 수정
- 템플릿 수정
- repo skill 생성 또는 수정
- 폴더 구조 변경
- Raw 문서 ingest 후 공식 문서 반영안 작성

## 검사 범위

| 검사 | 스크립트 | 확인 내용 |
|---|---|---|
| 전체 검사 | `scripts/run_checks.py` | 아래 모든 검사를 순서대로 실행 |
| 구조 검사 | `scripts/check_structure.py` | 필수 폴더/파일 존재, 금지 파일 부재 |
| Formatting 검사 | `scripts/check_formatting.py` | UTF-8, 최종 newline, trailing whitespace, fence 균형 등 |
| YAML 검사 | `scripts/check_yaml.py` | Markdown frontmatter YAML 기본 문법, 중복 key, tab, quote 오류 |
| Metadata 검사 | `scripts/check_metadata.py` | Obsidian YAML frontmatter와 필수 key |
| 링크 검사 | `scripts/check_links.py` | Markdown 링크와 Obsidian wiki link 대상 존재 |
| Skill 검사 | `scripts/check_skills.py` | repo skill entrypoint, 필수 skill, deprecated `.codex/prompts` 부재 |

## 사용법

저장소 루트에서 실행한다.

```bash
uv run python skills/kb-quality-checks/scripts/run_checks.py .
```

개별 검사만 실행할 수도 있다.

```bash
uv run python skills/kb-quality-checks/scripts/check_formatting.py .
uv run python skills/kb-quality-checks/scripts/check_yaml.py .
uv run python skills/kb-quality-checks/scripts/check_metadata.py .
uv run python skills/kb-quality-checks/scripts/check_structure.py .
uv run python skills/kb-quality-checks/scripts/check_links.py .
uv run python skills/kb-quality-checks/scripts/check_skills.py .
```

## 결과 해석

- `OK`: 검사 통과
- `FAIL`: 수정이 필요한 결정적 오류 존재
- 종료 코드 `0`: 전체 통과
- 종료 코드 `1`: 하나 이상의 오류 존재

## 작업 규칙

- 검사 실패를 무시하고 공식 문서를 확정하지 않는다.
- 검사 실패가 판단을 요구하는 경우 기획 항목은 `10_PLANNING/99 - Questions.md`, 기술 항목은 `20_TECHNICAL/99 - Questions.md`에 질문으로 남긴다.
- `status: draft` 문서는 검사 통과 여부와 별개로 사람 검토 전까지 공식 문서가 아니다. `reviewed` 이상 상태에는 `reviewers`가 기록되어야 한다.
- 이 skill은 문서 품질을 확인할 뿐, 기획/기술 결정을 자동으로 확정하지 않는다.
