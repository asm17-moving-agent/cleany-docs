---
status: draft
source_refs:
  - "[기획서]"
related_decisions:
  - "30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스.md"
---

# 내비게이션과 매핑(Navigation and Mapping)

## 요약

MVP에서 로봇은 사전에 제작한 지도를 사용해 대기 위치와 운영자가 지정한 개별
좌석 사이를 자율 왕복한다. Mapping은 환경 준비 과정이며 데모 기능이 아니다.

## 지도와 좌석

- 지도는 데모 전에 제작·검증한다.
- Backend의 좌석 ID는 Robot이 사용할 목표 pose로 해석되어야 한다.
- 목표 pose는 단순 도착점이 아니라 책상을 관찰·조작할 수 있는 접근 자세를
  고려해야 한다.
- 좌석 배치가 바뀌면 map 전체보다 좌석 pose mapping을 우선 갱신할 수 있어야 한다.

정확한 pose map 형식과 관리 위치는 구현 시 정한다.

## 주행 흐름

```text
target seat id
  → target pose lookup
  → Nav2 goal
  → localization / planning / control
  → arrival result
  → desk work
  → home pose Nav2 goal
```

Mission Manager는 도착·실패·취소 결과만 소비하며 wheel command를 직접 만들지 않는다.

## Gazebo 역할

Gazebo는 다음 Navigation 경계를 검증한다.

- 4륜 Mecanum base command와 odometry
- LiDAR·IMU·camera sensor 연결
- map·localization·Nav2 goal과 복귀
- 좌석 접근 pose와 장애물 조건
- timeout·cancel·safe stop 전달

MuJoCo는 좌석 도착 후 tabletop manipulation을 주로 검증하며 Navigation의 공식
시뮬레이터로 사용하지 않는다.

## 현재와 목표 경계

현재 Mission Manager는 Navigator를 Planner와 별도 port로 호출한다. ER 2가 향후
Navigation Capability까지 직접 선택할지는 열린 질문이며, 그 전까지 기존 경계를
유지한다.

## 위험과 확인 사항

- Mecanum slip과 geometry 오차로 인한 localization·도킹 오차
- 의자·가방 등 임시 장애물과 좁은 통로
- 책상 조작에 부적합한 최종 base pose
- map과 실제 좌석 배치 불일치
- Navigation 성공과 안전한 조작 자세를 같은 의미로 처리하는 오류

## 관련 문서

- [[20_TECHNICAL/04 - Robot Platform XLeRobot|Robot Platform XLeRobot]]
- [[20_TECHNICAL/10 - Robot ROS Contract|Robot ROS Contract]]
- [[20_TECHNICAL/13 - Verification and Simulation Strategy|Verification and Simulation Strategy]]
