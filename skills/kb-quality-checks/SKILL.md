---
name: kb-quality-checks
description: 끌리니 KB의 공유 가능한 무결성을 검사한다. 문서, metadata, 폴더와 repo skill을 바꾼 뒤 핵심 구조, YAML, 내부 참조와 skill 진입점을 확인할 때 사용한다.
---

# KB Quality Checks

이 skill은 사람의 내용 검토 전에 자동 판정할 수 있는 KB 무결성만 확인한다.

## 검사 범위

| 검사 | 스크립트 | 확인 내용 |
|---|---|---|
| 전체 검사 | `scripts/run_checks.py` | 아래 모든 검사를 순서대로 실행 |
| 구조 검사 | `scripts/check_structure.py` | 핵심 계층, `40_RAW/assets`, 루트 안내 문서 존재 |
| YAML 검사 | `scripts/check_yaml.py` | frontmatter 문법, 구분자, 중복 key |
| Metadata 검사 | `scripts/check_metadata.py` | Decision 날짜와 금지된 상태 및 관계 metadata 부재 |
| 참조 검사 | `scripts/check_references.py` | Markdown 링크와 이미지, wiki link와 embed 대상 존재 |
| Skill 검사 | `scripts/check_skills.py` | 발견된 repo skill manifest와 Codex 진입점 일치 |

다음 항목은 CI 실패 조건으로 삼지 않는다.

- 핵심 계층 밖의 개별 문서와 폴더 이름
- 공백, 줄바꿈과 표 정렬 같은 Markdown 스타일
- 특정 skill 목록이나 본문의 고정 문구
- 문서 내용의 사실성, 검토 완료 여부, 결정의 승인 여부

## 사용법

저장소 루트에서 실행한다.

```bash
uv run --locked --only-group quality python skills/kb-quality-checks/scripts/run_checks.py .
```

개별 검사만 실행할 수도 있다.

```bash
uv run --locked --only-group quality python skills/kb-quality-checks/scripts/check_yaml.py .
uv run --locked --only-group quality python skills/kb-quality-checks/scripts/check_references.py .
```

## 결과 해석

- `OK`: 검사 통과
- `FAIL`: 수정이 필요한 결정적 오류 존재
- 종료 코드 `0`: 전체 통과
- 종료 코드 `1`: 하나 이상의 오류 존재

## 작업 규칙

- 무결성 검사 실패를 무시하고 공유하지 않는다.
- 검사 실패가 판단을 요구하는 경우 기획 항목은 `10_PLANNING/99 - Questions.md`,
  기술 항목은 `20_TECHNICAL/99 - Questions.md`에 질문으로 남긴다.
- 검사 통과는 내용 승인과 별개다. 작업 브랜치의 변경은 사람 검토 전까지 현재
  기준이 아니다. 검토자와 승인 이력은 GitHub PR에서 관리한다.
- 이 skill은 문서 품질을 확인할 뿐, 기획/기술 결정을 자동으로 확정하지 않는다.
