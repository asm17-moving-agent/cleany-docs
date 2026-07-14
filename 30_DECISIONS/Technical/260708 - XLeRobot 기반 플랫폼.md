---
type: decision
decision_type: technical
status: draft
reviewers:
  -
tags:
  - decision
  - draft
  - technical
  - robot-platform
  - cleany
date: 2026-07-08
impact: high
source_refs:
  - "40_RAW/20_Planning/기획서 원문 요약.md"
  - "40_RAW/00_Inbox/지출신청서_관리.md"
related_jira:
  -
supersedes:
superseded_by:
updated: 2026-07-14
---

# 260708 - XLeRobot 기반 플랫폼

## 1. 결정

XLeRobot을 끌리니의 기준 모바일 매니퓰레이터 플랫폼으로 확정할지 검토하는 Technical Decision 초안이다. 이동 베이스는 별도 selected Decision에서 4륜 Mecanum custom base로 구체화했다. 이 문서가 다루는 XLeRobot 전체 플랫폼 선택은 사람 검토 전이므로 아직 확정 결정이 아니다.

## 2. 이유

- Raw 요약에는 모바일 매니퓰레이터로 XLeRobot, RGB-D, 2D LiDAR, IMU, 매니퓰레이터가 기재되어 있다.
- 플랫폼 선택은 센서 구성, 조작 가능 범위, 실내 이동, 파지, 정돈, 안전 기준에 영향을 준다.
- Raw BOM은 표준 XLeRobot의 3륜 base가 아니라 DC geared motor 4개와 4륜 Mecanum wheel을 포함한다.
- 플랫폼이 바뀌면 기술 문서와 평가 지표를 다시 정리해야 한다.

## 3. 대안

| 대안 | 선택하지 않은 이유 |
|---|---|
| XLeRobot을 기준 플랫폼으로 둔다 | Raw에 명시되어 있으나 정확한 사양, 페이로드, 구동 범위 확인이 필요하다. |
| 다른 모바일 매니퓰레이터를 검토한다 | Raw 근거에는 다른 플랫폼 후보가 구체적으로 제시되어 있지 않다. |
| 시뮬레이션 전용 플랫폼으로 먼저 제한한다 | 실제 XLeRobot 적용 목표와 괴리가 생길 수 있다. |

## 4. 가정

- XLeRobot이 무인 스터디카페 환경에서 주행과 기본 조작을 수행할 수 있다고 가정한다.
- 센서와 매니퓰레이터 상세 사양은 아직 추가 확인 필요다.
- 이동 베이스는 4륜 Mecanum 구성을 사용하며 상세 kinematics와 controller parameter는 추가 정의가 필요하다.

## 5. 리스크

- 페이로드와 작업 범위가 부족하면 쓰레기 수거, 정돈, 책상 닦기 같은 기능이 제한될 수 있다.
- 실제 플랫폼 조립과 캘리브레이션 시간이 Sprint 계획에 영향을 줄 수 있다.
- 센서 구성이 안전 기준을 만족하지 못할 수 있다.
- custom Mecanum base는 표준 XLeRobot assembly, URDF와 controller를 그대로 재사용하지 못할 수 있다.

## 6. 재검토 조건

- XLeRobot의 센서, 매니퓰레이터, 페이로드, 구동 범위가 확인된다.
- 테스트 공간에서 요구되는 동선과 작업 높이가 플랫폼 한계를 넘는다.
- 다른 플랫폼이 일정, 비용, 안전 측면에서 더 적합하다는 근거가 나온다.
- 4륜 Mecanum base의 payload, traction, odometry 또는 안전 검증이 목표를 만족하지 못한다.

## 7. 출처

- [[40_RAW/20_Planning/기획서 원문 요약|기획서 원문 요약]]
- [[40_RAW/00_Inbox/지출신청서_관리|지출신청서 관리]]
