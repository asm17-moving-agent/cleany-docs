---
type: technical
status: draft
reviewers:
  -
tags:
  - technical
  - questions
  - draft
  - cleany
source_refs:
  - "[기획서]"
  - "[ros2_ws/src/cleany_mission_manager/README.md]"
related_decisions:
  - "30_DECISIONS/Planning/260708 - MVP 기능 범위.md"
  - "30_DECISIONS/Technical/260708 - XLeRobot 기반 플랫폼.md"
  - "30_DECISIONS/Technical/260708 - Jetson AGX Orin 64GB.md"
  - "30_DECISIONS/Technical/260708 - Rule-based VLA 3 Layer 구조.md"
  - "30_DECISIONS/Technical/260708 - 안전 기준과 실패 처리 정책.md"
related_jira:
  -
updated: 2026-07-12
---

# 기술 미해결 질문(Technical Questions)

## 1. 요약

이 문서는 시스템 구조, 인터페이스, 하드웨어, 런타임, 데이터, 평가, 안전처럼 기술 판단이 필요한 미해결 질문을 모아두는 목록이다.

## 2. 질문 분류 기준

- 시스템을 어떻게 구성하고 검증할지에 관한 질문은 이 문서에서 관리한다.
- 사용자, 가치, 제품 범위, 시연 구성, 성공 목표처럼 기획 판단이 필요한 질문은 [[10_PLANNING/99 - Questions|Planning Questions]]에서 관리한다.
- 기획과 기술에 걸친 주제는 제품 선택과 기술 구현 경계를 나눠 각각 한 번만 기록한다.

## 3. 관리 규칙

- 질문에 답할 근거가 없으면 내용을 임의로 확정하지 않는다.
- 사실이나 외부 근거 확인이 필요하면 `추가 확인 필요`, 기준·계약·정책 정의가 필요하면 `추가 정의 필요`, 후보 선택이 필요하면 `검토 필요`로 표시한다.
- 기존 문서에 우선순위가 없던 질문은 `미정`으로 유지한다.
- 질문이 해결되면 관련 Technical 또는 Decision 문서에 반영한 뒤 상태를 갱신한다.

## 4. 질문 목록

### 4.1 시스템 경계와 인터페이스

| 질문 | 배경 | 관련 문서 | 우선순위 | 상태 |
|---|---|---|---|---|
| 온디바이스 추론 대상과 서버 학습·처리 대상의 경계는 무엇인가? | 로봇 엣지와 서버의 책임 및 데이터 이동 범위를 정해야 한다. | [[20_TECHNICAL/00 - Technical Overview|Technical Overview]], [[20_TECHNICAL/06 - Edge Runtime Jetson Orin|Edge Runtime Jetson Orin]] | 미정 | 추가 정의 필요 |
| 작업 대상 구역을 어떤 ID, 지도 좌표 또는 UI 영역으로 전달할 것인가? | 대시보드, Mission Manager, Navigator 사이의 대상 지정 계약이 필요하다. | [[20_TECHNICAL/01 - System Concept|System Concept]], [[20_TECHNICAL/05 - Navigation and Mapping|Navigation and Mapping]], [[20_TECHNICAL/09 - Mission Manager FSM|Mission Manager FSM]] | 미정 | 추가 정의 필요 |
| 물체별 집기 실패와 저신뢰 분류를 어떤 결과 코드와 운영자 알림 계약으로 처리할 것인가? | 모듈 결과와 사용자 표시를 연결할 공통 실패 표현이 필요하다. | [[20_TECHNICAL/01 - System Concept|System Concept]], [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]], [[20_TECHNICAL/09 - Mission Manager FSM|Mission Manager FSM]] | 미정 | 추가 정의 필요 |
| Planner의 정확한 `TaskPlan` schema는 무엇인가? | 현재 문서는 실행 가능한 high-level skill sequence만 계약으로 요구하고 상세 schema 확정을 유예했다. | [[20_TECHNICAL/09 - Mission Manager FSM|Mission Manager FSM]] | 미정 | 추가 정의 필요 |
| Skill Executor 내부의 skill breakdown과 입출력 계약은 무엇인가? | 세부 동작 분해는 `cleany_skill_executor` 설계 시 확정하도록 유예됐다. | [[20_TECHNICAL/09 - Mission Manager FSM|Mission Manager FSM]] | 미정 | 추가 정의 필요 |
| Dashboard/backend와 Mission Report를 어떤 방식으로 연동할 것인가? | MVP는 console 또는 file log를 사용하고 외부 연동은 이후로 유예했다. | [[20_TECHNICAL/09 - Mission Manager FSM|Mission Manager FSM]] | 미정 | 검토 필요 |
| `target_pose`, `home_pose`, `priority`, `deadline` 같은 MissionRequest 확장 필드는 언제 어떤 계약으로 추가할 것인가? | MVP 최소 요청 이후의 확장 조건이 정해지지 않았다. | [[20_TECHNICAL/09 - Mission Manager FSM|Mission Manager FSM]] | 미정 | 검토 필요 |

