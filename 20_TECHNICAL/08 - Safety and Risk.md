# 안전과 리스크(Safety and Risk)

## 요약

현재 확정된 안전 범위는 사람이 없는 통제 구역에서 감독자가 작업 구역 밖에서
비상 정지할 수 있는 데모다. 사람 감지 시 거리, 정지 및 재개 정책과 실제 힘, 속도 제한은
아직 정하지 않았다.

## Planner보다 우선하는 원칙

- ER 2와 VLA 출력은 물리적 안전의 유일한 근거가 아니다.
- 허용되지 않은 Capability와 argument는 실행하지 않는다.
- workspace, joint, velocity, force, collision과 timeout 제한은 로컬에서 강제한다.
- 실행 중 안전 조건이 깨지면 Planner 응답을 기다리지 않고 중단할 수 있어야 한다.
- 불확실한 분실물 정책을 AI가 임의로 보완해 실행하지 않는다.
- 안전 기능의 실패를 일반 task 실패와 구분해 보고한다.

## Stop 계층

| 계층 | 목적 | 의존하면 안 되는 것 |
|---|---|---|
| Mission cancel | 사용자가 미션 또는 action을 취소 | ER 2의 다음 응답 |
| Safe stop | timeout, fault, 로컬 위험에서 동작을 안전하게 정지 | cloud 연결 |
| Emergency stop | 즉시 위험에서 구동을 최우선 차단 | 일반 ROS node 정상 동작 |

stop은 Task Planner가 선택하는 일반 Manipulation Skill이 아니다. ER 2에 정지 요청
tool을 제공하더라도 실제 선점 경로는 별도로 유지한다.

## Supervisor와 독립 안전 계층

System Supervisor는 시스템 가용성, Fault, 기능 제한과 실행 허가를 관리하고 필요한
경우 Mission 중단을 요청한다. 실제 구동 정지와 하드웨어 보호는 Supervisor와
독립된 하위 제어기 및 안전 계층이 보장해야 한다.

- Mission 중단 요청 수락과 실제 중단 완료를 구분한다. 실패나 시간 초과는 운영
  잠금으로 확대하며 보고 저장 성공 여부가 정지 경로를 막아서는 안 된다.
- ESP32 통신 두절 시 ROS 정지 명령이 도착한다고 가정하지 않는다. 하위 watchdog과
  보호 기능 및 실제 정지 증거가 필요하다.
- Supervisor 종료 시 허가는 로컬에서 만료되어야 하며 재시작하면 이전 허가를
  무효화한다. 이것만으로 임의의 motor 명령원이 물리적으로 차단되는 것은 아니다.
- 기능 가용성과 특정 동작의 안전성은 다르다. 팔 통신 정상만으로 이동에 안전한 팔
  상태를 추정하거나 camera frame만으로 Perception 준비를 선언하지 않는다.
- 운영 잠금 해제에는 Fault 원인 해소와 fresh 안전 재검증이 필요하다. E-stop은
  software Service만으로 해제하지 않으며 물리 해제와 보호 계층 상태를 확인한다.

`feat/system-supervisor`의 `c63fadb`에는 위 상태 및 허가 계약이 구현되어 있지만
실물 독립 안전 상태 adapter와 Arm 정지 증거는 추가 구현 및 검증이 필요하다.
기본 설정은 해당 증거 없이 자동 운영을 허용하지 않는다. synthetic ROS graph의
정지 및 복구 응답은 실물 모터 정지나 E-stop 회로 검증으로 해석하지 않는다.

## 예상 밖 장면 변화

책상 작업은 외부 개입이 없는 준정적 환경을 전제로 하지만, 로봇 행동으로 물체가
낙하하거나 전도되거나 예상하지 않은 접촉이 발생할 수 있다.

- 실행 중 즉시 정지와 물리적 제한은 VLM 응답을 기다리지 않는다.
- Capability, controller, hardware safety가 이상을 감지하면 활성 동작을 종료하거나
  차단한다.
- Mission Manager는 실패 결과를 기록하고 최신 장면을 다시 요청한다.
- VLM은 정지 또는 행동 종료 뒤 새 장면으로 복구 행동, 보류, 미션 종료를 제안한다.
- 기존 object pose와 proposal은 장면 변화 뒤 재사용하지 않는다.

물체의 낙하 또는 전도는 Perception의 영상 판정으로 감지하고, 활성 동작을 즉시
중단한 뒤 최신 장면을 다시 관찰하는 방향으로 정한다. 영상 판정 기준과 안전 정지의
실제 검증은 구현 및 시험에서 확인한다.

## 현재 데모 조건

- 사람 없는 통제된 작업 구역
- 작업 구역 밖 감독자
- 감독자가 접근 가능한 비상 정지 수단
- 사전에 정한 지도, 좌석, 물체 배치
- base 이동과 arm 작업 경계가 관찰 가능한 상태

사람이 접근했을 때 자동 정지, 거리, 재개 행동은 이 조건에서 추론하지 않고 열린
질문으로 남긴다.

## 주요 리스크

| 영역 | 실패 예 | 필요한 방어 경계 |
|---|---|---|
| Navigation | localization 오류, 장애물 충돌, 부적절한 도착 자세 | Nav2, base limit, cancel, safe stop |
| Perception | 물체 누락, stale mask, 잘못된 3D 위치 | Scene validation, timestamp, 재관찰 |
| Task Planning | 환각, 잘못된 순서, tool argument | Mission state, allowlist, schema 검증 |
| Manipulation | 파지 실패, 물체 낙하, 전도, 손상, 충돌 | 실행 감시, workspace, collision, force, timeout, 재관찰 |
| Cloud | 지연, API 오류, 연결 손실 | 새 행동 차단, 로컬 안전 유지 |
| Hardware | 과전류, 전원 저하, node, MCU 장애 | 전원 보호, watchdog, e-stop |
| 운영 | 분실물 오처리, 불완전한 결과 표시 | 미정 정책 차단, 명시적 보고 |

## 관련 문서

- [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>)
- [Robot ROS Contract](<10 - Robot ROS Contract.md>)
- [Technical Questions](<99 - Questions.md>)
- [System Supervisor](<14 - System Supervisor.md>)

## 출처

- [261016 - System Supervisor 설계 지시](<../40_RAW/261016 - System Supervisor 설계 지시.md>)
- [Supervisor 안전 및 검증 범위 at c63fadb](https://github.com/asm17-moving-agent/cleany/blob/c63fadb467afac08cc62a3cfd0a5af7c59b6e8b7/ros2_ws/src/cleany_system_supervisor/README.md)

- [기획서 원문 요약](<../40_RAW/기획서 원문 요약.md>)

## 관련 결정

- [261016 - System Supervisor 책임과 안전 경계](<../30_DECISIONS/Technical/261016 - System Supervisor 책임과 안전 경계.md>)

- [260708 - 안전 기준과 실패 처리 정책](<../30_DECISIONS/Technical/260708 - 안전 기준과 실패 처리 정책.md>)
- [260806 - Task Planning과 Robot Capability 경계](<../30_DECISIONS/Technical/260806 - Task Planning과 Robot Capability 경계.md>)
