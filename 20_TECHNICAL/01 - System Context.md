# 시스템 컨텍스트(System Context)

## 요약

Cleany 시스템은 운영자가 사용하는 Dashboard, 미션을 할당하고 외부 상태를 관리하는
Backend, 물리 미션을 수행하는 Robot으로 나뉜다. 이 문서는 세 영역의 경계만 다루며
관제 lifecycle과 로봇 내부 package, topic은 다루지 않는다.

## 시스템 경계

```mermaid
flowchart LR
    operator["스터디카페 운영자"]
    dashboard["Dashboard"]
    backend["Backend"]
    robot["Cleany Robot"]
    site["지정 좌석, 책상"]

    operator -->|좌석 선택, 미션 요청| dashboard
    dashboard -->|요청| backend
    backend -->|Mission Request| robot
    robot -->|상태, 전후 관찰, 결과| backend
    backend -->|진행, 최종 결과| dashboard
    robot <--> site
```

## 구성요소 책임

| 구성요소 | 책임 | 책임 밖 |
|---|---|---|
| Dashboard | 대상 좌석 선택, 수동 요청, 진행, 최종 결과 표시 | 로봇 상태 전이와 motor 제어 |
| Backend | 우선순위 대기열, 미션 할당, Robot 상태와 결과 관리, Dashboard 연동 | Robot 내부 planning과 물리 안전 판단 |
| Robot | 이동, 관찰, 계획, 물리 실행, 복귀와 MissionReport 생성 | 점포 운영 정책 임의 확정 |
| 운영자 | 미션 요청, 결과 확인, 필요 시 비상 정지 | 작업 중 로봇 구역 진입을 전제로 하지 않음 |

## 최소 정보 흐름

### Mission Request

제품 관점에서 요청은 대상 좌석을 식별할 수 있어야 한다. 대기열과 수락 및 거절의
의미는 [Robot Operations and Mission Dispatch](<02 - Robot Operations and Mission Dispatch.md>)에서
관리하고, 정확한 API 필드와 queue schema는 Backend 구현 문서에서 정한다.

### Progress

Dashboard는 최소한 요청 수락, 이동, 책상 작업, 복귀, 완료, 실패를 구분해 표시할 수
있어야 한다. 로봇 내부의 세부 FSM state를 그대로 외부 계약으로 노출할 필요는 없다.

### Result

최종 결과는 성공 여부만이 아니라 작업 전후 관찰, 처리한 대상, 실패 및 미처리 대상을
포함해야 한다. 저장 기간과 payload는 아직 확정하지 않는다.

## 실패 경계

- Backend 연결 실패가 로봇의 safe stop, e-stop을 막아서는 안 된다.
- Robot은 처리하지 못한 대상을 성공으로 축약하지 않는다.
- Dashboard의 재시도, 알림 사용자 경험은 Planning Questions에 남아 있다.
- Backend가 Mission Manager의 내부 상태를 직접 변경하지 않는다.

## 관련 문서

- [Target Scenario](<../10_PLANNING/02 - Target Scenario.md>)
- [Robot Operations and Mission Dispatch](<02 - Robot Operations and Mission Dispatch.md>)
- [Mission Lifecycle](<09 - Mission Lifecycle.md>)
- [ROS 2 Software Architecture](<11 - ROS 2 Software Architecture.md>)

## 출처

- [기획서 원문 요약](<../40_RAW/기획서 원문 요약.md>)

## 관련 결정

- [260708 - MVP 기능 범위](<../30_DECISIONS/Planning/260708 - MVP 기능 범위.md>)
