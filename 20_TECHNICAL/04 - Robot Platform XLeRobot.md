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
  - "40_RAW/00_Inbox/지출신청서_관리.md"
related_decisions:
  - "30_DECISIONS/Technical/260708 - XLeRobot 기반 플랫폼.md"
  - "30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스.md"
  - "30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB.md"
  - "30_DECISIONS/Technical/260715 - 로봇 프레임 구조.md"
related_jira:
  -
updated: 2026-07-15
---

# XLeRobot 로봇 플랫폼

## 1. 요약

XLeRobot은 끌리니의 기반 모바일 매니퓰레이터로 기획서에 명시되어 있다. selected Decision에 따라 XLeRobot에서 유지하는 범위는 상부 모듈인 듀얼 매니퓰레이터와 깊이 카메라다. 이동 베이스는 표준 XLeRobot 구성을 그대로 사용하지 않고 4륜 Mecanum custom base를 사용한다. 상부와 base를 연결하는 frame은 RÅSKOG와 알루미늄 프로파일을 별도 Decision에서 비교 중이다.

## 2. 기획 맥락

끌리니는 단순 청소 로봇이 아니라 물체를 보고 판단하고 조작해야 하는 관리 로봇이다. 따라서 이동 기반과 로봇 팔을 함께 갖춘 모바일 매니퓰레이터가 필요하다.

## 3. 기술 개념

### 3.1 플랫폼 역할

- 작업 구역까지 이동한다.
- 4륜 Mecanum base로 전후·좌우 병진과 제자리 회전을 수행한다.
- 책상, 바닥, 의자 주변을 관찰한다.
- 쓰레기 후보를 집어 지정 수거함으로 이동한다.
- 흐트러진 의자나 소형 집기를 밀기, 정렬, 이동 동작으로 복구한다.
- 책상 닦기, 소등, 문단속 등은 기획서에 포함되어 있으나 실제 조작 방식은 검토 필요다.

### 3.2 하드웨어 구성 초안

| 구성 | 역할 | 상태 |
|---|---|---|
| 4륜 Mecanum base | 4개 독립 구동 wheel을 이용한 실내 holonomic 이동과 작업 위치 접근 | selected, 상세 설계 검토 필요 |
| Base motor/driver | encoder가 있는 DC geared motor 4개와 dual motor driver 2개 | Raw BOM 기반 |
| Base MCU | encoder feedback 수집과 MDD20A PWM/DIR 출력 | 멘토 지원 MCU 사용 확정, 상세 사양 확인 필요 |
| Frame | XLeRobot 상부 모듈과 4륜 Mecanum base 연결 | RÅSKOG와 알루미늄 프로파일 비교 중, draft Decision |
| 듀얼 매니퓰레이터 | 집기, 이동, 정렬, 닦기 등 조작 | XLeRobot 유지 범위, 정확한 모델과 사양 확인 필요 |
| 깊이 카메라 | 물체 후보 탐지와 깊이 정보 제공 | XLeRobot 유지 범위, 정확한 모델과 사양 확인 필요 |
| 2D LiDAR | 실내 지도, 장애물 감지, 주행 보조 | 기획서 기반 |
| IMU | 자세/움직임 추정 보조 | 기획서 기반 |
| Jetson Orin NX 16GB | 온디바이스 추론 및 로봇 런타임 | selected Decision, 기획서의 AGX Orin 64GB 대체 |

## 4. 인터페이스 / 경계

| 구성요소 | 책임 | 경계 |
|---|---|---|
| Mecanum Base Backend | `linear.x`, `linear.y`, `angular.z` 명령을 wheel target으로 변환하고 MCU feedback으로 odometry를 제공 | 전역 경로 계획은 Nav2에 의존 |
| Mentor-supported MCU | 4개 motor encoder 수집, wheel velocity 제어와 MDD20A PWM/DIR 출력 | 상위 mission과 navigation 판단을 수행하지 않음 |
| Dual Manipulators | 물체 집기, 밀기, 정렬, 닦기 | 물체 의미 판단을 직접 수행하지 않음 |
| Sensor Suite | RGB-D, LiDAR, IMU 데이터 제공 | 최종 행동 결정은 VLA/Rule 계층에 위임 |
| ROS 2 Drivers | 하드웨어 제어 인터페이스 제공 | 기획서에는 드라이버 세부 정보 없음 |

## 5. 가정

- XLeRobot에서 유지하는 범위는 듀얼 매니퓰레이터와 깊이 카메라다.
- 이동 베이스는 4륜 Mecanum kinematics를 사용하며 `cmd_vel.linear.y`를 좌우 병진 속도로 지원한다.
- encoder feedback과 MDD20A 출력은 멘토 지원 MCU가 담당한다.
- wheel radius, wheelbase, track width, motor direction, MCU 모델과 Jetson 통신 계약은 추가 정의가 필요하다.
- 듀얼 매니퓰레이터는 쓰레기 후보와 소형 물체를 다룰 수 있다고 가정하며 실제 도달 범위와 payload는 추가 확인이 필요하다.
- 센서는 인식과 주행에 필요한 데이터를 제공한다.
- frame 후보별 상부 높이와 base-to-arm transform은 아직 확정되지 않았다.

## 6. 리스크

- 실제 XLeRobot 사양이 기획 기능을 모두 지원하지 못할 수 있다.
- custom Mecanum base는 표준 XLeRobot base의 assembly, URDF와 controller를 그대로 재사용하지 못할 수 있다.
- LeRobot community 자료가 SO-101 중심으로 최적화되어 있어 듀얼 매니퓰레이터와 custom frame·base 구성에 그대로 적용되지 않을 수 있다.
- frame 변경에 따른 base-to-arm transform, 양팔 충돌 영역과 calibration은 추가 기구학 복잡도를 만든다.
- 멘토 지원 MCU의 적용 경로는 확인됐지만, 상세 encoder I/O, 전기 규격, 제어 주기 또는 Jetson 통신 계약이 base 요구사항과 맞지 않을 수 있다.
- Mecanum wheel slip과 encoder 처리 오차가 odometry 및 Nav2 localization 성능을 낮출 수 있다. wheel odometry와 IMU 융합 및 localization 보정 방식은 추가 정의가 필요하다.
- 로봇 팔의 도달 범위, 페이로드, 그리퍼 형태가 쓰레기 수거와 책상 닦기에 충분하지 않을 수 있다.
- 실내 좁은 공간에서 회전 반경과 장애물 회피 문제가 발생할 수 있다.

## 7. 관련 결정

- [[30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스|4륜 메카넘 베이스]]는 `selected` Decision이다.
- [[30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB|Jetson Orin NX 16GB]]는 메인 엣지 컴퓨팅 장치를 채택한 `selected` Decision이다.
- [[30_DECISIONS/Technical/260708 - XLeRobot 기반 플랫폼|XLeRobot 기반 플랫폼]]은 XLeRobot 유지 범위를 듀얼 매니퓰레이터와 깊이 카메라로 한정한 `selected` Decision이다.
- [[30_DECISIONS/Technical/260715 - 로봇 프레임 구조|로봇 프레임 구조]]는 RÅSKOG와 알루미늄 프로파일을 비교하는 `draft` Decision이다.
