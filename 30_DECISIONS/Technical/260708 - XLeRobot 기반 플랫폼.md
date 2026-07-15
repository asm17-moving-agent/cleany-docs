---
type: decision
decision_type: technical
status: selected
reviewers:
  - 박창수
tags:
  - decision
  - technical
  - robot-platform
  - cleany
date: 2026-07-08
impact: high
source_refs:
  - 40_RAW/20_Planning/기획서 원문 요약.md
  - 40_RAW/00_Inbox/지출신청서_관리.md
related_jira:
  -
supersedes:
superseded_by:
updated: 2026-07-15
---

# 260708 - XLeRobot 기반 플랫폼

## 1. 결정

XLeRobot 전체 조립체를 그대로 채택하지 않고, XLeRobot에서 유지하는 범위를 상부 모듈인 듀얼 매니퓰레이터와 깊이 카메라로 한정한다.

이동 베이스는 별도 selected Decision에 따라 4륜 Mecanum custom base를 그대로 사용한다. 상부 모듈과 이동 베이스를 연결하는 프레임은 이 결정의 범위에 포함하지 않는다. XLeRobot 기본 구성인 IKEA RÅSKOG와 알루미늄 프로파일을 별도 Technical Decision에서 비교하며, 해당 Decision이 selected 상태가 되기 전까지 프레임 구조를 확정하지 않는다.

## 2. 이유

- Raw 요약에는 모바일 매니퓰레이터로 XLeRobot과 RGB-D가 기재되어 있다.
- 전체 플랫폼의 제약을 수용하는 대신 필요한 조작·인식 구성인 듀얼 매니퓰레이터와 깊이 카메라를 유지한다.
- 이동 베이스는 표준 XLeRobot base와 분리해 이미 선택한 4륜 Mecanum 구성을 사용한다.
- 프레임은 매니퓰레이터 도달 범위, 작업 높이, 상부와 base 사이의 기구학 모델에 영향을 주므로 별도 결정으로 관리한다.

## 3. 대안

| 대안 | 선택 결과 또는 선택하지 않은 이유 |
|---|---|
| XLeRobot 전체 구성을 그대로 사용한다 | 플랫폼 제약이 있고, 별도 selected Decision인 4륜 Mecanum base와 일치하지 않아 선택하지 않았다. |
| XLeRobot 상부 모듈과 4륜 Mecanum base를 조합한다 | 듀얼 매니퓰레이터와 깊이 카메라를 유지하면서 이동 베이스를 분리하는 현재 선택안이다. |
| 상부 모듈까지 전부 새로 구성한다 | 현재 검토에서는 XLeRobot의 듀얼 매니퓰레이터와 깊이 카메라를 유지하기로 했으므로 선택하지 않았다. |

## 4. 가정

- 듀얼 매니퓰레이터와 깊이 카메라는 XLeRobot 상부 구성을 기준으로 유지한다.
- 매니퓰레이터와 깊이 카메라의 정확한 모델, 페이로드, 도달 범위, calibration과 interface는 추가 확인이 필요하다.
- 이동 베이스는 4륜 Mecanum 구성을 사용하며 상세 kinematics와 controller parameter는 추가 정의가 필요하다.
- 프레임 선택에 따라 상부 모듈의 높이와 `base_link` 기준 고정 transform이 달라질 수 있다.

## 5. 리스크

- LeRobot community의 자료와 도구가 SO-101 중심으로 최적화되어 있어, 듀얼 매니퓰레이터와 custom base·frame 조합에는 기존 예제, URDF와 controller 설정을 그대로 적용하지 못할 수 있다.
- custom frame과 mounting geometry는 base, 두 매니퓰레이터와 카메라 사이의 추가 기구학 모델링, 충돌 검토와 calibration 복잡도를 만든다.
- 페이로드와 도달 범위가 부족하면 쓰레기 수거, 정돈, 책상 닦기 같은 기능이 제한될 수 있다.
- 실제 플랫폼 조립과 calibration 시간이 Sprint 계획에 영향을 줄 수 있다.
- custom Mecanum base는 표준 XLeRobot assembly, URDF와 controller를 그대로 재사용하지 못할 수 있다.

## 6. 재검토 조건

- 듀얼 매니퓰레이터 또는 깊이 카메라가 요구 작업 범위와 인식 조건을 충족하지 못한다.
- 테스트 공간의 작업 높이와 거리가 매니퓰레이터 도달 범위를 넘는다.
- 프레임 Decision 결과로 상부 모듈의 배치나 기구학 구조를 변경해야 한다.
- SO-101 중심 community 자산을 현재 구성에 적용하기 어렵다는 검증 결과가 나온다.
- 4륜 Mecanum base의 payload, traction, odometry 또는 안전 검증이 목표를 만족하지 못한다.

## 7. 출처

- [[40_RAW/20_Planning/기획서 원문 요약|기획서 원문 요약]]
- [[40_RAW/00_Inbox/지출신청서_관리|지출신청서 관리]]
- [[30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스|4륜 메카넘 베이스]]
- [[30_DECISIONS/Technical/260715 - 로봇 프레임 구조|로봇 프레임 구조]]
