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

## 1. 한 줄 상태

현재 KB는 기획서 원문을 바탕으로 만든 초기 scaffold다. 다음 단계는 새 문서를 늘리는 것이 아니라, 핵심 질문을 사람 검토로 닫고 필요한 항목을 Decision 초안으로 분리하는 것이다.

## 2. 지금 확실한 것

- 프로젝트명은 `끌리니(Cleany) : 무인 점포 관리 로봇`이다.
- 팀명은 `AI 에이전트는 움직이고 싶어`이며 팀원은 이동근, 박창수, 이정현이다.
- 문제 인식은 무인 점포 및 공간 공유 서비스 확산에 따른 청결, 정돈, 시설 상태 유지 공백이다.
- 기획서 기준 1차 타깃은 무인 스터디카페/공간대여 시설로 고려된다.
- 예비 기술 구조는 XLeRobot 기반 모바일 매니퓰레이터, Rule-based VLA, SLAM/Nav2, Jetson AGX Orin 64GB, RGB-D, 2D LiDAR, IMU를 중심으로 작성되어 있다.

## 3. 아직 확정하면 안 되는 것

- MVP 기능 범위
- 관제 대시보드의 MVP 포함 여부
- 책상 닦기, 소등, 문단속의 실제 수행 방식
- 팀원별 역할, 멘토 역할, 월별 추진 일정
- 정량 성공 기준과 평가 목표값
- 안전 기준과 실패 처리 정책
- Jetson/ROS/JetPack 조합의 실제 호환성
- XLeRobot의 정확한 센서, 페이로드, 매니퓰레이터 사양

## 4. 다음 회의에서 닫아야 할 질문

1. MVP 데모는 쓰레기 수거, 공간 정리, 자율주행, 점검 중 어디까지 보여줄 것인가?
2. 1차 타깃을 무인 스터디카페로 확정할 것인가?
3. 관제 대시보드는 MVP에 넣을 것인가, 향후 확장으로 둘 것인가?
4. 정량 성공 기준은 어떤 지표와 목표값으로 둘 것인가?
5. 안전 기준과 실패 처리 정책은 최소 어디까지 정의할 것인가?
6. Jetson AGX Orin 64GB와 XLeRobot을 기준 플랫폼으로 확정할 것인가?

전체 질문은 [[10_PLANNING/08 - Questions|Questions]]에서 관리한다.

## 5. 지금 문서를 고친다면

- 기획 범위를 좁히는 내용은 [[10_PLANNING/04 - Scope and Non-Goals|Scope and Non-Goals]]와 [[10_PLANNING/05 - Success Criteria|Success Criteria]]에 반영한다.
- 기술 전제를 바꾸는 내용은 `20_TECHNICAL` 문서에 반영한다.
- 프로젝트 방향, Sprint, 안전, 기술 리스크에 영향이 큰 선택은 [[30_DECISIONS/00 - Decision Index|Decision Index]]에 후보로 남긴다.
- 근거가 Raw에만 있으면 `source_refs`를 갱신하고 `review_status: needs-human-review`를 유지한다.

## 6. 최근 기준 문서

- [[40_RAW/20_Planning/기획서 원문 요약|기획서 원문 요약]]
- [[10_PLANNING/00 - Project Brief|Project Brief]]
- [[10_PLANNING/02 - Target Scenario|Target Scenario]]
- [[10_PLANNING/04 - Scope and Non-Goals|Scope and Non-Goals]]
- [[10_PLANNING/05 - Success Criteria|Success Criteria]]
- [[20_TECHNICAL/00 - Technical Overview|Technical Overview]]
- [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]]
- [[20_TECHNICAL/08 - Safety and Risk|Safety and Risk]]
- [[30_DECISIONS/00 - Decision Index|Decision Index]]

## 7. 작업 전 확인

문서를 수정하기 전에는 이 문서의 “아직 확정하면 안 되는 것”을 확인한다. 문서를 수정한 뒤에는 `$kb-quality-checks`를 실행하고, 검토 플래그가 필요한 경우 `$kb-audit`로 요약한다.
