# 핵심 용어

일반적인 기술 용어가 아니라, Cleany 문서에서 의미나 책임 경계를 일관되게
해석해야 하는 용어만 정의한다.

| 용어 | 이 KB에서의 의미 |
|---|---|
| Mission | Dashboard 요청 하나에서 좌석 왕복·책상 작업·결과 보고까지 이어지는 실행 단위 |
| Mission Manager | Mission 단계 전이와 최종 결과의 Source of Truth |
| Scene State | 관찰 ID, 물체 후보·영역·의미·3D 위치와 품질을 묶은 Perception 출력 의미 |
| Task Planner | Scene과 Mission 목표로 처리 대상·순서·Capability를 제안하는 계층 |
| Gemini Robotics ER 2 | 장면·시간·물리 맥락을 이해하고 tool·VLA를 호출하는 cloud embodied-reasoning VLM |
| VLA | Vision-Language-Action. 영상·언어 입력을 로봇의 물리 action과 연결하는 learned policy |
| Robot Capability | Navigation, Observation, Manipulation처럼 로봇이 제공하는 목표 지향 기능의 중립적 상위 용어 |
| Manipulation Skill | 좌석 도착 후 arm·gripper로 수행하는 high-level 물리 작업. 내부에 VLA policy를 포함할 수 있음 |
| Safe stop / Emergency stop | Safe stop은 timeout·fault·로컬 위험에서 동작을 안전 상태로 전환하는 제어 경로이고, Emergency stop은 AI와 일반 ROS 실행보다 우선해 구동을 차단하는 물리적 경로 |
