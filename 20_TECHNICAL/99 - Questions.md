# 기술 미해결 질문(Technical Questions)

## 요약

설계, 계약, 안전에서 실제로 남아 있는 질문만 관리한다. 일정, 담당자, 우선순위와
진행 상태는 Jira에서 관리한다.

## 질문

| 질문 | 관련 문서 |
|---|---|
| 선택된 Planner가 책상 도착 후 작업만 제안할 것인가, Navigation Capability도 제안할 것인가? | [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>), [Navigation and Mapping](<05 - Navigation and Mapping.md>) |
| Manipulation Skill별로 VLA policy, MoveIt, controller와 규칙 기반 fallback을 어떻게 조합할 것인가? | [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>) |
| 로컬 VLM, API 기반 VLM, YOLO와 SAM 계열, YOLO segmentation을 정확도, 지연, 실패 형태와 조작 적합성으로 어떻게 비교해 선택할 것인가? | [Perception and Scene Understanding](<07 - Perception and Scene Understanding.md>), [Edge Runtime](<06 - Edge Runtime Jetson Orin.md>) |
| API 기반 VLM을 채택할 경우 일반 API와 Streaming을 각각 어느 단계에 사용하고 cloud 장애 시 미션을 어떻게 끝낼 것인가? | [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>), [Edge Runtime](<06 - Edge Runtime Jetson Orin.md>) |
| 작업 후 재관찰을 Mission lifecycle과 ROS interface에 어떻게 추가할 것인가? | [Perception and Scene Understanding](<07 - Perception and Scene Understanding.md>), [Mission Lifecycle](<09 - Mission Lifecycle.md>) |
| Manipulation 실행 중 물체의 낙하 또는 전도와 예상 밖 장면 변화를 어떤 local signal로 감지하고 언제 동작을 중단해 재관찰할 것인가? | [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>), [Safety and Risk](<08 - Safety and Risk.md>), [Verification and Simulation Strategy](<13 - Verification and Simulation Strategy.md>) |
| 사람의 존재 또는 접근을 감지했을 때 정지 거리, 재개 조건과 운영자 승인 정책은 무엇인가? | [Safety and Risk](<08 - Safety and Risk.md>) |
| base와 arm의 속도, 힘, workspace, timeout과 e-stop 우선순위를 어떤 값과 계층에서 강제할 것인가? | [Safety and Risk](<08 - Safety and Risk.md>), [Robot ROS Contract](<10 - Robot ROS Contract.md>) |
| 좌석 ID→접근 pose mapping 형식과 책상 조작에 적합한 도착 조건은 무엇인가? | [Navigation and Mapping](<05 - Navigation and Mapping.md>) |
| 실제 전력 예산, battery, fuse, 배선 정격과 USB 장치 배치는 어떻게 확정할 것인가? | [Hardware Configuration](<12 - Hardware Configuration.md>) |
| Backend와 Robot의 논리 관제 계약을 어떤 transport, API 또는 event schema로 구현하고 heartbeat와 offline 판정 기준을 어떻게 정할 것인가? | [Robot Operations and Mission Dispatch](<02 - Robot Operations and Mission Dispatch.md>), [System Context](<01 - System Context.md>) |
| 원격 reset을 허용할 복구 가능 오류와 대기 위치 복귀를 수락할 안전 조건은 무엇인가? | [Robot Operations and Mission Dispatch](<02 - Robot Operations and Mission Dispatch.md>), [Safety and Risk](<08 - Safety and Risk.md>) |

제품 선택이 필요한 질문은 [Planning Questions](<../10_PLANNING/99 - Questions.md>)에서 관리한다.

## 출처

- [00 - Technical Overview](<00 - Technical Overview.md>)

## 관련 결정

- [260708 - 안전 기준과 실패 처리 정책](<../30_DECISIONS/Technical/260708 - 안전 기준과 실패 처리 정책.md>)
- [260806 - Task Planning과 Robot Capability 경계](<../30_DECISIONS/Technical/260806 - Task Planning과 Robot Capability 경계.md>)
