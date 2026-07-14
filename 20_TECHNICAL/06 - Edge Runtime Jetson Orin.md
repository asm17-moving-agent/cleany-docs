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
  - "30_DECISIONS/Technical/260708 - Jetson AGX Orin 64GB.md"
  - "30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB.md"
related_jira:
  -
updated: 2026-07-14
---

# Jetson Orin 엣지 런타임

## 1. 요약

기획서에는 Jetson AGX Orin 64GB가 메인 컴퓨팅 장치로 명시되어 있으나, selected Decision에 따라 현재 기준 장치는 Jetson Orin NX 16GB다. 이 문서는 온디바이스 추론, TensorRT 최적화, Docker, CUDA, JetPack 환경을 예비 기술 관점에서 정리한다.

## 2. 기획 맥락

끌리니는 무인 공간에서 실시간으로 객체 탐지, 위치 추정, 장애물 회피, 행동 판단을 수행해야 한다. 외부 서버 의존도가 높으면 지연, 네트워크 장애, 현장 운영 안정성 문제가 생길 수 있으므로 온디바이스 추론이 기획서에 포함되어 있다.

## 3. 기술 개념

### 3.1 기획서 및 Decision 기준 개발환경

| 구분 | 항목 | 현재 기준 | 상태 |
|---|---|---|---|
| OS | Robot Edge | JetPack 6.2, Jetson Linux 36.4.3, Ubuntu 22.04 기반 root filesystem | selected Decision, Orin NX 16GB 지원 확인 |
| Compute runtime | Robot Edge | CUDA 12.6, TensorRT 10.3, cuDNN 9.3 | JetPack 6.2 공식 구성 |
| ROS 2 | Robot Edge | ROS 2 Humble 후보 | Ubuntu 22.04 arm64 공식 지원, 채택은 추가 검토 필요 |
| OS | Server, Training Server | Ubuntu 26.04 LTS, Docker, CUDA | 기획서 기반, 실제 호환성 검토 필요 |
| 개발도구 | IDE | VS Code | 기획서 기반 |
| 협업/CI | GitHub, GitHub Actions, Github Projects | 문서에는 GitHub Projects 표기로 기재 | 기획서 기반 |
| 로봇 개발환경 | ROS 2, LeRobot, MuJoCo, Isaac Sim | 원문 표기 `Mujoco`, `IssacSim` 포함 | 표기 검토 필요 |
| 개발언어 | 로봇 미들웨어 | C++(ROS 2) | 기획서 기반 |
| 개발언어 | AI 추론 | Python(PyTorch, OpenCV, TensorRT) | 기획서 기반 |
| HW | 메인 컴퓨팅 | NVIDIA Jetson Orin NX 16GB | selected Decision, 기획서의 AGX Orin 64GB 대체 |

### 3.2 온디바이스 추론 역할

- 객체 탐지 및 Segmentation
- 위치 추정
- 장애물 회피 관련 인식
- 경량 VLM 또는 VLA 판단 보조
- TensorRT 기반 추론 최적화

### 3.3 서버와의 관계 초안

기획서에는 서버 로그 정제 및 학습이 언급되어 있다. 따라서 초기 이해는 다음과 같다.

- 로봇 엣지: 실시간 추론과 작업 실행
- 서버/학습 환경: 로그 정제, 데이터 학습, 모델 개선
- 구체 데이터 업로드 방식과 개인정보/보안 정책은 추가 확인 필요

## 4. 인터페이스 / 경계

| 구성요소 | 책임 | 경계 |
|---|---|---|
| Jetson Orin NX 16GB | 온디바이스 추론 및 로봇 런타임 실행 | 학습 서버 전체 역할을 대체하지 않음 |
| TensorRT | 모델 추론 최적화 | 모델 품질 자체를 보장하지 않음 |
| Docker/CUDA/JetPack | 실행 환경 구성 | 실제 버전 호환성은 검토 필요 |
| ROS 2 Runtime | 센서, 주행, 조작 노드 실행 | Jira/문서 운영과 무관 |
| Training Server | 로그 정제와 학습 가능성 | 기획서에 상세 구조 없음 |

## 5. 가정

- 메인 엣지 컴퓨팅 장치는 selected Decision에 따라 Jetson Orin NX 16GB를 사용한다.
- Orin NX 16GB의 base software stack은 JetPack 6.2를 사용한다.
- 온디바이스 추론 대상 모델은 경량화와 TensorRT 최적화가 필요할 수 있다.
- perception, navigation, manipulation과 AI 추론의 동시 실행 memory budget은 benchmark로 검증한다.
- ROS 2 Humble은 Ubuntu 22.04 arm64 호환 후보지만 프로젝트의 ROS 2 배포판으로 아직 확정하지 않는다.

## 6. 리스크

- JetPack 6.2 base stack 지원은 확인됐지만 ROS 2 배포판과 프로젝트별 Python·AI package 조합이 맞지 않을 수 있다.
- 객체 탐지, VLA 판단, Nav2, 조작 제어를 동시에 실행할 때 성능 병목이 생길 수 있다.
- 16GB memory budget, 발열과 전력 사용량이 현장 운영 안정성에 영향을 줄 수 있다.

## 7. 관련 결정

- [[30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB|Jetson Orin NX 16GB]]는 `selected` Decision이다.
- [[30_DECISIONS/Technical/260708 - Jetson AGX Orin 64GB|Jetson AGX Orin 64GB]] 안은 메모리 가격 상승에 따른 조달 비용 증가로 `dropped`됐다.

## 8. 참고 근거

- [NVIDIA JetPack 6.2 Release Notes](https://docs.nvidia.com/jetson/jetpack/6.2/release-notes/index.html)
- [ROS 2 Humble Ubuntu 22.04 arm64 지원](https://docs.ros.org/en/humble/Installation/Alternatives/Ubuntu-Install-Binary.html)
