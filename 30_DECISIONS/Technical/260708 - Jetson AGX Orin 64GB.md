---
type: decision
decision_type: technical
status: draft
reviewers:
  -
tags:
  - decision
  - draft
  - technical
  - edge-runtime
  - cleany
date: 2026-07-08
impact: high
source_refs:
  - "40_RAW/20_Planning/기획서 원문 요약.md"
related_jira:
  -
supersedes:
superseded_by:
updated: 2026-07-08
---

# 260708 - Jetson AGX Orin 64GB

## 1. 결정

NVIDIA Jetson AGX Orin 64GB를 끌리니의 메인 엣지 컴퓨팅 장치로 확정할지 검토하는 Technical Decision 초안이다. 사람 검토 전이므로 아직 확정 결정이 아니다.

## 2. 이유

- Raw 요약에는 메인 컴퓨팅으로 NVIDIA Jetson AGX Orin 64GB가 명시되어 있다.
- 엣지 컴퓨팅 선택은 실시간 추론, TensorRT 최적화, ROS 2 실행, 비용, 전력, 발열, 개발환경 호환성에 영향을 준다.
- Ubuntu 26.04 LTS, JetPack 7, ROS 2 조합은 Raw에서도 호환성 검토 필요로 표시되어 있다.

## 3. 대안

| 대안 | 선택하지 않은 이유 |
|---|---|
| Jetson AGX Orin 64GB를 기준 장치로 둔다 | Raw에 명시되어 있으나 실제 버전 호환성과 비용 검토가 필요하다. |
| Jetson Orin NX 등 하위 장치를 검토한다 | 비용과 전력 측면 장점이 있을 수 있으나 Raw 기준 공식 항목은 아니다. |
| 서버 추론 중심으로 둔다 | 온디바이스 실시간 추론 방향과 맞지 않을 수 있다. |

## 4. 가정

- 객체 탐지, 위치 추정, 장애물 회피 등 주요 AI 기능은 Jetson에서 실시간으로 실행하는 방향이다.
- 서버는 로그 정제와 학습에 활용될 수 있으나 실시간 판단의 필수 의존성으로 확정하지 않는다.

## 5. 리스크

- JetPack, CUDA, ROS 2, Python/PyTorch/TensorRT 버전 조합이 실제로 맞지 않을 수 있다.
- 발열, 전력, 비용이 플랫폼 선택에 영향을 줄 수 있다.
- 실시간 추론 성능이 데모 요구 수준을 만족하지 못할 수 있다.

## 6. 재검토 조건

- 실제 호환성 검증에서 Raw의 개발환경 조합이 맞지 않는 것으로 확인된다.
- 모델 후보 벤치마크에서 AGX Orin 64GB가 과하거나 부족하다고 판단된다.
- 비용 또는 전력 제약으로 하위 장치 검토가 필요해진다.

## 7. 출처

- [[40_RAW/20_Planning/기획서 원문 요약|기획서 원문 요약]]
