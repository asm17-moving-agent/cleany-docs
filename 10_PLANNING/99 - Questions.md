---
type: planning
status: draft
reviewers:
  -
tags:
  - planning
  - questions
  - draft
  - cleany
source_refs:
  - "[기획서]"
related_decisions:
  - "30_DECISIONS/Planning/260708 - 1차 타깃 무인 스터디카페.md"
  - "30_DECISIONS/Planning/260708 - MVP 기능 범위.md"
related_jira:
  -
updated: 2026-07-12
---

# 기획 미해결 질문(Planning Questions)

## 1. 요약

이 문서는 사용자, 가치, 제품 범위, 시나리오, 성공 기준, 프로젝트 운영처럼 기획 판단이 필요한 미해결 질문을 모아두는 목록이다.

## 2. 질문 분류 기준

- 제품이 누구의 어떤 문제를 어디까지 해결할지는 이 문서에서 관리한다.
- 시스템 구조, 인터페이스, 하드웨어, 런타임, 안전 구현처럼 기술 판단이 필요한 질문은 [[20_TECHNICAL/99 - Questions|Technical Questions]]에서 관리한다.
- 기획과 기술에 걸친 주제는 제품 선택과 기술 구현 경계를 나눠 각각 한 번만 기록한다.

## 3. 관리 규칙

- 질문에 답할 근거가 없으면 내용을 임의로 확정하지 않는다.
- 사실이나 외부 근거 확인이 필요하면 `추가 확인 필요`, 기준이나 정책 정의가 필요하면 `추가 정의 필요`, 후보 선택이 필요하면 `검토 필요`로 표시한다.
- 기존 문서에 우선순위가 없던 질문은 `미정`으로 유지한다.
- 질문이 해결되면 관련 Planning 또는 Decision 문서에 반영한 뒤 상태를 갱신한다.

## 4. 질문 목록

### 4.1 타깃, 사용자, 시장

| 질문 | 배경 | 관련 문서 | 우선순위 | 상태 |
|---|---|---|---|---|
| 무인 스터디카페를 1차 타깃으로 확정할 것인가? | 기획서에는 1차 타깃으로 설정했다고 적혀 있으나 팀 합의 상태를 확인해야 한다. | [Project Brief](<00 - Project Brief.md>), [Problem and Users](<01 - Problem and Users.md>) | 높음 | 검토 필요 |
| 공간대여 시설의 구체 유형은 무엇인가? | 공간 구조에 따라 정리 대상과 안전 기준이 달라진다. | [Project Brief](<00 - Project Brief.md>), [Problem and Users](<01 - Problem and Users.md>) | 중간 | 추가 확인 필요 |
| 무인 점포 유형별로 필요한 정리 작업은 어떻게 다른가? | 초기 타깃 이후의 적용 범위와 기능 우선순위를 판단하려면 유형별 차이를 알아야 한다. | [Problem and Users](<01 - Problem and Users.md>) | 미정 | 추가 확인 필요 |
| 기획서의 시장 수치 출처는 무엇인가? | 시장 규모, 국내 무인점포 수, 서울시 업종별 수치가 기재되어 있다. | [Project Brief](<00 - Project Brief.md>), [Problem and Users](<01 - Problem and Users.md>) | 중간 | 추가 확인 필요 |
| 실제 운영자 인터뷰 또는 현장 검증 계획이 있는가? | 사용자 가치와 운영 문제를 실제 현장에서 검증해야 한다. | [Problem and Users](<01 - Problem and Users.md>) | 중간 | 추가 확인 필요 |
| 운영자가 가장 중요하게 보는 문제는 청결, 정돈, 보안, 비용 중 무엇인가? | 기능과 성공 기준의 우선순위를 정하는 데 필요하다. | [Problem and Users](<01 - Problem and Users.md>) | 중간 | 검토 필요 |

### 4.2 MVP 범위와 시나리오

