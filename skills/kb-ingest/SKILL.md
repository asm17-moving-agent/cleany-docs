---
name: kb-ingest
description: 40_RAW의 회의록, 조사자료, 기획서 요약을 근거로 Planning/Decision 문서 초안을 생성하거나 갱신한다. Raw를 source of truth 근거로 보존하면서 YAML metadata, tags, source_refs, related_decisions를 연결할 때 사용한다.
compatibility: Codex repo-scoped skill, instruction-only workflow
tags:
  - skill
  - ingest
  - raw
  - planning
  - decision
---

# KB Ingest

이 skill은 `40_RAW`의 회의록, 조사 내용, 기획서 요약을 근거로 `10_PLANNING` 또는 `30_DECISIONS` 문서를 생성/갱신하는 Codex 문서 작성 워크플로우다.

## 목적

- Raw 기록을 최종 결정처럼 취급하지 않는다.
- Raw에서 나온 논의, 결정 후보, 미해결 질문을 YAML metadata와 문서 링크로 추적한다.
- Decision이 필요한 경우 `30_DECISIONS/Planning` 또는 `30_DECISIONS/Technical`에 `status: draft` 문서를 만든다.
- Planning 반영이 필요한 경우 `10_PLANNING` 문서의 `source_refs`, `related_decisions`, `tags`, `review_status`를 갱신한다.
- 별도 working 폴더 없이 각 문서의 YAML metadata로 draft/review/ingest 상태를 표현한다.

## 입력

- Raw 문서 경로: `40_RAW/.../*.md`
- 변환 목표: `planning`, `decision`, 또는 `planning+decision`
- 필요한 경우 대상 Planning 문서 경로
- 필요한 경우 Decision 제목과 decision_type: `planning` 또는 `technical`

## 워크플로우

1. Raw 문서를 끝까지 읽는다.
2. Raw frontmatter를 확인하고 필요한 경우 아래 metadata를 갱신한다.
   - `tags`
   - `ingest_status`
   - `ingest_targets`
   - `planning_targets`
   - `technical_targets`
   - `decision_candidates`
   - `related_decisions`
   - `related_planning`
   - `related_technical`
3. Raw 본문에서 다음 항목을 추출한다.
   - 핵심 논의
   - 결정 후보
   - Planning 반영 후보
   - Technical 반영 후보
   - 미해결 질문
   - Jira issue 후보
4. Decision 문서가 필요한지 판단한다. 아래 조건 중 2개 이상이면 Decision 초안을 만든다.
   - 프로젝트 방향에 영향을 준다.
   - 나중에 번복하면 비용이 크다.
   - Planning 또는 Technical 문서의 핵심 내용을 바꾼다.
   - Sprint 계획이나 Jira Epic/Story 구조에 영향을 준다.
   - 멘토나 리뷰어가 질문할 가능성이 높다.
   - 기술 리스크 또는 안전 리스크에 영향을 준다.
5. Decision 초안을 만들 때는 기본 상태를 유지한다.
   - `status: draft`
   - `review_status: needs-human-review`
   - `source_refs`에 Raw 문서 경로를 반드시 넣는다.
   - `reflected_in`은 실제 반영한 문서만 넣는다.
   - 사람 검토 전에는 `selected`로 바꾸지 않는다.
6. Planning 문서를 갱신할 때는 다음을 지킨다.
   - 기획서나 Raw에 없는 내용을 확정하지 않는다.
   - `source_refs`에 Raw 문서 경로를 추가한다.
   - 관련 Decision이 있으면 `related_decisions`에 추가한다.
   - 검토가 필요한 상태면 `review_status: needs-human-review`를 유지한다.
   - 불확실한 내용은 `검토 필요` 또는 `추가 확인 필요`로 표시한다.
7. 미해결 질문은 `10_PLANNING/08 - Questions.md`에 추가한다.
8. Decision 문서를 생성하거나 상태를 바꾼 경우 `30_DECISIONS/00 - Decision Index.md`를 갱신한다.
9. 마지막에 `$kb-quality-checks` 검사를 요청하거나 실행하고 결과를 요약한다.

## Raw metadata 권장 형식

```yaml
---
type: raw-meeting
review_status: needs-human-review
ingest_status: triaged
ingest_targets:
  - planning
  - decision
planning_targets:
  - "10_PLANNING/04 - Scope and Non-Goals.md"
technical_targets:
  -
decision_candidates:
  - "MVP 범위 확정"
related_decisions:
  -
related_planning:
  - "10_PLANNING/04 - Scope and Non-Goals.md"
related_technical:
  -
tags:
  - raw
  - meeting
  - ingest-source
---
```

## 출력 위치

- Planning 문서: `10_PLANNING/`
- Planning Decision: `30_DECISIONS/Planning/`
- Technical Decision: `30_DECISIONS/Technical/`
- 미해결 질문: `10_PLANNING/08 - Questions.md`
- Raw 원본/요약: `40_RAW/`

별도 working 폴더는 사용하지 않는다. 초안 여부는 `status`, `review_status`, `tags`, `ingest_status`로 표현한다.

## 금지 사항

- Raw 문서를 selected Decision처럼 취급하지 않는다.
- 사람 검토 없이 Decision을 `selected`로 바꾸지 않는다.
- 근거 없는 rationale, 수치, 일정, 역할 분담을 만들지 않는다.
- Planning 문서에 과도한 기술 구현 상세를 넣지 않는다.
- Technical 문서에 제품 narrative를 반복하지 않는다.
