---
source_refs:
  - "[기획서]"
related_decisions:
  - "30_DECISIONS/Technical/260708 - XLeRobot 기반 플랫폼.md"
  - "30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스.md"
  - "30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB.md"
---

# 기술 개요(Technical Overview)

## 요약

끌리니는 Dashboard 요청을 받아 지정 좌석으로 왕복하고 책상 위 물체를 처리하는
ROS 2 기반 모바일 매니퓰레이터다. 이 문서는 전체 기술 지도를 제공하며 각 설계
세부는 한 문서에서만 설명한다.

## 전체 구조

```text
Dashboard / Backend
        ↓ Mission Request · Status · Result
Mission Manager
├─ Navigator → Nav2 → Mobile Base
├─ Perception → Scene / Object State
├─ Task Planner → ER 2 또는 RuleBasedPlanner
├─ Manipulation Skills → VLA / MoveIt / Controller
└─ Reporter → Before / After / Failure

Robot Interface → Gazebo / MuJoCo / Real Robot
Safety Controls → 모든 물리 실행을 독립적으로 제한·중단
```

## 책임 지도

| 주제 | 문서 | 소유하는 질문 |
|---|---|---|
| 외부 경계 | [[20_TECHNICAL/01 - System Context|System Context]] | Dashboard·Backend·Robot은 무엇을 주고받는가? |
| 판단과 실행 | [[20_TECHNICAL/03 - Task Planning and Robot Capabilities|Task Planning and Robot Capabilities]] | 누가 작업을 고르고 어떤 Capability가 실행하는가? |
| 로봇 형태 | [[20_TECHNICAL/04 - Robot Platform XLeRobot|Robot Platform XLeRobot]] | 로봇의 신체와 subsystem 경계는 무엇인가? |
| 주행 | [[20_TECHNICAL/05 - Navigation and Mapping|Navigation and Mapping]] | 좌석까지 어떻게 왕복하는가? |
| 엣지·클라우드 | [[20_TECHNICAL/06 - Edge Runtime Jetson Orin|Edge Runtime Jetson Orin]] | 로컬과 클라우드는 무엇을 담당하는가? |
| 인식 | [[20_TECHNICAL/07 - Perception and Scene Understanding|Perception and Scene Understanding]] | 장면을 어떤 계약으로 표현하는가? |
| 안전 | [[20_TECHNICAL/08 - Safety and Risk|Safety and Risk]] | 어떤 제약이 Planner보다 우선하는가? |
| 미션 | [[20_TECHNICAL/09 - Mission Lifecycle|Mission Lifecycle]] | 미션 단계와 상태 소유자는 누구인가? |
| 로봇 계약 | [[20_TECHNICAL/10 - Robot ROS Contract|Robot ROS Contract]] | Sim과 Real이 공유하는 의미는 무엇인가? |
| 소프트웨어 | [[20_TECHNICAL/11 - ROS 2 Software Architecture|ROS 2 Software Architecture]] | 패키지 책임은 어떻게 나뉘는가? |
| 하드웨어 | [[20_TECHNICAL/12 - Hardware Configuration|Hardware Configuration]] | 실제 부품·전원·배선은 어떻게 구성되는가? |
| 검증 | [[20_TECHNICAL/13 - Verification and Simulation Strategy|Verification and Simulation Strategy]] | 단계별로 무엇을 어디서 검증하는가? |

## 현재 설계 원칙

- 제품 목표와 구현 상태를 구분한다.
- Mission 상태 전이는 Mission Manager만 소유한다.
- Planner가 제안한 행동은 로컬 검증을 통과한 뒤에만 실행한다.
- Manipulation Skill은 VLA-backed 실행을 포함할 수 있다.
- Navigation, Manipulation과 Safety Control을 하나의 모호한 skill 목록으로 섞지 않는다.
- Gazebo는 주행, MuJoCo는 책상 조작 검증을 담당한다.
- 정확한 ROS schema, parameter와 실행 명령은 구현 코드·패키지 README가 관리한다.

## 열린 경계

ER 2가 책상 작업만 오케스트레이션할지 Navigation Capability도 호출할지,
Manipulation Skill의 VLA·규칙·motion backend 조합, 사람 존재 시 안전 행동은 아직
결정하지 않았다. [[20_TECHNICAL/99 - Questions|Technical Questions]]에서 관리한다.
