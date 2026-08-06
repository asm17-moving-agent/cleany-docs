---
status: draft
---

# 용어집(Glossary)

| 용어 | 이 KB에서의 의미 |
|---|---|
| Cleany | 무인 스터디카페에서 퇴실 후 책상 위 물체를 처리하는 모바일 매니퓰레이터 프로젝트 |
| Mission | Dashboard 요청 하나에서 좌석 왕복·책상 작업·결과 보고까지 이어지는 실행 단위 |
| Mission Manager | Mission 단계 전이와 최종 결과의 Source of Truth |
| Scene State | 관찰 ID, 물체 후보·영역·의미·3D 위치와 품질을 묶은 Perception 출력 의미 |
| Task Planner | Scene과 Mission 목표로 처리 대상·순서·Capability를 제안하는 계층 |
| Gemini Robotics ER 2 | 장면·시간·물리 맥락을 이해하고 tool·VLA를 호출하는 cloud embodied-reasoning VLM |
| VLA | Vision-Language-Action. 영상·언어 입력을 로봇의 물리 action과 연결하는 learned policy |
| RuleBasedPlanner | AI Planner 연결 전 같은 high-level 계약을 검증하는 규칙 기반 통합 구현 |
| Robot Capability | Navigation, Observation, Manipulation처럼 로봇이 제공하는 목표 지향 기능의 중립적 상위 용어 |
| Manipulation Skill | 좌석 도착 후 arm·gripper로 수행하는 high-level 물리 작업. 내부에 VLA policy를 포함할 수 있음 |
| Local Guard | Planner·VLA 출력의 schema, 상태, workspace, collision과 limit을 실행 전에 검증하는 로컬 경계 |
| Navigation | 사전 제작 지도에서 대기 위치와 지정 좌석 사이를 왕복하는 기능 |
| Nav2 | ROS 2 기반 localization·planning·control framework |
| Safe stop | timeout·fault·로컬 위험에서 현재 동작을 안전 상태로 전환하는 독립 제어 경로 |
| Emergency stop | AI와 일반 ROS 실행보다 우선해 구동을 차단하는 물리적 비상 정지 경로 |
| XLeRobot | Cleany가 상부 듀얼 매니퓰레이터와 깊이 카메라 구성을 활용하는 기반 플랫폼 |
| Gazebo | Mobile base, sensor, localization과 Nav2를 검증하는 simulator |
| MuJoCo | 좌석 도착 후 tabletop arm·gripper와 Manipulation Skill을 검증하는 simulator |
| Planning | 문제, 사용자, 가치, 범위, 시나리오와 성공 기준을 관리하는 KB 계층 |
| Technical | 시스템 개념, 경계, 제약, 리스크와 검증 전략을 관리하는 KB 계층 |
| Decision | 무엇을 왜 선택했는지와 재검토 조건을 기록하는 문서 |
| Raw | 초안, 개인 학습 노트, 회의록, 조사 자료와 임시 메모를 두는 비공식 작업 공간 |
| Jira | 일정, 담당자, 우선순위와 작업 상태의 Source of Truth |
