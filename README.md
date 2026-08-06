# 끌리니(Cleany) 기획 KB

끌리니(Cleany)는 무인 점포와 공간 대여 시설의 이용 후 정리, 점검 업무를 자동화하기 위한 XLeRobot 기반 관리 로봇 프로젝트입니다.

이 저장소는 구현 레포가 아닙니다. 팀원이 기획서, 회의록, 조사 자료, 의사결정 기록을 함께 관리하는 **기획/예비설계 중심 Markdown KB**입니다.

## 먼저 할 일

처음 들어왔다면 아래 순서로 보면 됩니다.

1. 전체 맥락을 잡는다: [00_START_HERE/00 - README.md](00_START_HERE/00%20-%20README.md)
2. 내 역할에 맞는 읽기 순서를 고른다: [00_START_HERE/01 - Reading Guide.md](00_START_HERE/01%20-%20Reading%20Guide.md)
3. 막힌 질문을 확인한다: [Planning Questions](10_PLANNING/99%20-%20Questions.md), [Technical Questions](20_TECHNICAL/99%20-%20Questions.md)
4. 결정 이력을 확인한다: [30_DECISIONS/00 - Decision Index.md](30_DECISIONS/00%20-%20Decision%20Index.md)

현재 가장 중요한 일은 문서를 더 많이 만드는 것이 아니라, 두 `Questions` 문서의
실제 질문을 사람 검토로 닫고 결정된 내용을 Planning, Technical 및 Decision에
반영하는 것입니다.

## 처음 작업하는 사람을 위한 10분 흐름

이 저장소에서 가장 먼저 구분해야 할 것은 `비공식 기록`, `현재 기준`, `결정 이력`입니다.

1. `40_RAW`는 비공식 작업 공간입니다. 초안, 개인 학습 노트, 회의록, 조사 자료와 원본을 자유롭게 보관합니다.
2. `main`의 `10_PLANNING`과 `20_TECHNICAL`은 현재 팀이 합의한 제품, 기술 기준입니다.
3. `main`의 `30_DECISIONS`는 실제로 내린 중요한 선택과 대체 이력을 추적합니다.
4. 불확실한 내용은 바로 결론으로 쓰지 않고 기획 질문은 `10_PLANNING/99 - Questions.md`, 기술 질문은 `20_TECHNICAL/99 - Questions.md`에 남깁니다.
5. 문서를 고친 뒤에는 `$kb-quality-checks`로 깨진 구조와 링크를 확인합니다.

작업할 때는 아래 질문으로 시작하면 됩니다.

| 내가 하려는 일 | 먼저 볼 곳 | 사용할 흐름 |
|---|---|---|
| 새 자료나 초안을 기록한다 | `40_RAW` | 필요한 경우 `$office-to-markdown`, `$kb-ingest` 사용 |
| 기획 범위를 정리한다 | `10_PLANNING/04 - Scope and Non-Goals.md` | 작업 브랜치에서 수정하고 PR 검토 |
| 기술 전제를 정리한다 | `20_TECHNICAL/00 - Technical Overview.md` | Planning과 섞지 않기 |
| 중요한 선택을 남긴다 | `30_DECISIONS/00 - Decision Index.md` | 실제 결정 확인 후 Decision 기록 |
| 무엇이 막혔는지 본다 | `10_PLANNING/99 - Questions.md`, `20_TECHNICAL/99 - Questions.md` | 계층별 질문 상태 갱신 |
| 공유 전 점검한다 | `00_START_HERE/01 - Reading Guide.md` | `$kb-quality-checks`, `$kb-audit`, `$kb-review-pack` |

## 자주 하는 작업

### 새 자료를 받았을 때

1. 독립적인 Markdown 초안과 메모는 `40_RAW` 루트에 둡니다.
2. 독립 문서의 Office/PDF/이미지 첨부 자료는 `40_RAW/assets/`에 둡니다.
3. 팀원이 폴더 단위로 관리하는 학습, 조사 자료는 `40_RAW/YYMMDD - 주제/`에 보존하고, 해당 묶음의 첨부 자료는 하위 `assets/`에 둡니다. Meetings, Research 같은 자료 종류별 분류 폴더는 만들지 않습니다.
4. Office/PDF 파일이면 `$office-to-markdown`으로 Markdown 변환을 요청합니다.
5. Planning 또는 Decision으로 반영해야 하면 `$kb-ingest`를 사용합니다.
6. 반영 후 본문의 `출처`, `관련 결정` 표준 Markdown 링크를 갱신합니다.

