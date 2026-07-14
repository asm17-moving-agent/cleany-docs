---
type: technical
status: draft
reviewers:
  -
tags:
  - technical
  - draft
  - cleany
source_refs:
  - "[기획서]"
related_decisions:
  - "30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스.md"
related_jira:
  -
updated: 2026-07-14
---

# 내비게이션과 매핑(Navigation and Mapping)

## 1. 요약

끌리니는 selected Decision에 따라 4륜 Mecanum holonomic base를 사용한다. 사전 지도 또는 초기 세팅 결과를 바탕으로 작업 대상 구역까지 이동하고 복귀하는 구조를 검토한다. 1차 시연에서 지도 생성과 자율주행을 현장 실물 시연할지는 공간 변화와 소요 시간을 검증한 뒤 결정한다.

## 2. 기획 맥락

이용 종료 후 로봇이 지정 공간으로 이동해야 정리 작업을 시작할 수 있다. 따라서 주행 안정성은 쓰레기 수거와 공간 정돈보다 먼저 보장되어야 하는 기반 기능이다.

## 3. 기술 개념

### 3.1 지도 생성

- SLAM으로 실내 지도를 생성한다.
- 무인 스터디카페/공간대여 시설의 방, 책상, 통로, 대기 위치, 수거함 위치를 지도 또는 작업 구역으로 표현해야 한다.
- 초기 세팅에서 사용자가 지도 위에 방, 책상, 작업 구역을 지정하는 UI 후보가 논의됐다.
- 지도 갱신 방식, 사용자의 세팅 부담, 운영 중 변경 대응은 검토 필요다.

### 3.2 자율주행

- Nav2 기반으로 작업 대상 구역까지 이동하는 방향을 검토한다.
- Mecanum base의 전후·좌우 병진과 제자리 회전을 활용하되 Nav2 controller와 실제 base backend가 같은 `cmd_vel` 의미를 사용해야 한다.
- encoder 기반 wheel odometry와 IMU를 융합하고 SLAM/localization으로 누적 오차를 보정하는 방향을 검토한다. 정확한 filter 구성과 검증 기준은 추가 정의가 필요하다.
- 이동 중 장애물을 회피한다.
- 작업 완료 후 대기 위치로 복귀한다.
- 시연 공간의 책상·칸막이 배치가 사전 지도와 달라질 수 있으므로, 현장 시연이 불안정하면 영상으로 전체 주행 흐름을 보완한다.

### 3.3 작업 위치 접근

- 로봇은 물체를 조작할 수 있는 위치까지 접근해야 한다.
- 매니퓰레이터 도달 범위와 베이스 위치 정밀도가 함께 고려되어야 한다.

## 4. 인터페이스 / 경계

| 구성요소 | 책임 | 경계 |
|---|---|---|
| SLAM | 지도 생성과 위치 추정 기반 제공 | 물체 정리 행동을 결정하지 않음 |
| Nav2 | 경로 계획, 추종, 장애물 회피 | 조작 가능한 최종 자세 보장은 별도 검토 |
| Mecanum Base Backend | `cmd_vel`을 4개 wheel target으로 변환하고 MCU feedback으로 wheel odometry 제공 | 전역 경로와 작업 목표를 결정하지 않음 |
| Mentor-supported MCU | encoder feedback 수집과 MDD20A PWM/DIR 출력 | 지도, 경로와 작업 목표를 결정하지 않음 |
| Sensor Suite | LiDAR, RGB-D, IMU 입력 제공 | 센서 캘리브레이션 세부는 미정 |
| Task Planner | 목적지와 작업 구역 지정 | 저수준 주행 제어를 직접 수행하지 않음 |
| Safety Layer | 장애물 및 위험 조건 감지 | 구체 기준 추가 정의 필요 |

## 5. 가정

- 대상 공간은 실내이며 사전 지도화 또는 초기 세팅이 가능하다.
- 로봇이 이동할 수 있는 통로 폭과 작업 공간이 확보된다.
- 4륜 Mecanum base는 `linear.x`, `linear.y`, `angular.z`를 지원한다.
- encoder feedback과 motor output은 멘토 지원 MCU가 담당한다.
- 작업 구역과 대기 위치는 사전 정의하거나 대시보드에서 지정할 수 있다.

## 6. 리스크

- 좁은 통로, 의자 위치 변화, 사람 또는 임시 장애물로 주행 실패가 발생할 수 있다.
- 작업 대상에 접근했지만 매니퓰레이터가 닿지 않는 위치일 수 있다.
- 지도와 실제 공간이 달라지는 경우 작업 안정성이 낮아질 수 있다.
- Mecanum wheel slip과 wheel geometry 오차로 odometry drift가 커질 수 있으며, IMU 융합만으로 평면 병진 slip이 제거되지는 않는다.
- 지도 생성 또는 3D 기반 평면도 변환이 시연 시간 안에 완료되지 않을 수 있다.

## 7. 관련 결정

- [[30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스|4륜 메카넘 베이스]]는 `selected` Decision이다.
