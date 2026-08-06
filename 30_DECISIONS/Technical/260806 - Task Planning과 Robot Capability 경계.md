---
date: 2026-08-06
source_refs:
  - "40_RAW/260803 - Gemini Robotics ER 2/00 - README.md"
  - "40_RAW/260803 - Gemini Robotics ER 2/03 - 시스템 아키텍처와 책임 경계.md"
---

# 260806 - Task Planning과 Robot Capability 경계

## 결정

Gemini Robotics ER 2, RuleBasedPlanner, Navigation, VLA-backed Manipulation Skill과
Safety Control은 아래 책임 경계를 따른다. 이전 `Rule-based VLA 3 Layer` 후보는
ER 2와 물리 VLA를 구분하지 못하므로 사용하지 않는다.

## 현재 합의된 경계

- ER 2는 motor action을 직접 생성하는 VLA가 아니라 고수준 task·tool orchestrator다.
- RuleBasedPlanner는 같은 high-level 경계의 E2E 통합 검증 구현이다.
- Manipulation Skill은 내부에 VLA policy를 포함할 수 있다.
- Skill·Planner 출력은 로컬 Guard를 통과한 뒤에만 실행된다.
- Mission state는 Mission Manager가 소유한다.
- safe stop과 e-stop은 일반 skill과 ER 2 응답에서 독립된 경로다.

## 남은 선택

| 선택 | 장점 | 고려할 점 |
|---|---|---|
| ER 2가 책상 도착 후 Manipulation만 orchestration | 현재 Mission Manager·Navigator 경계와 단순하게 맞음 | 장기적으로 mobility tool orchestration을 확장해야 할 수 있음 |
| ER 2가 Navigation과 Manipulation 모두 orchestration | 하나의 agent가 전체 physical workflow를 조정 가능 | safety·상태·tool 범위가 커지고 현재 구현 경계가 바뀜 |

Manipulation Skill별 VLA·MoveIt·controller 조합도 실험 후 결정한다.

## 현재 구현 기준

결정 전에는 Mission Manager가 Navigator를 직접 호출하고, Planner는 책상 Scene에서
high-level task를 제안하는 현재 경계를 유지한다. 문서에서 Navigation을 무조건
Physical Skill에 포함하거나 제외했다고 확정하지 않는다.

## 결정 조건

- Rule-based E2E 흐름과 ER 2 structured output 검증
- MuJoCo에서 VLA-backed Manipulation tool orchestration 검증
- Navigation을 ER 2 tool로 노출했을 때 상태·취소·실패 복잡도 비교
- cloud 지연·실패 시 Mission Manager가 안전하게 미션을 끝낼 수 있는지 확인

## 출처

- [[40_RAW/260803 - Gemini Robotics ER 2/00 - README|Gemini Robotics ER 2 조사]]
- [[40_RAW/260803 - Gemini Robotics ER 2/03 - 시스템 아키텍처와 책임 경계|시스템 책임 경계]]