### 4.2 Rule-based VLA와 인식·조작

| 질문 | 배경 | 관련 문서 | 우선순위 | 상태 |
|---|---|---|---|---|
| Rule-based VLA 3 Layer의 공식 명칭과 계층별 책임은 무엇인가? | 기획서에 3 Layer 개념은 있으나 각 계층의 경계가 상세하지 않다. | [[20_TECHNICAL/00 - Technical Overview|Technical Overview]], [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]] | 높음 | 추가 정의 필요 |
| VLA 후보 모델은 무엇이며 경량 VLM과의 관계 및 선정 기준은 무엇인가? | 기획서에는 경량 VLM만 기재되어 있고 실제 후보와 평가 기준이 없다. | [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]] | 중간 | 추가 확인 필요 |
| 객체 탐지·Segmentation 모델 후보와 선정 기준은 무엇인가? | YOLO, MediaPipe 등의 예시가 언급됐지만 채택 모델은 정해지지 않았다. | [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]] | 중간 | 검토 필요 |
| 규칙 기반 검증의 최소 규칙 세트는 무엇인가? | 안전하고 재현 가능한 행동 선택을 위한 기본 규칙이 필요하다. | [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]] | 미정 | 추가 정의 필요 |
| Planning에서 정한 MVP 물체별 집기 정책은 어떻게 정의할 것인가? | 물체 목록과 성공 조건을 실제 행동 규칙으로 변환해야 한다. | [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]], [[10_PLANNING/99 - Questions|Planning Questions]] | 미정 | 추가 정의 필요 |
| 불확실한 물체의 기본 행동과 결과 표현은 무엇인가? | 분실물이나 저신뢰 물체를 건드리지 않는 원칙을 모듈 행동과 결과 코드에 반영해야 한다. | [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]] | 미정 | 추가 정의 필요 |
| grasp estimation 폴백을 실제 MVP에 포함할 것인가? | 규칙 기반 집기 실패를 보완할 후보지만 실제 채택 여부와 인터페이스가 정해지지 않았다. | [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]] | 미정 | 검토 필요 |

### 4.3 로봇 플랫폼과 엣지 런타임

| 질문 | 배경 | 관련 문서 | 우선순위 | 상태 |
|---|---|---|---|---|
| XLeRobot의 정확한 모델, 부품, 센서, 매니퓰레이터, 페이로드, 도달 범위는 무엇인가? | 작업 가능 범위와 안전 제약을 판단할 실제 사양이 필요하다. | [[20_TECHNICAL/04 - Robot Platform XLeRobot|Robot Platform XLeRobot]] | 높음 | 추가 확인 필요 |
| 그리퍼 또는 말단장치 구성은 무엇인가? | 물체별 집기 가능성과 제어 방식을 결정하는 핵심 사양이다. | [[20_TECHNICAL/04 - Robot Platform XLeRobot|Robot Platform XLeRobot]] | 미정 | 추가 확인 필요 |
| 수거함은 로봇에 탑재되는가, 공간 내 고정 위치인가? | 플랫폼 구성과 이동·투입 시나리오가 달라진다. | [[20_TECHNICAL/04 - Robot Platform XLeRobot|Robot Platform XLeRobot]] | 미정 | 검토 필요 |
| 후속 책상 닦기 기능의 도구는 어떤 방식으로 장착할 것인가? | 1차 MVP 제외 후보지만 장기 기능의 플랫폼 제약으로 남아 있다. | [[20_TECHNICAL/04 - Robot Platform XLeRobot|Robot Platform XLeRobot]] | 미정 | 검토 필요 |
| Jetson AGX Orin 64GB를 기준 엣지 플랫폼으로 확정할 것인가? | 기획서에 명시되어 있으나 아직 selected Decision이 아니다. | [[20_TECHNICAL/06 - Edge Runtime Jetson Orin|Edge Runtime Jetson Orin]] | 높음 | 검토 필요 |
| Orin NX 등 다른 Jetson 계열을 대안으로 검토할 것인가? | 현재 기획서 기준 공식 항목은 아니지만 대안 검토 가능성이 언급됐다. | [[20_TECHNICAL/06 - Edge Runtime Jetson Orin|Edge Runtime Jetson Orin]] | 중간 | 검토 필요 |
| Ubuntu 26.04 LTS(JetPack 7)와 ROS 2 조합은 실제 사용 가능한가? | 개발환경 표의 버전 조합에 대한 실제 호환성 검증이 필요하다. | [[20_TECHNICAL/06 - Edge Runtime Jetson Orin|Edge Runtime Jetson Orin]] | 높음 | 추가 확인 필요 |

### 4.4 내비게이션, 데이터, 평가

