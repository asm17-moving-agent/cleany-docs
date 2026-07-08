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

## 3. 한 번에 이해하는 작업 흐름

이 KB의 기본 흐름은 `Raw 보존 → 초안 반영 → 질문/Decision 분리 → 검사 → 사람 검토`다.

### 3.1 Raw 보존

새 자료가 들어오면 먼저 `40_RAW`에 둔다. 원문 파일은 가능하면 그대로 보존하고, Office/PDF 파일은 `$office-to-markdown`으로 Markdown 변환본을 만든다.

이 단계에서는 요약, 판단, 결론을 만들지 않는다. 변환 결과는 `review_status: needs-human-review` 또는 `ingest_status`로 아직 검토 전임을 표시한다.

### 3.2 초안 반영

Raw에서 Planning 또는 Decision으로 옮길 내용이 보이면 `$kb-ingest`를 사용한다. 이때 작성자는 다음을 구분한다.

| 구분 | 처리 |
|---|---|
| 기획 범위, 사용자, 가치, 성공 기준 | `10_PLANNING`에 반영 |
| 시스템 개념, 아키텍처, 제약, 리스크 | `20_TECHNICAL`에 반영 |
| 프로젝트 방향이나 Sprint에 영향을 주는 선택 | `30_DECISIONS`에 draft Decision 생성 |
| 확정할 수 없는 내용 | `10_PLANNING/08 - Questions.md`에 질문 추가 |

### 3.3 질문과 Decision 분리

질문은 결론이 아니다. 질문은 팀이 검토해야 할 빈칸이고, Decision은 검토 결과를 추적하는 문서다.

- 질문은 [[10_PLANNING/08 - Questions|Questions]]에 남긴다.
- Decision 후보는 [[30_DECISIONS/00 - Decision Index|Decision Index]]에 남긴다.
- Decision 문서를 만들 때는 `status: draft`, `review_status: needs-human-review`를 유지한다.
- 사람 검토가 끝나기 전에는 `status: selected`로 바꾸지 않는다.

### 3.4 검사와 리뷰

문서를 고친 뒤에는 `$kb-quality-checks`를 실행한다. 이 검사는 구조, formatting, YAML metadata, 내부 링크, repo skill 구조를 확인한다.

검토 준비가 필요하면 `$kb-audit`를 실행한다. 이 리포트는 제품 문서의 `검토 필요`, `추가 확인 필요`, `추가 정의 필요`, Decision inventory, source_refs 상태를 요약한다.

사람 검토 전에 한 번에 볼 패키지가 필요하면 `$kb-review-pack`을 사용한다. 이 skill은 품질 검사, audit, Decision 상태, 미해결 질문, 다음 리뷰 액션을 함께 요약한다.

검사 실패가 단순 형식 문제면 수정한다. 실패가 기획 판단을 요구하면 임의로 고치지 않고 [[10_PLANNING/08 - Questions|Questions]]에 남긴다.

## 4. 실제 상황별 절차

### 4.1 새 원본 자료가 들어오면

1. 원본은 `40_RAW`에 보존한다.
2. Office/PDF 파일은 `$office-to-markdown`으로 변환한다.
3. Raw 요약은 최종 결정으로 취급하지 않는다.
4. 공식 문서에 반영할 후보가 있으면 `$kb-ingest`를 사용한다.
5. 반영 문서에는 `source_refs`를 남긴다.

예시 요청:

```text
$office-to-markdown "40_RAW/00_Inbox/자료.docx"를 Markdown으로 변환해 "40_RAW/20_Planning/자료 원문 변환.md"에 저장해. 요약이나 해석은 하지 마.
```

### 4.2 질문을 발견하면

1. 확정하지 않는다.
2. [[10_PLANNING/08 - Questions|Questions]]에 질문으로 남긴다.
3. 결정이 필요한 질문이면 [[30_DECISIONS/00 - Decision Index|Decision Index]]의 후보와 연결한다.
4. Jira 작업이 필요하면 문서 본문을 복사하지 말고 관련 문서 링크만 둔다.

### 4.3 결정을 내려야 하면

1. 후보가 프로젝트 방향, Sprint, 기술 리스크, 안전 기준에 영향을 주는지 본다.
2. 영향이 크면 Decision 초안을 만든다.
3. 사람 검토 전에는 `status: draft`, `review_status: needs-human-review`를 유지한다.
4. 검토가 끝난 뒤에만 `status: selected`로 승격한다.

예시 요청:

```text
$kb-ingest "40_RAW/10_Meetings/260708 - MVP 범위 회의.md"를 근거로 Planning 반영 후보와 Decision 초안을 만들어.
```

### 4.4 문서를 고쳤으면

1. `$kb-quality-checks`로 구조, metadata, 링크를 확인한다.
2. `$kb-audit`로 검토 플래그와 Decision 상태를 확인한다.
3. 실패 항목이 기획 판단을 요구하면 임의 수정하지 않고 질문으로 남긴다.

예시 요청:

```text
$kb-quality-checks 이 저장소의 전체 결정적 검사를 실행하고 실패 항목을 요약해.
$kb-audit 전체 audit 결과를 요약해.
$kb-review-pack 전체 KB를 사람 검토 전에 점검하고 다음 리뷰 액션을 요약해.
```

## 5. 어디에 무엇을 쓰나

| 위치 | 쓰는 내용 | 쓰지 않는 내용 |
|---|---|---|
| `10_PLANNING` | 문제, 사용자, 범위, 시나리오, 성공 기준 | 하드웨어 상세 구현 |
| `20_TECHNICAL` | 시스템 개념, 아키텍처, 인터페이스, 제약, 리스크 | 시장 narrative 반복 |
| `30_DECISIONS` | 중요한 결정과 이유 | 검토 전 확정 선언 |
| `40_RAW` | 기획서, 회의록, 조사 자료, 멘토 피드백 | 공식 결론 |
| `90_TEMPLATES` | 반복 문서 템플릿 | 프로젝트 고유 사실 |

## 6. 초심자가 자주 헷갈리는 규칙

| 헷갈리는 점 | 기준 |
|---|---|
| Raw에 적혀 있으면 확정인가? | 아니다. Raw는 근거이며 최종 결정이 아니다. |
| draft 문서를 공식 문서처럼 써도 되는가? | 검토 전 초안으로만 다룬다. |
| selected Decision은 누가 만드는가? | 사람 검토 후에만 승격한다. |
| 모르는 내용을 추정해서 채워도 되는가? | 안 된다. `검토 필요` 또는 `추가 확인 필요`로 남긴다. |
| Jira issue에는 무엇을 넣는가? | 문서 본문 복붙이 아니라 관련 문서 링크를 넣는다. |
| 제품 구현 코드를 만들어도 되는가? | 안 된다. 이 저장소는 기획 KB다. |

## 7. 현재 가장 중요한 일

1. 기획서 원문 요약이 원문 의도를 왜곡하지 않았는지 확인한다.
2. MVP 기능 범위를 정한다.
3. 1차 타깃을 무인 스터디카페로 확정할지 정한다.
4. 정량 성공 기준과 안전 기준을 정의한다.
5. Jetson AGX Orin 64GB, XLeRobot, Rule-based VLA 구조를 Decision 후보로 정리한다.

## 8. 기본 원칙

- Raw는 근거지만 최종 결정은 아니다.
- 기획서에 없는 내용을 확정 사실처럼 쓰지 않는다.
- Planning과 Technical을 섞지 않는다.
- 사람 검토 전에는 `review_status: reviewed`로 바꾸지 않는다.
- selected Decision은 사람 검토 후에만 만든다.
