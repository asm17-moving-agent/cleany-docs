---
type: decision-index
status: draft
review_status: needs-human-review
tags:
  - decision
  - index
  - draft
  - cleany
updated: 2026-07-08
---

# 결정 인덱스(Decision Index)

기획서 기반으로 아직 `selected` Decision을 임의 생성하지 않는다. 현재 문서는 Decision 후보를 추적하기 위한 인덱스다.

## Planning Decisions

| 날짜 | 결정 | 상태 | 반영 문서 |
|---|---|---|---|
|  |  |  |  |

## Technical Decisions

| 날짜 | 결정 | 상태 | 반영 문서 |
|---|---|---|---|
|  |  |  |  |

## Deprecated / Superseded Decisions

| 날짜 | 결정 | 대체 문서 | 사유 |
|---|---|---|---|
|  |  |  |  |

## Decision 문서 생성 기준

Decision 문서는 아래 조건 중 2개 이상을 만족할 때만 생성한다.

- 프로젝트 방향에 영향을 준다.
- 나중에 번복하면 비용이 크다.
- Planning 또는 Technical 문서의 핵심 내용을 바꾼다.
- Sprint 계획이나 Jira Epic/Story 구조에 영향을 준다.
- 멘토나 리뷰어가 질문할 가능성이 높다.
- 기술 리스크 또는 안전 리스크에 영향을 준다.

## 초기 Decision 후보

| 후보 | 유형 | 이유 | 상태 |
|---|---|---|---|
| 1차 타깃을 무인 스터디카페로 확정할지 | planning | 기능 범위와 데모 공간에 영향 | 후보 |
| MVP 기능 범위를 어디까지 둘지 | planning | Sprint, 성공 기준, 기술 범위에 영향 | 후보 |
| XLeRobot을 기준 플랫폼으로 확정할지 | technical | 하드웨어, 센서, 조작 범위에 영향 | 후보 |
| Jetson AGX Orin 64GB를 메인 컴퓨팅으로 확정할지 | technical | 성능, 비용, 개발환경에 영향 | 후보 |
| Rule-based VLA의 3 Layer 구조를 어떻게 정의할지 | technical | 판단 구조와 평가 방식에 영향 | 후보 |
| 안전 기준과 실패 처리 정책을 어떻게 둘지 | technical | 데모 안정성과 상용화 리스크에 영향 | 후보 |

## 운영 규칙

- 후보는 확정 결정이 아니다.
- `selected` 상태가 된 Decision만 공식 결정으로 취급한다.
- Decision 문서는 관련 Raw 출처와 반영 문서를 반드시 연결한다.
- Raw에서 Decision 초안을 만들 때는 `$kb-ingest` skill prompt를 사용한다.
- Decision 초안은 `status: draft`, `review_status: needs-human-review`, `tags`로 검토 상태를 표시한다.
