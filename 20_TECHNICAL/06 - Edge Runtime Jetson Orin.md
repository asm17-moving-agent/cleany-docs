---
type: technical
status: draft
review_status: needs-human-review
tags:
  - technical
  - draft
  - needs-human-review
  - cleany
source_refs:
  - "[기획서]"
related_decisions:
  -
related_jira:
  -
updated: 2026-07-08
---

# Jetson Orin 엣지 런타임

## 1. 요약

기획서에는 Jetson AGX Orin 64GB가 메인 컴퓨팅 장치로 명시되어 있다. 이 문서는 온디바이스 추론, TensorRT 최적화, Docker, CUDA, JetPack 환경을 예비 기술 관점에서 정리한다.

## 2. 기획 맥락

끌리니는 무인 공간에서 실시간으로 객체 탐지, 위치 추정, 장애물 회피, 행동 판단을 수행해야 한다. 외부 서버 의존도가 높으면 지연, 네트워크 장애, 현장 운영 안정성 문제가 생길 수 있으므로 온디바이스 추론이 기획서에 포함되어 있다.

## 3. 기술 개념

### 3.1 기획서 기준 개발환경

| 구분 | 항목 | 기획서 내용 | 상태 |
|---|---|---|---|
| OS | Robot Edge, Server, Training Server | Ubuntu 26.04 LTS(JetPack 7), Docker, CUDA | 기획서 기반, 실제 호환성 검토 필요 |
| 개발도구 | IDE | VS Code | 기획서 기반 |
| 협업/CI | GitHub, GitHub Actions, Github Projects | 문서에는 GitHub Projects 표기로 기재 | 기획서 기반 |
| 로봇 개발환경 | ROS 2, LeRobot, MuJoCo, Isaac Sim | 원문 표기 `Mujoco`, `IssacSim` 포함 | 표기 검토 필요 |
| 개발언어 | 로봇 미들웨어 | C++(ROS 2) | 기획서 기반 |
| 개발언어 | AI 추론 | Python(PyTorch, OpenCV, TensorRT) | 기획서 기반 |
| HW | 메인 컴퓨팅 | NVIDIA Jetson AGX Orin 64GB | 기획서 기반 |

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
| Jetson AGX Orin | 온디바이스 추론 및 로봇 런타임 실행 | 학습 서버 전체 역할을 대체하지 않음 |
| TensorRT | 모델 추론 최적화 | 모델 품질 자체를 보장하지 않음 |
| Docker/CUDA/JetPack | 실행 환경 구성 | 실제 버전 호환성은 검토 필요 |
| ROS 2 Runtime | 센서, 주행, 조작 노드 실행 | Jira/문서 운영과 무관 |
| Training Server | 로그 정제와 학습 가능성 | 기획서에 상세 구조 없음 |

## 5. 가정

- 현재 KB는 기획서 기준으로 Jetson AGX Orin 64GB를 우선 기록한다.
- Orin NX는 현재 기획서 기준 공식 항목이 아니므로 검토 필요 질문으로만 남긴다.
- 온디바이스 추론 대상 모델은 경량화와 TensorRT 최적화가 필요할 수 있다.

## 6. 리스크

- 실제 JetPack, CUDA, Ubuntu, ROS 2 버전 조합이 맞지 않을 수 있다.
- 객체 탐지, VLA 판단, Nav2, 조작 제어를 동시에 실행할 때 성능 병목이 생길 수 있다.
- 발열, 전력, 메모리 사용량이 현장 운영 안정성에 영향을 줄 수 있다.

## 7. 관련 결정

- 현재 selected Decision 없음.
- Jetson AGX Orin 64GB 확정 여부는 Technical Decision 후보다.

## 8. 미해결 질문

- Jetson AGX Orin 64GB를 확정할 것인가?
- Orin NX 등 다른 Jetson 계열을 대안으로 검토할 것인가?
- Ubuntu 26.04 LTS(JetPack 7)와 ROS 2 조합은 실제 사용 가능한가?
- 온디바이스에서 실행할 모델과 서버에서 처리할 학습 작업의 경계는 무엇인가?
