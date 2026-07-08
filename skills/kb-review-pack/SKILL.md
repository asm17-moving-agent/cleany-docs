---
name: kb-review-pack
description: 끌리니 KB의 사람 검토 준비 패키지를 만든다. 품질 검사, audit 결과, Decision 상태, 미해결 질문, 다음 리뷰 액션을 한 번에 정리할 때 사용한다.
tags:
  - skill
  - review
  - audit
  - quality-checks
compatibility: Codex repo-scoped skill, instruction-only workflow
---

# KB Review Pack

이 skill은 끌리니 KB를 사람이 검토하기 전에 필요한 상태 정보를 한 번에 모으는 Codex 문서 리뷰 워크플로우다.

## 목적

- `.codex/prompts` custom prompt를 사용하지 않고 repo skill로 리뷰 흐름을 관리한다.
- `$kb-quality-checks`와 `$kb-audit` 결과를 기반으로 검토 패키지를 만든다.
- Planning, Technical, Decision, Raw의 상태를 분리해 사람이 판단할 수 있게 정리한다.
- 문서 내용을 자동 확정하거나 Decision을 `selected`로 승격하지 않는다.

## 입력

- 검토 범위: 전체 KB 또는 특정 폴더/문서
- 검토 목적: 기획 리뷰, 기술 리뷰, Sprint 준비, PR 전 검토, 외부 공유 전 검토
- 필요한 경우 기준 Raw 문서 또는 Decision 문서

## 워크플로우

1. 검토 범위를 확인한다.
2. 먼저 `$kb-quality-checks`를 실행해 결정적 오류를 확인한다.
3. 이어서 `$kb-audit`를 실행해 다음 항목을 확인한다.
   - 검토 플래그
   - source_refs 상태
   - Decision inventory
4. 필요한 경우 관련 문서를 읽어 리뷰 맥락을 확인한다.
   - `00_START_HERE/02 - Current Status.md`
   - `10_PLANNING/08 - Questions.md`
   - `30_DECISIONS/00 - Decision Index.md`
   - 검토 범위의 Planning/Technical 문서
5. 결과를 아래 형식으로 요약한다.
   - 결정적 검사 결과
   - Blocking issues
   - 사람 검토 필요 항목
   - Decision 후보와 draft Decision 상태
   - `Questions`에서 닫아야 할 질문
   - Jira issue 후보
   - 다음 작업 제안
6. 문서 수정이 필요한 경우 바로 확정하지 않고 수정 후보를 제안한다.

## 출력 형식

```text
검사 결과
- ...

Blocking issues
- ...

사람 검토 필요 항목
- ...

Decision 상태
- ...

다음 리뷰 액션
- ...
```

## 금지 사항

- 사람 검토 없이 `status: selected` 또는 `review_status: reviewed`로 바꾸지 않는다.
- Raw 문서를 공식 결정처럼 취급하지 않는다.
- 기획/기술 판단을 임의로 확정하지 않는다.
- Jira issue 본문에 문서 내용을 복붙하지 않는다.
- `.codex/prompts` custom prompt를 새로 만들거나 갱신하지 않는다.
