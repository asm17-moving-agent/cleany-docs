---
type: decision
decision_type: technical
status: dropped
reviewers:
  - 박창수
tags:
  - decision
  - dropped
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
superseded_by: "30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB.md"
updated: 2026-07-14
---

# 260708 - Jetson AGX Orin 64GB

## 1. 결정

NVIDIA Jetson AGX Orin 64GB를 끌리니의 메인 엣지 컴퓨팅 장치로 사용하는 안은 폐기한다. 메모리 가격 상승에 따른 조달 비용 증가를 이유로 메인 엣지 컴퓨팅 장치는 Jetson Orin NX 16GB로 변경한다.

## 2. 이유

- Raw 요약에는 메인 컴퓨팅으로 NVIDIA Jetson AGX Orin 64GB가 명시되어 있다.
- 엣지 컴퓨팅 선택은 실시간 추론, TensorRT 최적화, ROS 2 실행, 비용, 전력, 발열, 개발환경 호환성에 영향을 준다.
- 프로젝트 검토 시점의 메모리 가격 상승으로 AGX Orin 64GB의 조달 비용 부담이 커졌다.
- Jetson 생태계를 유지하면서 비용을 낮추기 위해 Orin NX 16GB를 대체 장치로 선택했다.

## 3. 대안

| 대안                              | 판단                               |
| ------------------------------- | -------------------------------- |
| Jetson AGX Orin 64GB를 기준 장치로 둔다 | 메모리 가격 상승에 따른 조달 비용 증가로 폐기한다.    |
| Jetson Orin NX 16GB를 기준 장치로 둔다  | 대체 장치로 선택한다.                     |
| 서버 추론 중심으로 둔다                   | 온디바이스 실시간 추론 방향과 맞지 않아 선택하지 않는다. |

## 4. 가정

- 객체 탐지, 위치 추정, 장애물 회피 등 주요 AI 기능은 Orin NX 16GB에서 실시간으로 실행하는 방향이다.
- 서버는 로그 정제와 학습에 활용될 수 있으나 실시간 판단의 필수 의존성으로 확정하지 않는다.
- 모델과 ROS 2 workload는 16GB 메모리 범위에 맞게 구성하고 실제 사용량을 검증한다.

## 5. 리스크

- Orin NX 16GB의 base software stack은 JetPack 6.2로 정했지만 ROS 2와 프로젝트별 Python·AI package 조합은 추가 검증이 필요하다.
- 16GB 메모리에서 동시 실행 workload가 메모리 또는 추론 성능 한계를 넘을 수 있다.
- carrier board, 발열과 전력 구성이 현장 운영 요구를 만족하지 못할 수 있다.

## 6. 재검토 조건

- Orin NX 16GB의 실제 workload benchmark가 데모 요구 수준을 만족하지 못한다.
- 조달 가격이나 공급 조건이 다시 바뀌어 AGX Orin 64GB 또는 다른 장치가 더 적합해진다.

## 7. 출처

- [[40_RAW/20_Planning/기획서 원문 요약|기획서 원문 요약]]
- [NVIDIA JetPack 6.2 Release Notes](https://docs.nvidia.com/jetson/jetpack/6.2/release-notes/index.html)

## 8. 관련 결정

- [[30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB|Jetson Orin NX 16GB]]가 이 안을 대체한다.
