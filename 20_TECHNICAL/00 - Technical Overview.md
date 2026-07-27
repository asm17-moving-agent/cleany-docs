---
type: technical
status: draft
reviewers:
  -
tags:
  - technical
  - draft
  - cleany
source_refs:
  - "[기획서]"
related_decisions:
  - "30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB.md"
related_jira:
  -
updated: 2026-07-27
---

# 기술 개요(Technical Overview)

## 1. 요약

끌리니의 예비 기술 구조는 XLeRobot 상부 모듈과 custom 4륜 Mecanum base를 결합한 모바일 매니퓰레이터가 인식, 판단, 이동, 조작을 수행하는 구조다. 현재 기준 핵심 기술은 Agentic VLA, Rule Guard, SLAM, ROS 2 Humble·Navigation/Nav2, Jetson Orin NX 16GB·JetPack 6.2, RGB-D, 2D LiDAR, IMU, 객체 탐지 및 Segmentation, MuJoCo, Isaac Sim, TensorRT다.

## 2. 기획 맥락

무인 스터디카페에서 운영자가 Dashboard로 요청하면 Backend가 Mission Queue를 통해 로봇에 작업을 할당한다. 현재 시연 환경은 개발센터 개발공간으로 한정하며, 기술 구조는 요청·상태·결과 표시와 인식, 주행, 조작, 판단, 안전을 나누어 다룬다.

## 3. 기술 개념

### 3.1 상위 구조

1. 센서가 공간과 물체 상태를 관찰한다.
2. 객체 탐지 및 Segmentation이 쓰레기, 분실물 후보, 불확실하거나 위험한 물체를 구분한다.
3. Agentic VLA가 물체 의미와 주변 맥락을 해석하고 행동 후보를 만든다.
4. Rule Guard가 안전·신뢰도·허용 작업을 검증해 수거, 분실물 별도 보관, 사람 검토 요청 중 행동을 선택한다.
5. Nav2 기반 주행이 작업 대상 구역까지 이동한다.
6. 매니퓰레이터가 쓰레기 수거와 분실물 별도 보관 조작을 수행한다.
7. 작업 완료 후 대기 위치로 복귀하고 Mission feedback, MissionReport, 전후 결과를 Backend와 Dashboard에 제공한다.

### 3.2 핵심 구성요소

| 구성요소                | 현재 이해                          |
| ------------------- | ------------------------------ |
| Robot platform | XLeRobot 상부 모듈과 custom 4륜 Mecanum base를 결합한 모바일 매니퓰레이터 |
| RGB-D               | 물체 후보와 깊이 정보를 획득하는 센서          |
| 2D LiDAR            | 지도 작성, 위치 추정, 장애물 감지에 활용되는 센서  |
| IMU                 | 자세와 움직임 추정 보조 센서               |
| Jetson Orin NX 16GB | 온디바이스 AI 추론 및 로봇 런타임 컴퓨팅 장치    |
| ROS 2 Humble/Nav2 | 자율주행과 로봇 소프트웨어 통합 기반 |
| Agentic VLA / Rule Guard | 의미 기반 행동 후보 생성과 안전·신뢰도 기반 행동 검증 구조 |
| MuJoCo/Isaac Sim    | 주행, 접근, 파지, 수거, 정돈 시나리오 검증 환경  |

## 4. 인터페이스 / 경계

| 구성요소 | 책임 | 경계 |
|---|---|---|
| Perception | 객체 탐지, Segmentation, 위치 추정 | 최종 행동 결정을 단독 수행하지 않음 |
| Agentic VLA / Rule Guard | 행동 후보 생성과 안전·신뢰도 기반 검증 | 저수준 모터 제어 상세를 포함하지 않음 |
| Navigation | 지도 생성, 위치 추정, 경로 계획, 장애물 회피 | 물체 조작을 수행하지 않음 |
| Manipulation | 쓰레기 수거와 분실물 별도 보관 | 물체 의미 분류를 단독 판단하지 않음 |
| Edge Runtime | 온디바이스 추론과 로봇 런타임 실행 | 서버 학습 파이프라인 세부 구현은 별도 검토 |
| Dashboard / Backend | 작업 요청, Mission Queue, 진행 상태와 전후 결과 표시 | FSM 상태 전이 source of truth는 Mission Manager이며, 구체 API와 데이터 보존 방식은 추가 정의 필요 |

## 5. 가정

- 기획서에는 Jetson AGX Orin 64GB가 기록되어 있으나 selected Decision에 따라 메인 컴퓨팅은 Jetson Orin NX 16GB를 사용한다.
- XLeRobot에 RGB-D, 2D LiDAR, IMU, 매니퓰레이터가 포함되는 것으로 이해한다.
- SLAM과 Nav2는 실내 지도 생성 및 작업 구역 이동에 사용된다.
- MuJoCo와 Isaac Sim은 실제 로봇 실험 전 시뮬레이션 검증에 활용된다.

## 6. 리스크

- 실제 환경에서 쓰레기와 분실물 후보를 안정적으로 구분하지 못할 수 있다.
- 조작 실패, 파지 실패, 충돌 위험이 있다.
- Jetson Orin NX 16GB의 memory budget, 추론 성능과 ROS 2 런타임 통합 병목이 발생할 수 있다.
- 시뮬레이션에서 성공한 정책이 실제 XLeRobot에 그대로 적용되지 않을 수 있다.
- 안전 기준이 아직 상세화되어 있지 않다.

## 7. 관련 결정

- [[30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB|Jetson Orin NX 16GB]]는 `selected` Decision이다.
