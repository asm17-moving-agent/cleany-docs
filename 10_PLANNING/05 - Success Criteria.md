---
source_refs:
  - "[기획서]"
related_decisions:
  - "30_DECISIONS/Planning/260708 - MVP 기능 범위.md"
---

# 성공 기준(Success Criteria)

## 요약

현재 성공 기준은 통제된 데모 환경에서의 단계별 통과 여부다. 물체별 성공률,
반복 횟수와 같은 수치 목표는 아직 사용하지 않는다.

## 1. Rule-based 통합 검증 단계

다음 전체 흐름이 규칙 기반 Planner와 검증 가능한 실행 계층으로 연결되면 통과한다.

- Dashboard에서 개별 좌석 미션을 요청할 수 있다.
- 로봇이 사전 제작 지도를 사용해 대상 좌석에 도착한다.
- 작업 전 장면과 여러 물체를 관찰한다.
- 규칙 기반 Planner가 허용된 작업 순서를 만든다.
- Manipulation Skill 실행 결과가 Mission Manager로 반환된다.
- 작업 후 장면을 다시 관찰하고 대기 위치로 복귀한다.
- Dashboard에서 전후 결과와 미션 상태를 확인할 수 있다.

이 단계는 목표 MVP의 축소판이 아니라 AI Planner를 연결하기 전 E2E 경계를 검증하는
단계다.

## 2. 목표 MVP

Rule-based 통합 검증 흐름을 유지하면서 다음 조건을 추가로 만족하면 통과한다.

- AI가 여러 물체가 있는 책상 장면을 해석하고 처리 순서를 제안한다.
- 제안은 허용된 Robot Capability와 로컬 검증을 통과한 뒤에만 실행된다.
- VLA 기반 Manipulation Skill을 포함한 물리 실행 결과를 관찰해 다음 행동이나
  완료 여부를 판단한다.
- 실패하거나 처리할 수 없는 물체를 성공으로 보고하지 않는다.

ER 2는 현재 목표 AI 경로지만, 클라우드 API의 지연·정확도·실패·비용 검증 결과에
따라 adapter 선택은 바뀔 수 있다.

## 3. 승인된 축소 범위

실제 로봇에서 전체 흐름을 완성하기 어려운 경우 팀이 별도로 승인한 축소 범위만
최종 데모로 인정한다. 축소되는 단계, 시뮬레이션 또는 영상으로 대체하는 단계와
미완료 항목을 결과에 명시해야 한다.

## 공통 시연 조건

- 사람이 없는 통제된 구역
- 작업 구역 밖 감독자와 비상 정지 수단
- 사전 제작 지도와 고정된 좌석 위치
- 작업 전후 관찰 보존
- 여러 물체가 놓인 책상 장면

## 관련 문서

- [[10_PLANNING/02 - Target Scenario|Target Scenario]]
- [[20_TECHNICAL/03 - Task Planning and Robot Capabilities|Task Planning and Robot Capabilities]]
- [[20_TECHNICAL/13 - Verification and Simulation Strategy|Verification and Simulation Strategy]]
