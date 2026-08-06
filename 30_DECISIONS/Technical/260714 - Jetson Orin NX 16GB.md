---
date: 2026-07-14
source_refs:
  - "40_RAW/기획서 원문 요약.md"
supersedes: "30_DECISIONS/Technical/260708 - Jetson AGX Orin 64GB.md"
---

# 260714 - Jetson Orin NX 16GB

## 1. 결정

끌리니의 메인 엣지 컴퓨팅 장치는 NVIDIA Jetson Orin NX 16GB를 사용한다. 기획서에 기록된 Jetson AGX Orin 64GB 안은 폐기하고 이 결정으로 대체한다. 로봇 엣지 런타임은 JetPack 6.2와 ROS 2 Humble을 기준으로 둔다.

## 2. 이유

- 프로젝트 검토 시점의 메모리 가격 상승으로 AGX Orin 64GB의 조달 비용 부담이 커졌다.
- ROS 2, sensor 처리, 로컬 실행 검증과 robot adapter를 로봇에서 실행하는 방향은 유지한다.
- Orin NX 16GB의 base software stack은 JetPack 6.2를 사용한다.
- ROS 2 Humble을 로봇 엣지의 ROS 2 배포판으로 사용한다.
- 실제 AI 모델과 ROS 2 workload가 16GB 메모리에서 목표 성능을 만족하는지는 별도 benchmark로 검증한다.

## 3. 대안

| 대안                   | 판단                                        |
| -------------------- | ----------------------------------------- |
| Jetson Orin NX 16GB  | 비용을 고려한 현재 기준 장치로 선택한다.                   |
| Jetson AGX Orin 64GB | 메모리 가격 상승에 따른 조달 비용 증가로 선택하지 않는다.         |
| 서버 전용 robot runtime | 안전·sensor·hardware integration을 네트워크에 의존하므로 선택하지 않는다. |

## 4. 가정

- ROS 2, sensor 처리, Navigation, 로컬 Perception·VLA adapter와 실행 검증은 Orin에서 수행한다.
- ER 2 같은 cloud Planner를 사용해도 고주기 제어와 안전 정지는 Orin에 남긴다.
- 실제 로컬 AI workload와 node별 memory budget은 후보 adapter를 정한 뒤 측정한다.
- 정확한 carrier board, storage, power mode와 cooling 구성은 추가 확인한다.
- base software stack은 JetPack 6.2, Jetson Linux 36.4.3의 Ubuntu 22.04 기반 root filesystem, CUDA 12.6과 TensorRT 10.3 조합을 사용한다.
- JetPack 6.2와 ROS 2 Humble의 프로젝트별 Python·AI package 조합은 추가 검증한다.

## 5. 리스크

- 16GB 메모리에서 perception, navigation, manipulation과 로컬 VLA adapter를 동시에 실행할 때 메모리 부족이나 성능 저하가 발생할 수 있다.
- JetPack 6.2의 Orin NX 16GB 지원은 확인됐지만, ROS 2 Humble과 프로젝트별 Python·AI package 조합에서 추가 호환성 문제가 발생할 수 있다.
- carrier board, 전원과 방열 구성이 로봇 탑재 및 현장 운영 요구를 만족하지 못할 수 있다.

## 6. 재검토 조건

- 대표 workload benchmark가 목표 latency, 처리량 또는 메모리 사용 기준을 만족하지 못한다.
- 필수 ROS 2 Humble 또는 AI package가 JetPack 6.2 환경에서 지원되지 않는다.
- 조달 가격, 공급 일정 또는 전력·방열 제약으로 다른 장치가 더 적합해진다.

## 7. 출처

- [[40_RAW/기획서 원문 요약|기획서 원문 요약]]
- [NVIDIA JetPack 6.2 Release Notes](https://docs.nvidia.com/jetson/jetpack/6.2/release-notes/index.html)
- [ROS 2 Humble Ubuntu 22.04 arm64 지원](https://docs.ros.org/en/humble/Installation/Alternatives/Ubuntu-Install-Binary.html)

## 8. 관련 결정

- [[30_DECISIONS/Technical/260708 - Jetson AGX Orin 64GB|Jetson AGX Orin 64GB]] 안을 대체한다.
