# 기술 미해결 질문(Technical Questions)

## 요약

설계, 계약, 안전에서 실제로 남아 있는 질문만 관리한다. 일정, 담당자, 우선순위와
진행 상태는 Jira에서 관리한다.

## 질문

| 질문 | 관련 문서 |
|---|---|
| 선택된 Planner가 책상 도착 후 작업만 제안할 것인가, Navigation Capability도 제안할 것인가? | [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>), [Navigation and Mapping](<05 - Navigation and Mapping.md>) |
| Manipulation Skill별로 VLA policy, MoveIt, controller와 규칙 기반 fallback을 어떻게 조합할 것인가? | [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>) |
| 현재 YOLOE-seg와 Gemini Perception 경로의 정확도, 지연, 실패 사례를 어떤 기준으로 검증할 것인가? | [Perception and Scene Understanding](<07 - Perception and Scene Understanding.md>), [Verification and Simulation Strategy](<13 - Verification and Simulation Strategy.md>) |
| API 기반 VLM을 채택할 경우 일반 API와 Streaming을 각각 어느 단계에 사용하고 cloud 장애 시 미션을 어떻게 끝낼 것인가? | [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>), [Edge Runtime](<06 - Edge Runtime Jetson Orin.md>) |
| 작업 후 재관찰을 Mission lifecycle과 ROS interface에 어떻게 추가할 것인가? | [Perception and Scene Understanding](<07 - Perception and Scene Understanding.md>), [Mission Lifecycle](<09 - Mission Lifecycle.md>) |
| 영상에서 물체 낙하 또는 전도를 판정할 기준과 즉시 정지 조건을 어떻게 검증할 것인가? | [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>), [Safety and Risk](<08 - Safety and Risk.md>), [Verification and Simulation Strategy](<13 - Verification and Simulation Strategy.md>) |
| 사람의 존재 또는 접근을 감지했을 때 정지 거리, 재개 조건과 운영자 승인 정책은 무엇인가? | [Safety and Risk](<08 - Safety and Risk.md>) |
| base와 arm의 속도, 힘, workspace, timeout과 e-stop 우선순위를 어떤 값과 계층에서 강제할 것인가? | [Safety and Risk](<08 - Safety and Risk.md>), [Robot ROS Contract](<10 - Robot ROS Contract.md>) |
| 좌석 ID→접근 pose mapping 형식과 책상 조작에 적합한 도착 조건은 무엇인가? | [Navigation and Mapping](<05 - Navigation and Mapping.md>) |
| 실제 전력 예산, battery, fuse, 배선 정격과 USB 장치 배치는 어떻게 확정할 것인가? | [Hardware Configuration](<12 - Hardware Configuration.md>) |
| Backend와 Robot의 논리 관제 계약을 어떤 transport, API 또는 event schema로 구현하고 heartbeat와 offline 판정 기준을 어떻게 정할 것인가? | [Robot Operations and Mission Dispatch](<02 - Robot Operations and Mission Dispatch.md>), [System Context](<01 - System Context.md>) |
| 원격 reset을 허용할 복구 가능 오류와 대기 위치 복귀를 수락할 안전 조건은 무엇인가? | [Robot Operations and Mission Dispatch](<02 - Robot Operations and Mission Dispatch.md>), [Safety and Risk](<08 - Safety and Risk.md>) |
| Manipulation Action의 중복 요청을 어떻게 막고, 성공, 차단, 실패, 취소 및 치명 오류와 정지, 물체, 놓기 상태를 ModuleResult 및 MissionReport에 어떻게 보존할 것인가? | [Mission Lifecycle](<09 - Mission Lifecycle.md>), [ROS 2 Software Architecture](<11 - ROS 2 Software Architecture.md>) |
| 작업 전후 관찰 자료의 로컬 저장 확인, Backend 저장 확인과 자동 및 수동 재전송을 어떤 ROS/API 계약으로 제공하고, 같은 관찰 ID의 중복 저장을 어떻게 막을 것인가? | [Perception and Scene Understanding](<07 - Perception and Scene Understanding.md>), [Robot Operations and Mission Dispatch](<02 - Robot Operations and Mission Dispatch.md>) |
| 사진 전송의 자동 재시도 한도와 간격 및 재연결 시 전송 방식을 어떻게 정할 것인가? | [Perception and Scene Understanding](<07 - Perception and Scene Understanding.md>) |
| 미전송 로컬 관찰 자료의 보관 기한과 기한 계산 및 삭제 조건을 어떻게 정할 것인가? 기존 초안의 7일은 검토값이다. | [Perception and Scene Understanding](<07 - Perception and Scene Understanding.md>) |
| 영상 감지나 미션 취소 뒤 실제 구동 정지를 어떤 상태 또는 controller 응답으로 확인하고 보고할 것인가? | [Mission Lifecycle](<09 - Mission Lifecycle.md>), [Safety and Risk](<08 - Safety and Risk.md>), [Verification and Simulation Strategy](<13 - Verification and Simulation Strategy.md>) |

제품 선택이 필요한 질문은 [Planning Questions](<../10_PLANNING/99 - Questions.md>)에서 관리한다.

## 출처

- [00 - Technical Overview](<00 - Technical Overview.md>)
- [책상 정리 작업 흐름과 Action 최신화 논의](<../40_RAW/260930 - Table Cleanup Workflow.md>)
- [Action 결과와 관찰 자료 전달 정책 합의](<../40_RAW/261002 - Action 결과와 관찰 자료 전달 정책 합의.md>)

## 관련 결정

- [260708 - 안전 기준과 실패 처리 정책](<../30_DECISIONS/Technical/260708 - 안전 기준과 실패 처리 정책.md>)
- [260806 - Task Planning과 Robot Capability 경계](<../30_DECISIONS/Technical/260806 - Task Planning과 Robot Capability 경계.md>)
- [261002 - Manipulation 결과와 안전 상태 보존](<../30_DECISIONS/Technical/261002 - Manipulation 결과와 안전 상태 보존.md>)
- [261002 - 관찰 자료 로컬 저장과 Backend 재전송](<../30_DECISIONS/Technical/261002 - 관찰 자료 로컬 저장과 Backend 재전송.md>)
