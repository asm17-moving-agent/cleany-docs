# 기술 미해결 질문(Technical Questions)

## 요약

사용자의 선택이나 배경 설명이 필요한 항목과, 구현 및 시험으로 확인할 항목을
구분한다. 일정, 담당자와 작업 상태는 Jira에서 관리한다. 코드 기본값을 과거 결정의
이유로 추정하거나 합성 시험을 실물 근거로 바꾸지 않는다.

2026-10-17 확인한 두 선택은 닫았다. FSM+BT Runtime을 기준으로 Supervisor를
통합하고, MoveIt, 규칙 기반 조작도 MVP 조작 기준을 충족할 수 있다. 선택의 의미와
현재 구현 완료 여부는 구분한다.

## 사용자 맥락 또는 결정이 필요한 항목

| ID | 필요한 설명 또는 결정 | 현재 근거와 남겨 둔 경계 |
|---|---|---|
| T-01 | FSM+BT를 처음 도입할 때 해결하려던 문제, 검토한 대안과 선택 이유는 무엇이었나? | 이번 통합 기준은 확정했다. 과거 도입 이유를 새로 추정하지 않는다. [Mission Lifecycle](<09 - Mission Lifecycle.md>) |
| T-02 | 기존 바이너리 serial에서 micro-ROS로 전환한 이유와 감수한 제약은 무엇이었나? | 구현은 존재한다. 비교 대안과 채택 이유가 확인된 뒤 ADR로 복원한다. [Robot ROS Contract](<10 - Robot ROS Contract.md>) |
| T-03 | planner/controller, 전후, 횡이동 정책과 wheel-only 또는 IMU 융합 estimator 중 최종 채택한 것과 이유는 무엇인가? | 확인한 profile 및 비교 브랜치를 최종 결론으로 합치지 않는다. [Navigation and Mapping](<05 - Navigation and Mapping.md>) |
| T-04 | 선택된 Planner가 책상 작업만 제안할 것인가, Navigation Capability도 제안할 것인가? | 현재 별도 Navigator port를 유지한다. [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>) |
| T-05 | 사람 감지의 정지 거리, 재개 및 승인 조건과 base, arm의 실물 제한값을 어떻게 정할 것인가? | 통제 구역 데모와 실물 안전 증거를 구분한다. [Safety and Risk](<08 - Safety and Risk.md>) |
| T-06 | 사진 자동 재시도 한도, 간격, 미전송 자료 보관 기한과 삭제 조건을 어떻게 정할 것인가? | 로컬 저장과 Backend 재전송 정책은 확정했다. 7일은 검토값이다. [Perception](<07 - Perception and Scene Understanding.md>) |
| T-07 | 실물 전력 예산, battery, fuse, 배선 정격과 USB 배치를 어떻게 확정할 것인가? | 부품 목록과 실제 실장, 검증을 구분한다. [Hardware Configuration](<12 - Hardware Configuration.md>) |

## 구현과 검증으로 확인할 항목

| ID | 확인할 경계 | 이미 있는 것과 남은 것 |
|---|---|---|
| T-08 | FSM+BT Runtime에 Supervisor 허가와 중단, 복구 계약을 어떻게 연결하고 검증할 것인가? | 통합 기준은 확정했다. 별도 순차 core bridge를 Runtime에 연결하는 작업이 남았다. [System Supervisor](<14 - System Supervisor.md>) |
| T-09 | 실제 Perception, Planner와 단일 객체 Action을 재관찰 loop에 어떻게 연결할 것인가? | Mock 기반 loop는 구현돼 있다. 실제 관찰과 executor 연결을 확인해야 한다. [Mission Lifecycle](<09 - Mission Lifecycle.md>) |
| T-10 | 조작의 중복 실행, timeout, 결과 불명확, 취소에서 정지, 물체와 놓기 상태를 보존하는가? | Runtime의 Action Mock 계약은 있다. 실제 backend의 결과 및 복구 경계는 추가 확인한다. [Manipulation and Calibration](<15 - Manipulation and Calibration.md>) |
| T-11 | 작업 전후 자료 로컬 저장, Backend 저장 확인, 자동, 수동 재전송과 중복 저장 방지를 어떤 계약으로 연결할 것인가? | Gateway event ACK와 실제 이미지 저장 확인은 다르다. [Perception](<07 - Perception and Scene Understanding.md>) |
| T-12 | 현재 YOLOE-seg와 Gemini의 정확도, 지연, 실패 사례, 영상 낙하, 전도 판정과 즉시 정지를 어떤 입력으로 검증할 것인가? | 합성 및 현재 장면 평가와 실물 영상 일반화를 구분한다. [Verification](<13 - Verification and Simulation Strategy.md>) |
| T-13 | 실제 책상 조작에 필요한 도착 조건과 측정 근거는 무엇인가? | 좌석 registry, 정지, localization 오차 gate는 있다. 실제 팔 도달성, 시야와 참위치 오차는 별도다. [Navigation](<05 - Navigation and Mapping.md>) |
| T-14 | 원격 reset, 복귀와 cloud 추론 장애의 허용 조건을 어떤 API 및 Runtime 정책으로 연결할 것인가? | Gateway transport, heartbeat는 있다. 원격 복구 권한과 실제 안전 재검증은 별도다. [Operations](<02 - Robot Operations and Mission Dispatch.md>) |

분실물의 제품 처리 행동, 실제 MVP 대상과 축소 범위 및 Backend 관찰 자료의 보관, 권한은
[Planning Questions](<../10_PLANNING/99 - Questions.md>)에서 관리한다.

## 출처

- [기술 KB 구현 대조와 사용자 결정](<../40_RAW/261017 - 기술 KB 구현 대조와 사용자 결정.md>)
- [책상 정리 작업 흐름과 Action 최신화 논의](<../40_RAW/260930 - Table Cleanup Workflow.md>)
- [Action 결과와 관찰 자료 전달 정책 합의](<../40_RAW/261002 - Action 결과와 관찰 자료 전달 정책 합의.md>)
- [현재 연결과 미구현 adapter 경계 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/docs/INTEGRATION.md)
- [Supervisor 현재 한계 at c63fadb](https://github.com/asm17-moving-agent/cleany/blob/c63fadb467afac08cc62a3cfd0a5af7c59b6e8b7/ros2_ws/src/cleany_system_supervisor/README.md)

## 관련 결정

- [261017 - FSM과 BT Runtime 기준 Supervisor 통합](<../30_DECISIONS/Technical/261017 - FSM과 BT Runtime 기준 Supervisor 통합.md>)
- [261017 - MoveIt과 규칙 기반 조작의 MVP 인정](<../30_DECISIONS/Planning/261017 - MoveIt과 규칙 기반 조작의 MVP 인정.md>)
- [261016 - System Supervisor 책임과 안전 경계](<../30_DECISIONS/Technical/261016 - System Supervisor 책임과 안전 경계.md>)
- [261002 - Manipulation 결과와 안전 상태 보존](<../30_DECISIONS/Technical/261002 - Manipulation 결과와 안전 상태 보존.md>)
- [261002 - 관찰 자료 로컬 저장과 Backend 재전송](<../30_DECISIONS/Technical/261002 - 관찰 자료 로컬 저장과 Backend 재전송.md>)
