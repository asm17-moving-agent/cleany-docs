---
date: 2026-08-06
source_refs:
  - "40_RAW/260803 - Gemini Robotics ER 2/04 - 공식자료 검증.md"
  - "40_RAW/260806 - MVP Task Planning 책임 경계 결정.md"
---

# 260806 - Task Planning과 Robot Capability 경계

## 결정

Gemini Robotics ER 2, RuleBasedPlanner, Navigation, VLA-backed Manipulation Skill과
Safety Control은 아래 책임 경계를 따른다. 이전 `Rule-based VLA 3 Layer` 후보는
ER 2와 물리 VLA를 구분하지 못하므로 사용하지 않는다. MVP에서는 `Local Guard`를
독립 컴포넌트나 package로 두지 않는다.

## 현재 합의된 경계

- ER 2는 motor action을 직접 생성하는 VLA가 아니라 고수준 task·tool orchestrator다.
- RuleBasedPlanner는 같은 high-level 경계의 E2E 통합 검증 구현이다.
- Manipulation Skill은 내부에 VLA policy를 포함할 수 있다.
- Mission Manager가 Mission state, Capability allowlist와 기본 argument를 검증한다.
- Capability와 Robot backend가 workspace·joint·collision·timeout 등 물리 제약을
  검증하고 실행한다.
- VLM은 고정 주기로 실행하지 않고, 작업 전 관찰과 high-level 행동의
  성공·실패·차단 뒤에 새 장면으로 재추론한다.
- safe stop과 e-stop은 일반 skill과 ER 2 응답에서 독립된 경로다.

## MVP 검증 책임

| 책임 | 소유 위치 |
|---|---|
| Mission 단계·상태와 실행 순서 | Mission Manager |
| Capability allowlist·기본 argument 형식 | Mission Manager |
| workspace·joint·collision·timeout | Capability·Robot backend |
| safe stop·e-stop·hardware fault | Robot·hardware safety 경로 |

검증 정책이 여러 Capability에서 반복되고 독립 lifecycle·interface가 필요해질 때만
별도 Guard 컴포넌트 추출을 재검토한다.

## VLM 재추론 경계

MVP의 책상 작업은 외부 개입이 없는 준정적 환경을 전제로 하지만, 로봇 행동으로
장면이 바뀔 수 있다. 따라서 VLM은 다음 checkpoint에서 호출한다.

| Trigger | 처리 |
|---|---|
| 책상 도착 후 작업 전 관찰 | 최초 Scene을 해석하고 다음 high-level 행동 하나를 제안 |
| 행동 성공·실패·차단 | 실행 결과와 새 관찰로 다음 행동 또는 완료 여부 재판단 |
| 예상과 다른 장면 변화 | 기존 proposal을 폐기하고 새 Scene으로 재추론 |

trajectory 실행 중 즉시 정지와 물체 낙하·전도 감지는 Capability·controller·hardware
safety 책임이다. VLM은 동작을 고주기로 제어하지 않고, 행동이 끝나거나 중단된 뒤
의미를 해석하고 다음 행동을 제안한다.

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

- [[40_RAW/260803 - Gemini Robotics ER 2/04 - 공식자료 검증|Gemini Robotics ER 2 공식자료 검증]]
- [[40_RAW/260806 - MVP Task Planning 책임 경계 결정|MVP Task Planning 책임 경계 결정]]
