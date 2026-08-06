---
source_refs:
  - "10_PLANNING/05 - Success Criteria.md"
related_decisions:
  - "30_DECISIONS/Planning/260708 - MVP 기능 범위.md"
  - "30_DECISIONS/Technical/260806 - Task Planning과 Robot Capability 경계.md"
---

# 검증과 시뮬레이션 전략(Verification and Simulation Strategy)

## 요약

Cleany는 Rule-based E2E 통합, 목표 AI planning·physical execution, 실제 로봇 순으로
검증한다. Gazebo와 MuJoCo는 서로 대체하는 simulator가 아니라 다른 subsystem
경계를 담당한다.

## 검증 단계

| 단계 | 검증 목표 | 통과 기준 |
|---|---|---|
| Core | Mission·Planner·Capability 검증 순수 logic | 성공·실패·차단·부분 결과 경로가 재현됨 |
| Rule-based 통합 | Dashboard 요청부터 report까지 E2E 경계 | 고정 입력에서 전체 lifecycle이 연결됨 |
| Perception | image→mask→3D→Scene State | 실패를 포함한 각 adapter 계약이 확인됨 |
| Navigation Sim | 좌석 왕복과 cancel·failure | Gazebo에서 Nav2·base·sensor 경계가 동작함 |
| Manipulation Sim | 여러 물체와 physical skill | MuJoCo에서 VLA·motion backend 결과가 반환됨 |
| AI 통합 | ER 2 이벤트 기반 task order와 tool orchestration | 행동마다 허용 tool 하나만 실행되고 새 장면으로 재판단함 |
| Real Robot | 실제 sensor·base·arm·safety | 승인된 통제 시나리오를 전후 결과와 함께 수행함 |

현재는 정량 성공률보다 각 단계의 pass/fail과 실패 증거를 우선 기록한다.

## Simulator 책임

### Gazebo

- 4륜 Mecanum base와 `cmd_vel` 의미
- odometry, LiDAR, IMU, camera와 TF
- prebuilt map, localization, Nav2 goal과 복귀
- 장애물·timeout·cancel·safe stop 전달

### MuJoCo

- 좌석 도착 후 arm·gripper tabletop workspace
- pick·place·collect 같은 Manipulation Skill
- VLA policy 또는 motion backend adapter
- collision, timeout, grasp 실패, 물체 낙하·전도와 결과 반환

Isaac Sim은 현재 공식 검증 구조에 역할을 배정하지 않는다. 필요하면 Raw 연구
후보로만 평가한다.

## E2E 검증 흐름

1. Dashboard가 개별 좌석 요청을 보낸다.
2. Mission Manager가 Gazebo 또는 실제 Navigator로 좌석 도착을 확인한다.
3. 작업 전 관찰을 Scene State로 변환한다.
4. RuleBasedPlanner 또는 ER 2가 다음 high-level 행동 하나를 제안한다.
5. Mission Manager가 상태·allowlist·기본 argument를 검증한다.
6. MuJoCo 또는 실제 Manipulation backend가 물리 제약을 검증하고 skill을 실행한다.
7. success·failed·blocked 뒤 장면을 재관찰한다.
8. 실행 결과와 최신 Scene으로 다음 행동 또는 완료 여부를 재판단한다.
9. 최종 관찰을 확인한 뒤 복귀와 MissionReport를 완료한다.

Simulator 사이를 반드시 실시간으로 연결할 필요는 없다. 공통 Mission·Scene·Capability
결과 계약으로 subsystem 검증 결과를 연결한다.

## 증거와 실패 기록

- 입력 Mission과 환경·모델·config 식별자
- 작업 전후 관찰
- Planner proposal과 Mission·Capability 검증의 승인·거절 이유
- Capability별 success·failed·blocked 결과
- 행동 전후 Scene과 물체 낙하·전도 같은 예상 밖 변화
- Navigation·Perception·Planning·Manipulation 중 실패 경계
- 실제 로봇에서는 감독자·작업 구역·e-stop 준비 확인

## 구현 검증 문서 경계

정확한 build, pytest, colcon, launch와 CI 명령은 구현 레포의 root·workspace·package
README가 관리한다. KB는 제품 단계와 검증 증거의 의미를 관리한다. KB 자체 Markdown
무결성 검사는 AGENTS와 repo skill 안내를 따른다.

## 관련 문서

- [[10_PLANNING/05 - Success Criteria|Success Criteria]]
- [[20_TECHNICAL/05 - Navigation and Mapping|Navigation and Mapping]]
- [[20_TECHNICAL/07 - Perception and Scene Understanding|Perception and Scene Understanding]]
