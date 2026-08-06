---
name: kb-ingest
description: 40_RAW의 회의록, 조사자료, 기획서 요약을 근거로 Planning/Technical 반영안을 만들고, 실제 결정이 확인된 경우 Decision을 기록한다. Raw를 보존하면서 source_refs와 related_decisions를 연결할 때 사용한다.
compatibility: Codex repo-scoped skill, instruction-only workflow
tags:
  - skill
  - ingest
  - raw
  - planning
  - decision
---

# KB Ingest

이 skill은 `40_RAW`의 초안, 학습 노트, 회의록, 조사 내용, 기획서 요약을 근거로
Planning·Technical 반영안을 만들고 실제로 확인된 결정을 기록하는 Codex 문서 작성
워크플로우다.

## 목적

- Raw 기록을 공식 지식처럼 취급하지 않는다.
- Raw에서 나온 논의와 결정 후보는 원문과 문서 링크로 추적한다.
- 실제 결정이 확인되기 전에는 Decision 문서를 만들지 않는다.
- Planning·Technical 반영안은 작업 브랜치에서 만들고 `source_refs`와 `related_decisions`를 갱신한다.
- 폴더는 지식의 성격을, Git 브랜치와 PR은 검토 상태를 나타낸다.

## 입력

- Raw 문서 경로: `40_RAW` 루트 또는 하위 작업 폴더의 Markdown 문서
- 변환 목표: `planning`, `decision`, 또는 `planning+decision`
- 필요한 경우 대상 Planning 문서 경로
- 필요한 경우 Decision 제목과 decision_type: `planning` 또는 `technical`

## 워크플로우

1. Raw 문서를 끝까지 읽는다.
2. Raw frontmatter를 확인하고 필요한 경우 아래 관계 metadata를 갱신한다.
   - `ingest_targets`
   - `decision_candidates`
3. Raw 본문에서 다음 항목을 추출한다.
   - 핵심 논의
   - 결정 후보
   - Planning 반영 후보
   - Technical 반영 후보
   - 미해결 질문
   - Jira issue 후보
4. Decision 후보인지 판단한다. 아래 조건 중 2개 이상이면 Raw의
   `decision_candidates`에 남기되 Decision 문서를 자동 생성하지 않는다.
   - 프로젝트 방향에 영향을 준다.
   - 나중에 번복하면 비용이 크다.
   - Planning 또는 Technical 문서의 핵심 내용을 바꾼다.
   - Sprint 계획이나 Jira Epic/Story 구조에 영향을 준다.
   - 멘토나 리뷰어가 질문할 가능성이 높다.
   - 기술 리스크 또는 안전 리스크에 영향을 준다.
5. 회의록·사용자 지시·승인 기록에서 실제 결정이 확인된 경우에만 작업 브랜치에 Decision 문서를 만든다.
   - 선택한 내용을 `결정`에 명확히 적는다.
   - `source_refs`에 Raw 문서 경로를 반드시 넣는다.
   - Decision은 `source_refs`로 Raw만 참조한다. Planning·Technical 반영 문서는 역링크하지 않는다.
   - 검토자와 승인 이력은 GitHub PR에 남긴다.
6. Planning 문서를 갱신할 때는 다음을 지킨다.
   - 기획서나 Raw에 없는 내용을 확정하지 않는다.
   - `source_refs`에 Raw 문서 경로를 추가한다.
   - 관련 Decision이 있으면 `related_decisions`에 추가한다.
   - 실제로 미결정인 내용은 공식 본문에서 확정하지 않고 Questions와 연결한다.
7. 미해결 질문은 계층에 따라 중앙 Questions 문서에 추가한다.
   - 사용자, 가치, 제품 범위, 시나리오, 성공 기준, 프로젝트 운영 질문: `10_PLANNING/99 - Questions.md`
   - 시스템 구조, 인터페이스, 하드웨어, 런타임, 데이터, 평가, 안전 질문: `20_TECHNICAL/99 - Questions.md`
   - 두 계층에 걸친 주제는 제품 선택과 기술 구현 경계를 분리하고 같은 질문을 중복 기록하지 않는다.
   - LLM이 가능한 질문을 추측해 추가하지 않는다. 팀이 실제로 제기했거나 출처에 명시된 질문만 정리한다.
8. Decision 문서를 생성하거나 대체 관계를 바꾼 경우 `30_DECISIONS/00 - Decision Index.md`를 갱신한다.
9. 마지막에 `$kb-quality-checks` 검사를 요청하거나 실행하고 결과를 요약한다.

## Raw metadata 권장 형식

```yaml
---
ingest_targets:
  - planning
  - decision
decision_candidates:
  - "MVP 범위 확정"
---
```

## 출력 위치

- Planning 문서: `10_PLANNING/`
- Planning Decision: `30_DECISIONS/Planning/`
- Technical Decision: `30_DECISIONS/Technical/`
- 미해결 기획 질문: `10_PLANNING/99 - Questions.md`
- 미해결 기술 질문: `20_TECHNICAL/99 - Questions.md`
- Raw 초안·노트·원본·요약: `40_RAW/`

별도 working 폴더는 사용하지 않는다. Raw는 비공식 기록이고, `main`의
Planning·Technical은 현재 기준이며, `main`의 Decision은 실제 결정 이력이다. 반영안의
검토 상태는 작업 브랜치와 GitHub PR로 표현한다.

## 링크 방향

- Planning과 Technical 문서는 관련 Decision만 참조한다.
- Decision 문서는 `source_refs`로 Raw만 참조한다.
- Raw 문서는 상위 계층 문서를 역링크하지 않는다.
- 즉, 계층 간 링크는 `10_PLANNING`·`20_TECHNICAL` → `30_DECISIONS` → `40_RAW` 단방향으로 유지한다.

## 금지 사항

- Raw 문서를 공식 지식처럼 취급하지 않는다.
- 실제 결정이 확인되기 전에는 Decision 문서를 만들지 않는다.
- 가능한 미결정 사항을 추측해 Questions를 채우지 않는다.
- 근거 없는 rationale, 수치, 일정, 역할 분담을 만들지 않는다.
- Planning 문서에 과도한 기술 구현 상세를 넣지 않는다.
- Technical 문서에 제품 narrative를 반복하지 않는다.
