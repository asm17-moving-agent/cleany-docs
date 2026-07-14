---
type: decision
decision_type: technical
status: selected
reviewers:
  - 박창수
tags:
  - decision
  - technical
  - edge-runtime
  - jetson
  - orin-nx
date: 2026-07-14
impact: high
source_refs:
  - "40_RAW/20_Planning/기획서 원문 요약.md"
related_jira:
  -
supersedes: "30_DECISIONS/Technical/260708 - Jetson AGX Orin 64GB.md"
superseded_by:
updated: 2026-07-14
---

# 260714 - Jetson Orin NX 16GB

## 1. 결정

끌리니의 메인 엣지 컴퓨팅 장치는 NVIDIA Jetson Orin NX 16GB를 사용한다. 기획서에 기록된 Jetson AGX Orin 64GB 안은 폐기하고 이 결정으로 대체한다.

## 2. 이유

- 프로젝트 검토 시점의 메모리 가격 상승으로 AGX Orin 64GB의 조달 비용 부담이 커졌다.
- Jetson 기반 온디바이스 추론과 ROS 2 runtime 방향은 유지한다.
- Orin NX 16GB의 base software stack은 JetPack 6.2를 사용한다.
- 실제 AI 모델과 ROS 2 workload가 16GB 메모리에서 목표 성능을 만족하는지는 별도 benchmark로 검증한다.

## 3. 대안

| 대안                   | 판단                                        |
| -------------------- | ----------------------------------------- |
| Jetson Orin NX 16GB  | 비용을 고려한 현재 기준 장치로 선택한다.                   |
| Jetson AGX Orin 64GB | 메모리 가격 상승에 따른 조달 비용 증가로 선택하지 않는다.         |
| 서버 추론 중심 구성          | 네트워크를 실시간 판단의 필수 의존성으로 두지 않기 위해 선택하지 않는다. |

## 4. 가정

- 객체 탐지, 위치 추정, 장애물 회피와 경량 VLM/VLA 추론은 Orin NX 16GB에서 실행하는 방향이다.
- 모델 경량화, TensorRT 최적화와 node별 memory budget을 적용할 수 있다고 가정한다.
- 정확한 carrier board, storage, power mode와 cooling 구성은 추가 확인한다.
- base software stack은 JetPack 6.2, Jetson Linux 36.4.3의 Ubuntu 22.04 기반 root filesystem, CUDA 12.6과 TensorRT 10.3 조합을 사용한다.
- ROS 2 배포판과 프로젝트 package 조합은 추가 확인한다. Ubuntu 22.04 arm64를 공식 지원하는 ROS 2 Humble은 호환 후보지만 이 Decision에서 채택하지 않는다.

## 5. 리스크

- 16GB 메모리에서 perception, navigation, manipulation과 AI 추론을 동시에 실행할 때 메모리 부족이나 성능 저하가 발생할 수 있다.
- JetPack 6.2의 Orin NX 16GB 지원은 확인됐지만, 선택할 ROS 2 배포판과 프로젝트별 Python·AI package 조합에서 추가 호환성 문제가 발생할 수 있다.
- carrier board, 전원과 방열 구성이 로봇 탑재 및 현장 운영 요구를 만족하지 못할 수 있다.

## 6. 재검토 조건

- 대표 workload benchmark가 목표 latency, 처리량 또는 메모리 사용 기준을 만족하지 못한다.
- 필수 ROS 2 또는 AI package가 JetPack 6.2 환경에서 지원되지 않는다.
- 조달 가격, 공급 일정 또는 전력·방열 제약으로 다른 장치가 더 적합해진다.

## 7. 출처

- [[40_RAW/20_Planning/기획서 원문 요약|기획서 원문 요약]]
- [NVIDIA JetPack 6.2 Release Notes](https://docs.nvidia.com/jetson/jetpack/6.2/release-notes/index.html)
- [ROS 2 Humble Ubuntu 22.04 arm64 지원](https://docs.ros.org/en/humble/Installation/Alternatives/Ubuntu-Install-Binary.html)

## 8. 관련 결정

- [[30_DECISIONS/Technical/260708 - Jetson AGX Orin 64GB|Jetson AGX Orin 64GB]] 안을 대체한다.
