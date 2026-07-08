---
type: current-status
status: draft
review_status: needs-human-review
tags:
  - start-here
  - current-status
  - cleany
updated: 2026-07-08
---

# 현재 상태(Current Status)

## 1. 현재 프로젝트 단계

- 현재 단계는 기획서 원문 기반 초기 KB scaffold 작성 단계다.
- 세부 스토리보드, 시나리오, 부품 선정 및 아키텍처 결정은 추후 진행한다.

## 2. 현재 기획 상태

- 프로젝트명은 `끌리니(Cleany) : 무인 점포 관리 로봇`으로 확인된다.
- 팀명은 `AI 에이전트는 움직이고 싶어`이며 팀원은 이동근, 박창수, 이정현이다.
- 문제 인식은 무인 점포 및 공간 공유 서비스 확산에 따른 청결, 정돈, 시설 상태 유지 공백이다.
- 1차 타깃은 기획서 기준 무인 스터디카페/공간대여 시설로 고려된다.
- 주요 기능은 쓰레기 자동 수거, 공간 정리/정돈, 자율 주행, 분실물 후보 확인, 책상 닦기, 소등, 문단속, 관제 대시보드다.
- 팀 역할, 멘토 역할, 월별 상세 일정, 수행 방법, 결과물 활용방안 일부는 기획서에 placeholder 또는 빈 항목이 있어 검토 필요다.

## 3. 현재 기술 상태

- 예비 기술 구조는 XLeRobot 기반 모바일 매니퓰레이터, Rule-based VLA, SLAM, ROS 2 Navigation/Nav2, Jetson AGX Orin 64GB, RGB-D, 2D LiDAR, IMU를 중심으로 작성되어 있다.
- 객체 탐지 및 Segmentation, 경량 VLM, 온디바이스 추론, TensorRT 최적화, MuJoCo/Isaac Sim 기반 시뮬레이션이 기획서에 포함되어 있다.
- Ubuntu 22.04 LTS(JetPack 6), Docker, CUDA 등 개발환경 항목은 기획서에 적힌 수준으로만 반영했으며 실제 호환성은 추가 확인 필요다.
- Orin NX 사용 가능성은 현재 기획서 기준 공식 항목이 아니므로 검토 필요 질문으로 남긴다.

## 4. 주요 리스크

- 실제 무인 공간에서 쓰레기, 분실물, 기타 물체를 안정적으로 구분할 수 있는지 검토 필요.
- 로봇 팔로 쓰레기 수거, 정렬, 밀기, 책상 닦기 동작을 안정적으로 수행할 수 있는지 검토 필요.
- SLAM/Nav2 기반 주행 중 장애물 회피와 작업 위치 접근 정밀도 검토 필요.
- Jetson AGX Orin에서 인식, 판단, 주행, 조작 기능을 실시간으로 수행할 수 있는지 검토 필요.
- 소등, 문단속 기능은 물리 인터페이스와 안전 기준이 불명확하여 추가 확인 필요.
- 안전 기준, 평가 지표, 실패 처리 정책이 아직 상세화되지 않았다.

## 5. 미해결 질문

대표 질문은 [[10_PLANNING/08 - Questions|Questions]]에 정리한다.

- MVP 범위와 데모 시나리오는 어디까지인가?
- 무인 스터디카페를 1차 타깃으로 확정할 것인가?
- 정량 성공 기준은 어떻게 정의할 것인가?
- 팀원별 역할과 멘토 역할은 어떻게 정리할 것인가?
- Jetson AGX Orin 64GB를 확정할 것인가, 다른 Orin 계열도 검토할 것인가?
- 관제 대시보드는 MVP에 포함되는가, 데모 placeholder인가?

## 6. 최근 갱신 문서

- [[40_RAW/20_Planning/기획서 원문 요약|기획서 원문 요약]]
- [[10_PLANNING/00 - Project Brief|Project Brief]]
- [[10_PLANNING/02 - Target Scenario|Target Scenario]]
- [[20_TECHNICAL/00 - Technical Overview|Technical Overview]]
- [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]]
- [[30_DECISIONS/00 - Decision Index|Decision Index]]

## 7. 다음 검토 대상

1. 기획서 원문 요약이 원문 의도를 왜곡하지 않았는지 확인.
2. Scope와 Non-Goals가 팀 합의와 맞는지 확인.
3. Success Criteria의 정량 기준 정의.
4. 안전 기준과 실패 처리 정책 정의.
5. Decision 후보 중 selected로 승격할 항목 검토.
