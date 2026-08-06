---
ingest_targets:
  - technical
  - decision
decision_candidates:
  - "MVP에서 독립 Local Guard를 두지 않음"
  - "VLM은 행동 완료·실패·장면 변화에 이벤트 기반 재추론"
date: 2026-08-06
source_type: team-decision-record
---

# 260806 - MVP Task Planning 책임 경계 결정

## 독립 Local Guard를 두지 않음

KB 재점검 과정에서 MVP에는 `Local Guard`를 독립 컴포넌트나 package로 두지 않기로
결정했다. 검증과 안전 책임 자체를 제거하는 결정은 아니다.

- Mission 단계, Capability allowlist와 기본 argument 검증은 Mission Manager가 맡는다.
- workspace·joint·collision·timeout 같은 물리 실행 제약은 Capability와 Robot
  backend가 맡는다.
- safe stop·e-stop과 hardware fault 대응은 Planner·cloud와 독립된 로컬 경로를
  유지한다.
- 검증 정책이 여러 Capability에서 중복되고 독립 interface가 필요해질 때 별도
  컴포넌트 추출을 재검토한다.

## 결정 이유

MVP 단계에서 별도 Guard interface와 package를 추가하면 책임 경계와 통합 비용이
늘어난다. 현재 필요한 검증은 Mission Manager, Capability와 hardware safety 경로의
기존 책임 안에서 표현할 수 있다.

## VLM은 이벤트 기반으로 재추론

MVP 작업 구역은 사람이나 외부 물체가 작업 중 개입하지 않는 준정적 환경으로 둔다.
하지만 로봇 행동으로 물체가 이동·낙하·전도되거나 가려진 대상이 드러날 수 있으므로,
책상 도착 후 VLM을 최초 한 번만 호출하고 전체 계획을 그대로 실행하지 않는다.

- 작업 전 장면에서 최초 추론한다.
- 한 번에 high-level 행동 하나만 승인·실행한다.
- 행동이 성공·실패·차단으로 끝나면 새 장면과 실행 결과를 VLM에 전달해 다음 행동을
  다시 판단한다.
- 예상 밖 장면 변화가 확인되면 기존 proposal을 계속 사용하지 않고 재관찰·재추론한다.
- 고정 주기 또는 trajectory 실행 중의 VLM 호출로 활성 동작을 변경하지 않는다.

물체 낙하·전도 순간의 즉시 대응은 Capability, controller와 hardware safety가
담당하고, 정지 또는 행동 종료 후 의미 해석과 다음 행동 선택은 VLM이 담당한다.
구체적으로 어떤 local signal로 예상 밖 변화를 감지할지는 추가 결정이 필요하다.