### 기획 내용을 정리할 때

1. 문제, 사용자, 가치, 범위, 시나리오는 `10_PLANNING`에 둡니다.
2. 근거가 Raw에만 있으면 작업 브랜치에서 반영안을 만들고 PR에서 검토합니다.
3. 팀이 실제로 제기한 미결정 사항은 [Planning Questions](10_PLANNING/99%20-%20Questions.md)에 남깁니다.

### 기술 내용을 정리할 때

1. 시스템 개념, 아키텍처, 인터페이스, 제약, 리스크는 `20_TECHNICAL`에 둡니다.
2. 실제 구현 코드, 빌드 설정, 배포 설정은 만들지 않습니다.
3. 하드웨어, 런타임, 모델 후보는 합의된 기준과 실제 미결정 사항을 구분합니다.
4. 팀이 실제로 제기한 기술 판단은 [Technical Questions](20_TECHNICAL/99%20-%20Questions.md)에 남깁니다.

### 결정을 남길 때

1. 결정 전 선택지와 질문은 Raw 또는 Questions에서 관리합니다.
2. 팀이 실제 결정을 내리면 `$kb-ingest` 또는 Decision 템플릿으로 작업 브랜치에 기록합니다.
3. 검토와 승인 이력은 GitHub PR에 남기고, 병합된 Decision을 결정 이력으로 사용합니다.
4. 이전 결정을 바꾸면 기존 문서를 삭제하지 않고 `supersedes`, `superseded_by`로 연결합니다.

### 문서 수정 후

1. `$kb-quality-checks`로 구조, formatting, metadata, 링크를 확인합니다.
2. `$kb-audit`로 검토 플래그와 Decision 목록, 대체 관계를 요약합니다.
3. 실패 항목이 판단을 요구하면 기획 항목은 Planning Questions, 기술 항목은 Technical Questions에 남깁니다.

### Codex에게 요청할 때

반복 작업은 자연어보다 skill prompt로 요청합니다.

```text
$office-to-markdown "40_RAW/assets/자료.docx"를 Markdown으로 변환해 "40_RAW/자료 변환.md"에 저장해.
$kb-ingest "40_RAW/260708 - 회의.md"를 근거로 Planning 반영안과 회의에서 실제로 확정된 Decision만 정리해.
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
| `10_PLANNING` | 현재 합의된 제품 기준을 확인하고 바꿀 때 |
| `20_TECHNICAL` | 현재 합의된 기술 기준을 확인하고 바꿀 때 |
| `30_DECISIONS` | 실제로 내린 중요한 결정과 변경 이력을 확인할 때 |
| `40_RAW` | 초안, 개인 학습 노트, 회의록, 조사 자료 등 비공식 내용을 기록할 때 |
| `90_TEMPLATES` | 반복 문서 초안을 만들 때 |
| `skills` | 변환, 정비, 검사, 배포용 deterministic script를 관리할 때 |

## Source of Truth

`main`의 Planning과 Technical을 현재 기준으로 사용하고, Decision에서 그 이유와 변경
이력을 확인합니다. 두 계층이 충돌하면 임의로 우선순위를 정하지 말고 문서 반영
누락이나 Decision 대체 관계를 확인합니다. 해결되지 않으면 기획 판단은
[Planning Questions](10_PLANNING/99%20-%20Questions.md), 기술 판단은
[Technical Questions](20_TECHNICAL/99%20-%20Questions.md)에 남깁니다.

`40_RAW`는 우선순위에 포함하지 않고 근거와 맥락을 확인할 때만 참고합니다.

## 원칙

- 기획서에 없는 내용을 그럴듯하게 확정하지 않습니다.
- Raw 문서는 최종 결론이 아닙니다.
- Planning 문서와 Technical 문서를 섞지 않습니다.
- Jira issue에는 문서 본문을 복붙하지 않고 관련 문서 링크만 둡니다.
- 이 저장소에서 제품 구현 코드는 만들지 않습니다.