| 질문 | 배경 | 관련 문서 | 우선순위 | 상태 |
|---|---|---|---|---|
| 1차 MVP의 물체 종류·개수와 물체별 집기·수거함 투입 조건은 무엇인가? | 7/10 회의에서 소수의 사전 정의 물체를 인식·분류·집기하는 범위를 우선 논의했다. | [Project Brief](<00 - Project Brief.md>), [Target Scenario](<02 - Target Scenario.md>), [Scope and Non-Goals](<04 - Scope and Non-Goals.md>) | 높음 | 추가 정의 필요 |
| 분실물 후보와 저신뢰 물체를 사용자에게 어떻게 기록·표시·알림할 것인가? | 1차 MVP에서는 해당 물체를 건드리지 않는 방향이지만 결과 표시 방식은 정해지지 않았다. | [Target Scenario](<02 - Target Scenario.md>), [Scope and Non-Goals](<04 - Scope and Non-Goals.md>) | 높음 | 추가 정의 필요 |
| 웹 대시보드의 최소 호출·상태 확인 기능과 작업 요청 입력은 무엇인가? | 운영자 호출 UI 후보가 논의됐지만 대상 구역 선택 외 필수 입력과 상태 범위가 정해지지 않았다. | [Project Brief](<00 - Project Brief.md>), [Target Scenario](<02 - Target Scenario.md>), [Scope and Non-Goals](<04 - Scope and Non-Goals.md>) | 중간 | 검토 필요 |
| 자율주행·지도 생성·대시보드는 현장 시연과 사전 영상 보완을 어떤 기준으로 나눌 것인가? | 공간 배치 변경, 지도 생성 시간, 현장 안정성이 시연 리스크로 언급됐다. | [Project Brief](<00 - Project Brief.md>), [Target Scenario](<02 - Target Scenario.md>), [Scope and Non-Goals](<04 - Scope and Non-Goals.md>), [Success Criteria](<05 - Success Criteria.md>) | 높음 | 추가 정의 필요 |
| 작업 실패나 저신뢰 결과가 발생하면 사용자에게 보이는 흐름을 대기, 재시도, 중단, 기록, 알림 중 어떻게 구성할 것인가? | 기술 실패 처리와 별개로 시연 및 운영자 경험의 기본 흐름이 필요하다. | [Target Scenario](<02 - Target Scenario.md>), [Success Criteria](<05 - Success Criteria.md>) | 미정 | 추가 정의 필요 |

### 4.3 성공 기준과 검증

| 질문 | 배경 | 관련 문서 | 우선순위 | 상태 |
|---|---|---|---|---|
| 물체 인식·분류·집기·수거와 주행 성공을 어떤 지표, 목표값, 반복 횟수로 판정할 것인가? | MVP 성공 여부를 판단할 정량 기준이 아직 정의되지 않았다. | [Project Brief](<00 - Project Brief.md>), [Success Criteria](<05 - Success Criteria.md>) | 높음 | 추가 정의 필요 |
| 실제 공간 테스트와 시뮬레이션 테스트의 비중은 어떻게 둘 것인가? | 데모 신뢰도와 개발 비용을 함께 고려한 검증 계획이 필요하다. | [Success Criteria](<05 - Success Criteria.md>) | 미정 | 검토 필요 |
| 실제 테스트 공간은 어디인가? | 시뮬레이션 결과를 실환경 검증으로 연결하려면 대상 공간을 정해야 한다. | [Success Criteria](<05 - Success Criteria.md>) | 중간 | 추가 확인 필요 |

### 4.4 역할과 운영

| 질문 | 배경 | 관련 문서 | 우선순위 | 상태 |
|---|---|---|---|---|
| 팀원별 역할은 어떻게 나눌 것인가? | 기획서 역할 표에 placeholder와 빈 칸이 있다. | [Project Brief](<00 - Project Brief.md>) | 높음 | 추가 확인 필요 |
| 멘토별 역할과 기대 도움은 무엇인가? | 멘토 구성 및 역할 표에 placeholder와 빈 칸이 있다. | [Project Brief](<00 - Project Brief.md>) | 중간 | 추가 확인 필요 |
| Sprint 운영 방식과 Jira Epic/Story 구조는 어떻게 잡을 것인가? | Jira가 작업 상태의 source of truth다. | [Project Brief](<00 - Project Brief.md>) | 중간 | 검토 필요 |
| 추진 일정의 월별 배치는 어떻게 확정할 것인가? | 기획서 일정표에 항목은 있으나 월별 체크가 비어 있다. | [Project Brief](<00 - Project Brief.md>) | 높음 | 추가 확인 필요 |

## 5. 관련 결정

- 현재 selected Decision 없음.
- 아래 draft Decision은 검토용 초안이며 아직 selected Decision이 아니다.
  - [[30_DECISIONS/Planning/260708 - 1차 타깃 무인 스터디카페|1차 타깃 무인 스터디카페]]
  - [[30_DECISIONS/Planning/260708 - MVP 기능 범위|MVP 기능 범위]]
