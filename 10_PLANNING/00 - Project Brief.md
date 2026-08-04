---
status: draft
source_refs:
  - "[기획서]"
related_decisions:
  - "30_DECISIONS/Planning/260708 - MVP 기능 범위.md"
  - "30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB.md"
---

# 프로젝트 개요(Project Brief)

## 1. 요약

끌리니(Cleany)는 무인 스터디카페의 이용 후 정리·점검 업무를 자동화하기 위한 XLeRobot 기반 관리 로봇 프로젝트다. 1차 MVP는 Dashboard 요청부터 결과 표시까지, 사전에 정한 쓰레기와 분실물 후보를 각각의 보관 위치로 옮기는 흐름을 다룬다.

## 2. 현재 기획 이해

- 프로젝트명은 `끌리니(Cleany) : 무인 점포 관리 로봇`이다.
- 팀명은 `AI 에이전트는 움직이고 싶어`이다.
- 팀원은 이동근, 박창수, 이정현이다.
- 끌리니는 운영자 요청을 받아 지정 공간으로 이동하여 쓰레기와 분실물 후보를 구분·수거·보관하고 결과를 제공하는 로봇으로 이해한다.
- 제품의 1차 타깃은 무인 스터디카페이며, 현재 시연은 개발센터 개발공간으로 한정한다.
- 1차 MVP에는 Dashboard·Backend의 요청·Mission Queue·결과 표시, 쓰레기 수거, 분실물 별도 보관, 복귀가 포함된다. 분실물 분류 기준과 보관·인계 절차는 추가 정의가 필요하다.

## 3. 왜 중요한가

무인 점포와 공간 공유 서비스는 상주 인력이 없거나 적기 때문에 이용 종료 직후 청결, 정돈, 시설 상태 유지가 일정하지 않을 수 있다. 이 공백은 고객 경험과 브랜드 이미지에 직접적인 영향을 주며, 점주 1인이 다수 매장을 관리할 때 운영 부담을 키운다.

## 4. 핵심 내용

### 4.1 프로젝트 소개

- 이동형 로봇과 AI 비전 기술을 활용해 무인 점포의 이용 종료 후 정리 및 점검 업무를 자동화한다.
- XLeRobot 기반 모바일 매니퓰레이터가 매장 내 쓰레기, 분실물 후보, 흐트러진 집기류를 확인하고 정리한다.
- 사람이 상주하지 않는 시간에도 다음 이용자가 바로 사용할 수 있는 공간 상태를 만드는 것을 목표로 한다.

### 4.2 주요 기능과 MVP 초점

| 구분        | 내용                                  | 상태                  |
| --------- | ----------------------------------- | ------------------- |
| 1차 MVP | Dashboard·Backend 요청부터 쓰레기 수거·분실물 별도 보관·복귀·결과 표시까지 | 현재 기준 |
| 분실물 처리 | 분실물 후보를 별도 보관함으로 옮김 | 분류 기준과 보관·인계 절차 추가 정의 필요 |
| 시연 환경 | 개발센터 개발공간 | 지도·대상 구역·안전 구역 추가 정의 필요 |
| 후속 기능 후보  | 공간 정리/정돈, 책상 닦기, 소등, 문단속            | 1차 MVP 제외 후보        |

### 4.3 주요 기술 키워드

- Embodied AI
- Vision-Language-Action
- Robotics
- XLeRobot
- ROS 2
- SLAM
- Nav2
- Jetson Orin NX 16GB
- RGB-D
- 2D LiDAR
- IMU
- 객체 탐지 및 Segmentation
- 경량 VLM
- MuJoCo
- Isaac Sim
- TensorRT
- 온디바이스 추론

### 4.4 기대효과 초안

- 사용자 측면: 점포 청결 및 정돈 미흡으로 인한 고객 이탈과 이미지 손실을 줄이는 데 기여한다.
- 비즈니스 측면: 반복 순찰 및 청소 소요를 줄여 다점포 운영 효율을 높이는 데 기여한다.
- 확장 측면: 향후 로봇 임대, 유지관리 구독, 현장 설치 및 캘리브레이션 패키지 등으로 확장 가능성이 기획서에 언급되어 있다.

## 5. 관련 기술 문서

- [[20_TECHNICAL/00 - Technical Overview|Technical Overview]]
- [[20_TECHNICAL/01 - System Concept|System Concept]]
- [[20_TECHNICAL/04 - Robot Platform XLeRobot|Robot Platform XLeRobot]]

## 6. 관련 결정

- [[30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB|Jetson Orin NX 16GB]]는 메인 엣지 컴퓨팅 장치를 채택한 `selected` Decision이다.
- [[30_DECISIONS/Planning/260708 - MVP 기능 범위|MVP 기능 범위]] 초안에 7/10 회의의 반영 후보를 추가했다.