| 질문 | 배경 | 관련 문서 | 우선순위 | 상태 |
|---|---|---|---|---|
| 지도 생성은 수동 사전 매핑, 로봇 초기 캘리브레이션, 또는 둘의 조합 중 무엇인가? | 현장 준비 절차와 운영 부담을 결정해야 한다. | [[20_TECHNICAL/05 - Navigation and Mapping|Navigation and Mapping]] | 미정 | 검토 필요 |
| 사전 지도와 현장 환경의 차이를 어느 수준까지 허용할 수 있는가? | 가구 이동이나 배치 변경에 대한 내비게이션 허용 오차가 필요하다. | [[20_TECHNICAL/05 - Navigation and Mapping|Navigation and Mapping]] | 미정 | 추가 정의 필요 |
| Navigator 내부 mock seat map 형식은 무엇인가? | 현재 MVP 문서는 형식 확정을 구현 단계로 유예했다. | [[20_TECHNICAL/05 - Navigation and Mapping|Navigation and Mapping]], [[20_TECHNICAL/09 - Mission Manager FSM|Mission Manager FSM]] | 미정 | 추가 정의 필요 |
| 최소 데이터셋 범위와 라벨 기준은 무엇인가? | 모델 학습과 평가에 사용할 데이터 기준이 없다. | [[20_TECHNICAL/07 - Data and Evaluation|Data and Evaluation]] | 미정 | 추가 정의 필요 |
| 시뮬레이션으로 검증할 시나리오와 실제 테스트로 검증할 시나리오는 어떻게 나눌 것인가? | 각 환경에서 검증 가능한 기술 항목과 전이 기준을 정해야 한다. | [[20_TECHNICAL/07 - Data and Evaluation|Data and Evaluation]] | 미정 | 추가 정의 필요 |
| 현장 데이터 수집 시 개인정보 또는 보안 이슈를 어떻게 처리할 것인가? | 카메라 기반 데이터에 사용자나 민감 정보가 포함될 수 있다. | [[20_TECHNICAL/06 - Edge Runtime Jetson Orin|Edge Runtime Jetson Orin]], [[20_TECHNICAL/07 - Data and Evaluation|Data and Evaluation]], [[20_TECHNICAL/08 - Safety and Risk|Safety and Risk]] | 미정 | 추가 확인 필요 |

### 4.5 안전과 실패 처리

| 질문 | 배경 | 관련 문서 | 우선순위 | 상태 |
|---|---|---|---|---|
| 장애물 회피, 사람 감지, 충돌 위험에서 로봇이 반드시 정지해야 하는 조건은 무엇인가? | 실내 이동·조작 로봇의 최소 안전 기준이 필요하다. | [[20_TECHNICAL/08 - Safety and Risk|Safety and Risk]] | 높음 | 추가 정의 필요 |
| 조작 실패, 파지 실패, 오분류 시 재시도·중단·보고 정책은 무엇인가? | 쓰레기와 분실물 처리 오류가 사용자 자산과 데모 안정성에 영향을 준다. | [[20_TECHNICAL/01 - System Concept|System Concept]], [[20_TECHNICAL/08 - Safety and Risk|Safety and Risk]], [[20_TECHNICAL/09 - Mission Manager FSM|Mission Manager FSM]] | 높음 | 추가 정의 필요 |
| 후속 소등·문단속 기능은 물리 조작, IoT 연동, 상태 확인 중 무엇이며 안전·법적 기준은 무엇인가? | 시설 상태를 변경하는 방식에 따라 기술 경계와 책임이 달라진다. | [[20_TECHNICAL/04 - Robot Platform XLeRobot|Robot Platform XLeRobot]], [[20_TECHNICAL/08 - Safety and Risk|Safety and Risk]] | 높음 | 추가 확인 필요 |
| 안전 평가 시나리오와 통과 기준은 무엇인가? | 정지, 회피, 실패 처리 정책을 검증할 수 있는 기준이 필요하다. | [[20_TECHNICAL/07 - Data and Evaluation|Data and Evaluation]], [[20_TECHNICAL/08 - Safety and Risk|Safety and Risk]] | 미정 | 추가 정의 필요 |
| 독립 Safety Supervisor 또는 Safety Guardrail은 어떤 조건에서 도입할 것인가? | MVP에서는 각 모듈의 기본 safety check만 사용하고 독립 컴포넌트는 유예했다. | [[20_TECHNICAL/09 - Mission Manager FSM|Mission Manager FSM]] | 미정 | 검토 필요 |

## 5. 관련 결정

- 현재 selected Decision 없음.
- 아래 draft Decision은 검토용 초안이며 아직 selected Decision이 아니다.
  - [[30_DECISIONS/Planning/260708 - MVP 기능 범위|MVP 기능 범위]]
  - [[30_DECISIONS/Technical/260708 - XLeRobot 기반 플랫폼|XLeRobot 기반 플랫폼]]
  - [[30_DECISIONS/Technical/260708 - Jetson AGX Orin 64GB|Jetson AGX Orin 64GB]]
  - [[30_DECISIONS/Technical/260708 - Rule-based VLA 3 Layer 구조|Rule-based VLA 3 Layer 구조]]
  - [[30_DECISIONS/Technical/260708 - 안전 기준과 실패 처리 정책|안전 기준과 실패 처리 정책]]
