---
source_refs:
  - "[기획서]"
related_decisions:
  - "30_DECISIONS/Technical/260708 - XLeRobot 기반 플랫폼.md"
  - "30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스.md"
  - "30_DECISIONS/Technical/260715 - 로봇 프레임 구조.md"
---

# XLeRobot 로봇 플랫폼

## 요약

Cleany는 XLeRobot 상부 조작 플랫폼, 알루미늄 프로파일 프레임과 custom 4륜 Mecanum
base를 결합한 모바일 매니퓰레이터다. 이 문서는 로봇의 capability와 subsystem
경계를 다루며 부품 수량·배선은 Hardware Configuration에서 관리한다.

## Embodiment

| Subsystem | 역할 | 주요 경계 |
|---|---|---|
| Mobile Base | 실내 전후·좌우 이동과 회전 | 경로 계획은 Nav2가 담당 |
| Aluminum Frame | 상부 조작부, 컴퓨팅·센서·수거함 지지 | 실제 치수·하중 검증 필요 |
| Manipulator | 책상 위 물체 접근·파지·운반 | Skill/VLA의 안전한 실행 backend |
| Gripper | 물체 접촉·파지·해제 | 물체 손상과 파지력 제한 필요 |
| RGB-D / Arm Camera | 장면·근접 관찰과 작업 전후 기록 | 의미 판단은 Perception·Planner가 담당 |
| LiDAR / IMU / Encoder | 주행 관측과 상태 추정 | Mission 판단을 수행하지 않음 |
| Jetson Orin NX | ROS 2, sensor, adapter와 로컬 실행 검증 | 클라우드 ER 2 추론 자체는 수행하지 않음 |

## 플랫폼 선택의 의미

- 기존 XLeRobot의 조작·데이터 수집 생태계를 활용한다.
- Mecanum base의 holonomic 이동으로 책상 접근 자세를 조정한다.
- 알루미늄 프로파일로 상부 하중과 센서·컴퓨팅 장착을 반복 조정할 수 있게 한다.
- Sim과 Real에서 동일한 logical joint·frame·Capability 의미를 유지한다.

## Capability 경계

플랫폼 자체는 ‘어떤 물체를 처리할지’를 판단하지 않는다. Navigator는 base를,
Manipulation Skill은 arm·gripper를 사용한다. Safety Control은 두 실행 경로보다
우선한다.

## 주요 제약

- 책상 높이와 arm workspace가 실제 집기 영역을 제한한다.
- 프레임 높이·무게중심·수거함 위치는 주행 안정성에 영향을 준다.
- Mecanum slip은 odometry와 정밀 접근 오차를 키울 수 있다.
- arm payload와 gripper 형상은 처리 가능한 물체를 제한한다.
- base 이동과 arm 조작을 동시에 허용할지는 안전 검증 전 확정하지 않는다.

## 관련 문서

- [[20_TECHNICAL/05 - Navigation and Mapping|Navigation and Mapping]]
- [[20_TECHNICAL/10 - Robot ROS Contract|Robot ROS Contract]]
- [[20_TECHNICAL/12 - Hardware Configuration|Hardware Configuration]]
