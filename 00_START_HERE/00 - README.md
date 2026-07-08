---
type: start-here
status: draft
review_status: needs-human-review
tags:
  - start-here
  - cleany
updated: 2026-07-08
---

# 끌리니(Cleany) 기획 KB 시작하기

## 1. 이 문서는 무엇인가

이 KB는 끌리니 프로젝트의 기획, 예비설계, 결정, 원본 기록을 한곳에서 추적하기 위한 작업 공간이다. 구현 코드 저장소가 아니라, 팀원이 같은 근거를 보고 같은 질문을 닫아가기 위한 문서 저장소다.

끌리니는 무인 점포 및 공간 대여 시설의 이용 후 정리·점검 업무를 자동화하기 위한 XLeRobot 기반 관리 로봇 프로젝트다.

## 2. 처음 온 사람이 할 일

1. [[00_START_HERE/02 - Current Status|Current Status]]에서 현재 단계와 막힌 질문을 확인한다.
2. [[00_START_HERE/01 - Reading Guide|Reading Guide]]에서 내 목적에 맞는 읽기 순서를 고른다.
3. [[10_PLANNING/00 - Project Brief|Project Brief]]로 프로젝트 목적을 확인한다.
4. [[10_PLANNING/08 - Questions|Questions]]에서 아직 확정되지 않은 항목을 본다.
5. [[30_DECISIONS/00 - Decision Index|Decision Index]]에서 결정 후보와 selected Decision 여부를 확인한다.

현재 KB는 초기 scaffold 상태다. 공식 확정보다 검토 대기 항목이 더 많으므로, 문서를 읽을 때 `draft`, `needs-human-review`, `검토 필요`, `추가 확인 필요` 표시를 반드시 함께 본다.

## 3. 작업 흐름

### 3.1 원본 자료가 들어오면

1. 원본은 `40_RAW`에 보존한다.
2. Office/PDF 파일은 `$office-to-markdown`으로 변환한다.
3. Raw 요약은 최종 결정으로 취급하지 않는다.
4. 공식 문서에 반영할 후보가 있으면 `$kb-ingest`를 사용한다.
5. 반영 문서에는 `source_refs`를 남긴다.

### 3.2 질문을 발견하면

1. 확정하지 않는다.
2. [[10_PLANNING/08 - Questions|Questions]]에 질문으로 남긴다.
3. 결정이 필요한 질문이면 [[30_DECISIONS/00 - Decision Index|Decision Index]]의 후보와 연결한다.
4. Jira 작업이 필요하면 문서 본문을 복사하지 말고 관련 문서 링크만 둔다.

### 3.3 결정을 내려야 하면

1. 후보가 프로젝트 방향, Sprint, 기술 리스크, 안전 기준에 영향을 주는지 본다.
2. 영향이 크면 Decision 초안을 만든다.
3. 사람 검토 전에는 `status: draft`, `review_status: needs-human-review`를 유지한다.
4. 검토가 끝난 뒤에만 `status: selected`로 승격한다.

### 3.4 문서를 고쳤으면

1. `$kb-quality-checks`로 구조, metadata, 링크를 확인한다.
2. `$kb-audit`로 검토 플래그와 Decision 상태를 확인한다.
3. 실패 항목이 기획 판단을 요구하면 임의 수정하지 않고 질문으로 남긴다.

## 4. 어디에 무엇을 쓰나

| 위치 | 쓰는 내용 | 쓰지 않는 내용 |
|---|---|---|
| `10_PLANNING` | 문제, 사용자, 범위, 시나리오, 성공 기준 | 하드웨어 상세 구현 |
| `20_TECHNICAL` | 시스템 개념, 아키텍처, 인터페이스, 제약, 리스크 | 시장 narrative 반복 |
| `30_DECISIONS` | 중요한 결정과 이유 | 검토 전 확정 선언 |
| `40_RAW` | 기획서, 회의록, 조사 자료, 멘토 피드백 | 공식 결론 |
| `90_TEMPLATES` | 반복 문서 템플릿 | 프로젝트 고유 사실 |

## 5. 현재 가장 중요한 일

1. 기획서 원문 요약이 원문 의도를 왜곡하지 않았는지 확인한다.
2. MVP 기능 범위를 정한다.
3. 1차 타깃을 무인 스터디카페로 확정할지 정한다.
4. 정량 성공 기준과 안전 기준을 정의한다.
5. Jetson AGX Orin 64GB, XLeRobot, Rule-based VLA 구조를 Decision 후보로 정리한다.

## 6. 기본 원칙

- Raw는 근거지만 최종 결정은 아니다.
- 기획서에 없는 내용을 확정 사실처럼 쓰지 않는다.
- Planning과 Technical을 섞지 않는다.
- 사람 검토 전에는 `review_status: reviewed`로 바꾸지 않는다.
- selected Decision은 사람 검토 후에만 만든다.
