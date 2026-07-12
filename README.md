# 끌리니(Cleany) 기획 KB

끌리니(Cleany)는 무인 점포와 공간 대여 시설의 이용 후 정리·점검 업무를 자동화하기 위한 XLeRobot 기반 관리 로봇 프로젝트입니다.

이 저장소는 구현 레포가 아닙니다. 팀원이 기획서, 회의록, 조사 자료, 의사결정 기록을 함께 관리하는 **기획/예비설계 중심 Markdown KB**입니다.

## 먼저 할 일

처음 들어왔다면 아래 순서로 보면 됩니다.

1. 전체 맥락을 잡는다: [00_START_HERE/00 - README.md](00_START_HERE/00%20-%20README.md)
2. 내 역할에 맞는 읽기 순서를 고른다: [00_START_HERE/01 - Reading Guide.md](00_START_HERE/01%20-%20Reading%20Guide.md)
3. 막힌 질문을 확인한다: [Planning Questions](10_PLANNING/99%20-%20Questions.md), [Technical Questions](20_TECHNICAL/99%20-%20Questions.md)
4. 결정 후보를 확인한다: [30_DECISIONS/00 - Decision Index.md](30_DECISIONS/00%20-%20Decision%20Index.md)

현재 가장 중요한 일은 문서를 더 많이 만드는 것이 아니라, 두 `Questions` 문서에 쌓인 핵심 질문을 사람 검토로 닫고 필요한 항목을 Decision 초안으로 남기는 것입니다.

## 처음 작업하는 사람을 위한 10분 흐름

이 저장소에서 가장 먼저 구분해야 할 것은 `근거`, `초안`, `결정`입니다.

1. `40_RAW`는 근거입니다. 원문, 회의록, 조사 자료를 해석 없이 보존합니다.
2. `10_PLANNING`과 `20_TECHNICAL`은 검토 가능한 공식 문서 초안입니다. 대부분 `draft` 상태이며, 검토가 끝나면 reviewer와 함께 `reviewed`로 바꿉니다.
3. `30_DECISIONS`는 중요한 선택을 따로 추적하는 곳입니다. `selected`가 아니면 아직 확정 결정이 아닙니다.
4. 불확실한 내용은 바로 결론으로 쓰지 않고 기획 질문은 `10_PLANNING/99 - Questions.md`, 기술 질문은 `20_TECHNICAL/99 - Questions.md`에 남깁니다.
5. 문서를 고친 뒤에는 `$kb-quality-checks`로 깨진 구조와 링크를 확인합니다.

작업할 때는 아래 질문으로 시작하면 됩니다.

| 내가 하려는 일 | 먼저 볼 곳 | 사용할 흐름 |
|---|---|---|
| 새 파일을 받았다 | `40_RAW/00_Inbox` | `$office-to-markdown` 후 `$kb-ingest` |
| 기획 범위를 정리한다 | `10_PLANNING/04 - Scope and Non-Goals.md` | 근거 확인 후 draft 유지 |
| 기술 전제를 정리한다 | `20_TECHNICAL/00 - Technical Overview.md` | Planning과 섞지 않기 |
| 중요한 선택을 남긴다 | `30_DECISIONS/00 - Decision Index.md` | Decision 후보 또는 draft 생성 |
| 무엇이 막혔는지 본다 | `10_PLANNING/99 - Questions.md`, `20_TECHNICAL/99 - Questions.md` | 계층별 질문 상태 갱신 |
| 공유 전 점검한다 | `00_START_HERE/01 - Reading Guide.md` | `$kb-quality-checks`, `$kb-audit`, `$kb-review-pack` |

## 자주 하는 작업

### 새 자료를 받았을 때

1. 원본 파일을 `40_RAW` 아래에 둡니다.
2. 원본을 해석 없이 보존합니다.
3. Office/PDF 파일이면 `$office-to-markdown`으로 Markdown 변환을 요청합니다.
4. Planning 또는 Decision으로 반영해야 하면 `$kb-ingest`를 사용합니다.
5. 반영 후 `source_refs`, `related_decisions`, `related_jira`를 갱신합니다.

### 기획 내용을 정리할 때

1. 문제, 사용자, 가치, 범위, 시나리오는 `10_PLANNING`에 둡니다.
2. 근거가 Raw에만 있으면 확정처럼 쓰지 않습니다.
3. 불확실한 내용은 `검토 필요` 또는 `추가 확인 필요`로 남깁니다.
4. 핵심 판단이 필요하면 [Planning Questions](10_PLANNING/99%20-%20Questions.md)에 질문으로 남깁니다.

