---
date: 2026-10-16
source_type: user-instruction-record
ingest_targets:
  - technical
  - decision
---

# 261016 - System Supervisor 설계 지시

## 기록 범위

2026-10-16 Cleany 구현 작업에서 사용자가 제시한 System Supervisor 설계 지시 중
확정 원칙과 책임 경계를 발췌해 보존한다. 2026-10-17에는 해당 작업의 KB 반영을
명시적으로 요청했다. 별도 회의나 팀 전체 승인 이력을 뜻하지 않는다.

## 사용자가 확정한 설계 결정

1. **Supervisor 개입 범위**: 시스템 가용성 및 안전 관련 장애에만 개입한다.
   개별 Skill의 일반적인 실행 실패는 해당 컴포넌트가 처리한다.
2. **기능별 제한**: 장애 발생 시 영향받는 Capability만 제한하되, 안전을 보장할 수
   없다면 전체 운영을 잠근다.
3. **복구 책임 분리**: Supervisor는 복구 정책과 실행 여부를 결정하고, 실제 복구는
   해당 컴포넌트가 수행한다.
4. **미션 재개 책임**: 복구 후 Mission Manager가 환경과 작업 상태를 재검증하고
   재개 여부를 결정한다.
5. **복구 실패 처리**: 자동 복구에는 재시도 횟수와 시간 제한을 적용하며, 실패 시
   기능 제한 또는 운영 잠금을 유지한다.
6. **상태 모델 분리**: 시스템 운영 상태와 복구 작업 상태를 독립적으로 관리한다.

## 명시된 안전 및 재사용 경계

- 실제 구동 정지와 하드웨어 보호는 Supervisor와 독립된 하위 제어기 및 안전 계층이
  보장해야 한다. ESP32 통신 두절 시 ROS 정지 명령 전달에 의존하지 않는다.
- Supervisor 종료 후에도 실행 허가가 무기한 유효해서는 안 되며, 재시작하면 이전
  허가를 무효화하고 초기화부터 검증한다.
- 중단 요청 수락과 실제 중단 완료를 구분하고, 실패나 시간 초과는 오류를 확대한다.
- E-stop 해제를 소프트웨어 Service 호출만으로 수행하지 않는다.
- 기존 heartbeat, diagnostics, lifecycle과 Topic을 우선 재사용한다. Nav2 자체
  Recovery, Lifecycle Manager와 Skill의 일반 실패 처리를 중복 구현하지 않는다.
- 현재 지원하지 않는 하드웨어 기능을 성공으로 가정하지 않는다. mock 또는
  simulation 검증과 실제 하드웨어 검증을 구분한다.

## 구현과 확인 범위

위 원칙을 바탕으로 구현 레포의 `feat/system-supervisor` 작업을 진행했다. 패키지
구성, 정확한 메시지, 설정값, 테스트 결과와 미구현 adapter는 아래 구현 기록에서
확인한다. 이 링크의 commit은 로컬 작업 결과이며 원격 공개 여부와 별개다.

- [ROS 인터페이스 추가 commit de56525](https://github.com/asm17-moving-agent/cleany/commit/de56525)
- [Mission 허가 및 정지 연동 commit 03e7049](https://github.com/asm17-moving-agent/cleany/commit/03e7049)
- [Supervisor 구현 commit c63fadb](https://github.com/asm17-moving-agent/cleany/commit/c63fadb467afac08cc62a3cfd0a5af7c59b6e8b7)
- [Supervisor 구현 README](https://github.com/asm17-moving-agent/cleany/blob/c63fadb467afac08cc62a3cfd0a5af7c59b6e8b7/ros2_ws/src/cleany_system_supervisor/README.md)
