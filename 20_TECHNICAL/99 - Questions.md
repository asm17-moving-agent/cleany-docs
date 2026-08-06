---
status: draft
source_refs:
  - "20_TECHNICAL/00 - Technical Overview.md"
related_decisions:
  - "30_DECISIONS/Technical/260708 - 안전 기준과 실패 처리 정책.md"
  - "30_DECISIONS/Technical/260806 - Task Planning과 Robot Capability 경계.md"
---

# 기술 미해결 질문(Technical Questions)

## 요약

설계·계약·안전에서 실제로 남아 있는 질문만 관리한다. 일정, 담당자, 우선순위와
진행 상태는 Jira에서 관리한다.

## 질문

| 질문 | 관련 문서 |
|---|---|
| 목표 구조에서 ER 2는 책상 도착 후 작업만 오케스트레이션할 것인가, Navigation Capability도 호출할 것인가? | [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>), [Navigation and Mapping](<05 - Navigation and Mapping.md>) |
| Manipulation Skill별로 VLA policy, MoveIt·controller와 규칙 기반 fallback을 어떻게 조합할 것인가? | [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>) |
| ER 2, 로컬 VLM과 detector 후보를 어떤 실험 결과로 최종 선택할 것인가? | [Perception and Scene Understanding](<07 - Perception and Scene Understanding.md>), [Edge Runtime](<06 - Edge Runtime Jetson Orin.md>) |
| ER 2 일반 API와 Streaming을 각각 어느 단계에 사용하고 cloud 장애 시 미션을 어떻게 끝낼 것인가? | [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>), [Edge Runtime](<06 - Edge Runtime Jetson Orin.md>) |
| 작업 후 재관찰을 Mission lifecycle과 ROS interface에 어떻게 추가할 것인가? | [Perception and Scene Understanding](<07 - Perception and Scene Understanding.md>), [Mission Lifecycle](<09 - Mission Lifecycle.md>) |
| 사람 존재·접근 시 감지 거리, 정지, 재개와 운영자 승인 정책은 무엇인가? | [Safety and Risk](<08 - Safety and Risk.md>) |
| base·arm의 속도·힘·workspace·timeout과 e-stop 우선순위를 어떤 값과 계층에서 강제할 것인가? | [Safety and Risk](<08 - Safety and Risk.md>), [Robot ROS Contract](<10 - Robot ROS Contract.md>) |
| 좌석 ID→접근 pose mapping 형식과 책상 조작에 적합한 도착 조건은 무엇인가? | [Navigation and Mapping](<05 - Navigation and Mapping.md>) |
| 실제 전력 예산, battery·fuse·배선 정격과 USB 장치 배치는 어떻게 확정할 것인가? | [Hardware Configuration](<12 - Hardware Configuration.md>) |
| Dashboard·Backend와 Robot 사이 Mission Request·Progress·Result 최소 계약은 무엇인가? | [System Context](<01 - System Context.md>), [Mission Lifecycle](<09 - Mission Lifecycle.md>) |

제품 선택이 필요한 질문은 [[10_PLANNING/99 - Questions|Planning Questions]]에서 관리한다.