### 기술 내용을 정리할 때

1. 시스템 개념, 아키텍처, 인터페이스, 제약, 리스크는 `20_TECHNICAL`에 둡니다.
2. 실제 구현 코드, 빌드 설정, 배포 설정은 만들지 않습니다.
3. 하드웨어·런타임·모델 후보는 기획서에 적힌 수준과 추가 확인 필요 항목을 구분합니다.
4. 기술 판단이 필요하면 [Technical Questions](20_TECHNICAL/99%20-%20Questions.md)에 질문으로 남깁니다.

### 결정을 남길 때

1. 중요한 선택지는 먼저 [30_DECISIONS/00 - Decision Index.md](30_DECISIONS/00%20-%20Decision%20Index.md)에 후보로 둡니다.
2. 결정의 영향이 크면 `$kb-ingest` 또는 Decision 템플릿으로 초안을 만듭니다.
3. 사람 검토 전에는 `status: draft`와 빈 `reviewers`를 유지합니다. 검토가 끝나면 reviewer를 기록하고 `reviewed` 또는 `selected`로 바꿉니다.
4. `selected` Decision은 사람 검토 후에만 만듭니다.

### 문서 수정 후

1. `$kb-quality-checks`로 구조, formatting, metadata, 링크를 확인합니다.
2. `$kb-audit`로 검토 플래그와 Decision 상태를 요약합니다.
3. 실패 항목이 판단을 요구하면 기획 항목은 Planning Questions, 기술 항목은 Technical Questions에 남깁니다.

### Codex에게 요청할 때

반복 작업은 자연어보다 skill prompt로 요청합니다.

```text
$office-to-markdown "40_RAW/00_Inbox/자료.docx"를 Markdown으로 변환해.
$kb-ingest "40_RAW/10_Meetings/260708 - 회의.md"를 근거로 Planning 반영 후보와 Decision 초안을 만들어.
$kb-quality-checks 이 저장소의 전체 결정적 검사를 실행하고 실패 항목을 요약해.
$kb-audit 전체 audit 결과를 요약해.
$kb-review-pack 전체 KB를 사람 검토 전에 점검하고 다음 리뷰 액션을 요약해.
```

반대로 단순 조회, 리뷰, 이어지는 문서 편집, skill 자체 개선은 자연어로 요청해도 됩니다.

## 질문 허브

- 사용자, 제품 범위, 시나리오, 성공 기준, 프로젝트 운영은 [Planning Questions](10_PLANNING/99%20-%20Questions.md)에서 관리합니다.
- 시스템 경계, 인터페이스, 하드웨어, 런타임, 데이터, 평가, 안전은 [Technical Questions](20_TECHNICAL/99%20-%20Questions.md)에서 관리합니다.

## 문서 위치

| 위치 | 언제 쓰나 |
|---|---|
| `00_START_HERE` | 처음 읽을 때, 현재 상태를 파악할 때 |
| `10_PLANNING` | 왜 만들고, 누구를 위해, 어디까지 할지 정할 때 |
| `20_TECHNICAL` | 기획을 기술적으로 어떻게 가능하게 할지 정리할 때 |
| `30_DECISIONS` | 중요한 결정을 후보 또는 기록으로 남길 때 |
| `40_RAW` | 기획서, 회의록, 조사 자료, 멘토 피드백 원본을 보존할 때 |
| `90_TEMPLATES` | 반복 문서 초안을 만들 때 |
| `skills` | 변환, 정비, 검사, 배포용 deterministic script를 관리할 때 |

## Source of Truth

문서끼리 충돌하면 아래 순서를 따릅니다.

1. `status: selected`인 `30_DECISIONS` 문서
2. `status: reviewed`인 `10_PLANNING` 및 `20_TECHNICAL` 문서
3. `40_RAW` 원본 기록
4. `status: draft`인 문서

충돌을 발견하면 임의로 정리하지 말고, 기획 판단은 [Planning Questions](10_PLANNING/99%20-%20Questions.md), 기술 판단은 [Technical Questions](20_TECHNICAL/99%20-%20Questions.md)에 남깁니다.

## 원칙

- 기획서에 없는 내용을 그럴듯하게 확정하지 않습니다.
- Raw 문서는 최종 결론이 아닙니다.
- Planning 문서와 Technical 문서를 섞지 않습니다.
- Jira issue에는 문서 본문을 복붙하지 않고 관련 문서 링크만 둡니다.
- 이 저장소에서 제품 구현 코드는 만들지 않습니다.
