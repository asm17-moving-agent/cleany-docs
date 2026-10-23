---
date: 2026-10-23
source_type: user-instruction-record
ingest_targets:
  - technical
---

# 261023 - System Supervisor Mission Runtime 통합 지시

## 기록 범위

2026-10-23과 2026-10-24 구현 작업에서 사용자가 지시한 System Supervisor와 FSM+BT
Mission Runtime의 통합 원칙과, 그 지시에 따라 구현한 결과를 발췌해 보존한다. 별도
회의나 팀 전체 승인 이력을 뜻하지 않는다.

## 사용자가 지시한 통합 원칙

1. 기존 System Supervisor의 책임 경계와 fail-closed 정책을 유지하면서 main의
   `mission_runtime`을 기준으로 통합한다. 이전 순차 Mission 구현은 되살리지 않는다.
2. Supervisor는 상태 판단, Fault와 Capability 관리, 운영 허가와 복구 조정을 담당한다.
   Mission Runtime은 실제 미션 실행, 정지, 재개와 Journal을 담당한다.
3. Runtime 기능을 무조건 삭제하지 않고 중복되는 부분은 역할에 따라 통합한다.
   Runtime 자체의 실행 오류 처리와 Supervisor의 시스템 Fault 관리를 구별하고, 정지
   완료 판단과 안전 상태 검증의 책임을 명확히 한다.
4. Logger와 중복되는 JSONL 이벤트 기록은 제거하고 구조화된 이벤트 발행은 유지한다.
5. main에서 삭제된 패키지는 기존 대체 구조를 확인한 뒤 복원 여부를 결정한다.
6. 2026-10-24에는 이 KB의 System Supervisor 문서를 현재 구현에 맞게 갱신하고 팔 이동
   안전 판단의 책임 주체를 정리하도록 요청했다.

## 지시에 따라 구현한 결과

아래는 구현 결과의 요약이며 실물 검증이나 팀 승인을 뜻하지 않는다.

- Runtime은 감독 모드에서 미션마다 Supervisor lease 하나를 받고, lease가 있을 때만
  움직이며, 권한을 잃으면 정지한다. 정지 완료 판단은 Runtime이 하고 Supervisor의
  정지 요청 Action에 그 결과로 답한다.
- 감독 모드에서 Nav2 lifecycle 가용성과 독립 안전 fault 경로는 Supervisor 한 곳에서
  판단한다. Runtime의 기존 판단 경로는 감독 해제 모드에만 남겼다.
- 팔 상태에 따른 주행 허가는 Supervisor Capability에서 제외하고, 조작 결과를 근거로
  하는 Runtime의 기존 주행 gate(`safe_to_drive`)가 판단한다. Supervisor는 팔 실행
  계층의 가용성만 다룬다.
- `cleany_robot_interface`는 복원하지 않았다. Nav2 lifecycle 복구 owner는
  `cleany_navigation`, 팔 가용성 보고는 `cleany_skill_executor`에 두었다.

## 출처

- [구현 브랜치 feat/system-supervisor at 36a641d](https://github.com/asm17-moving-agent/cleany/tree/36a641d6892e431353c3cfefd4d23f1e0f2424a9)
- [Supervisor 계약 at 36a641d](https://github.com/asm17-moving-agent/cleany/blob/36a641d6892e431353c3cfefd4d23f1e0f2424a9/ros2_ws/src/cleany_system_supervisor/docs/supervision.md)
- [Mission 감독 계약 at 36a641d](https://github.com/asm17-moving-agent/cleany/blob/36a641d6892e431353c3cfefd4d23f1e0f2424a9/ros2_ws/src/cleany_interfaces/docs/mission.md)
- [검증 기록 at 36a641d](https://github.com/asm17-moving-agent/cleany/blob/36a641d6892e431353c3cfefd4d23f1e0f2424a9/docs/EVIDENCE.md)
