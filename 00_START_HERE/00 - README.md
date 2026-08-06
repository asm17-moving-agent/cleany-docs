# 끌리니(Cleany) 기획 KB 시작하기

## 1. 이 문서는 무엇인가

이 KB는 끌리니 프로젝트의 기획, 예비설계, 결정, 원본 기록을 한곳에서 추적하기 위한 작업 공간이다. 구현 코드 저장소가 아니라, 팀원이 같은 근거를 보고 같은 질문을 닫아가기 위한 문서 저장소다.

끌리니는 무인 스터디카페에서 이용자 퇴실 뒤 책상 위 물체를 처리하는 XLeRobot 기반
모바일 매니퓰레이터 프로젝트다.

## 2. 처음 온 사람이 할 일

1. [Reading Guide](<01 - Reading Guide.md>)에서 내 목적에 맞는 읽기 순서를 고른다.
2. [Project Brief](<../10_PLANNING/00 - Project Brief.md>)로 프로젝트 목적을 확인한다.
3. [핵심 용어](<03 - Glossary.md>)에서 프로젝트 내부 용어의 책임 경계를 확인한다.
4. [Planning Questions](<../10_PLANNING/99 - Questions.md>)와 [Technical Questions](<../20_TECHNICAL/99 - Questions.md>)에서 아직 확정되지 않은 항목을 본다.
5. [Decision Index](<../30_DECISIONS/00 - Decision Index.md>)에서 실제 결정과 변경 이력을 확인한다.

`main`의 Planning과 Technical은 현재 기준이고, 작업 브랜치의 변경은 GitHub PR에서
검토 중인 제안이다.

## 3. 한 번에 이해하는 작업 흐름

이 KB의 기본 흐름은 `Raw 작성, 보존 → 공식 문서 반영 → 질문/Decision 분리 → 검사 → 사람 검토`다.

### 3.1 Raw 작성과 보존

`40_RAW`는 초안, 개인 학습 노트, 회의록, 조사 자료와 임시 메모를 자유롭게 두는 비공식 작업 공간이다. 독립 문서는 `40_RAW` 루트에, 공용 첨부 자료는 `40_RAW/assets/`에 둔다. 팀원이 폴더 단위로 관리하는 학습, 조사 자료는 `40_RAW/YYMMDD - 주제/`에 보존하고, 첨부 자료는 해당 묶음의 `assets/`에 둔다. 자료 종류별 고정 분류 폴더는 두지 않는다.

Raw의 내용만으로 프로젝트 결론을 확정하지 않는다. 공식 지식으로 사용할 내용은 Planning, Technical 및 Decision에 반영하고 GitHub PR에서 검토한다.

### 3.2 공식 문서 반영

Raw에서 Planning 또는 Decision으로 옮길 내용이 보이면 `$kb-ingest`를 사용한다. 이때 작성자는 다음을 구분한다.

| 구분                          | 처리                                      |
| --------------------------- | --------------------------------------- |
| 기획 범위, 사용자, 가치, 성공 기준       | `10_PLANNING`에 반영                       |
| 시스템 개념, 아키텍처, 제약, 리스크       | `20_TECHNICAL`에 반영                      |
| 팀이 실제로 내린 중요한 선택          | `30_DECISIONS`에 Decision 기록           |
| 확정할 수 없는 기획 내용              | `10_PLANNING/99 - Questions.md`에 질문 추가  |
| 확정할 수 없는 기술 내용              | `20_TECHNICAL/99 - Questions.md`에 질문 추가 |

### 3.3 질문과 Decision 분리

질문은 결론이 아니다. 질문은 팀이 검토해야 할 빈칸이고, Decision은 검토 결과를 추적하는 문서다.

- 기획 질문은 [Planning Questions](<../10_PLANNING/99 - Questions.md>), 기술 질문은 [Technical Questions](<../20_TECHNICAL/99 - Questions.md>)에 남긴다.
- Decision 후보는 Raw 또는 Questions에 남긴다.
- 팀이 실제 결정을 내린 뒤 작업 브랜치에서 Decision 문서를 작성한다.
- 검토와 승인 이력은 GitHub PR에 남기고, 병합된 Decision을 결정 이력으로 사용한다.

### 3.4 검사와 리뷰

문서를 고친 뒤에는 `$kb-quality-checks`를 실행한다. 이 검사는 구조, formatting, YAML metadata, 내부 링크, repo skill 구조를 확인한다.

검토 준비가 필요하면 `$kb-audit`를 실행한다. 이 리포트는 제품 문서의 검토 플래그,
Decision 목록, 대체 관계와 문서별 출처 상태를 요약한다.

사람 검토 전에 한 번에 볼 패키지가 필요하면 `$kb-review-pack`을 사용한다. 이 skill은 품질 검사, audit, Decision 목록, 대체 관계, 미해결 질문, 다음 리뷰 액션을 함께 요약한다.

검사 실패가 단순 형식 문제면 수정한다. 판단이 필요하면 기획 항목은 [Planning Questions](<../10_PLANNING/99 - Questions.md>), 기술 항목은 [Technical Questions](<../20_TECHNICAL/99 - Questions.md>)에 남긴다.

## 4. 실제 상황별 절차

### 4.1 새 원본 자료가 들어오면

1. 독립적인 Markdown 초안과 메모는 `40_RAW` 루트에 둔다.
2. 독립 문서의 Office/PDF/이미지 첨부 자료는 `40_RAW/assets/`에 보존한다.
3. 팀원이 폴더 단위로 관리하는 학습, 조사 자료는 `40_RAW/YYMMDD - 주제/`에 보존하고, 첨부 파일은 해당 묶음의 `assets/`에 둔다.
4. 필요한 경우 `$office-to-markdown`으로 Office/PDF 파일을 변환한다.
5. Raw 문서는 최종 결정으로 취급하지 않는다.
6. 공식 문서에 반영할 후보가 있으면 `$kb-ingest`를 사용한다.
7. Planning과 Technical에는 직접 근거를 `출처`에, 관련 Decision을 `관련 결정`에 표준 Markdown 링크로 둔다. Decision은 Raw 및 외부 근거를 `출처`에서 참조하고 Raw는 상위 계층을 역링크하지 않는다.

예시 요청:

```text
$office-to-markdown "40_RAW/assets/자료.docx"를 Markdown으로 변환해 "40_RAW/자료 원문 변환.md"에 저장해. 요약이나 해석은 하지 마.
```

### 4.2 질문을 발견하면

1. 확정하지 않는다.
2. 기획 판단은 [Planning Questions](<../10_PLANNING/99 - Questions.md>), 기술 판단은 [Technical Questions](<../20_TECHNICAL/99 - Questions.md>)에 질문으로 남긴다.
3. 결정이 필요한 질문이면 [Decision Index](<../30_DECISIONS/00 - Decision Index.md>)의 후보와 연결한다.
4. Jira 작업이 필요하면 문서 본문을 복사하지 말고 관련 문서 링크만 둔다.

### 4.3 결정을 내려야 하면

1. 후보가 프로젝트 방향, Sprint, 기술 리스크, 안전 기준에 영향을 주는지 본다.
2. 아직 선택 전이면 Raw 또는 Questions에서 관리한다.
3. 팀이 실제 결정을 내리면 작업 브랜치에 Decision 문서를 작성한다.
4. 검토와 승인 이력은 GitHub PR에 남기고 병합 후 결정 이력으로 사용한다.

예시 요청:

```text
$kb-ingest "40_RAW/260708 - MVP 범위 회의.md"를 근거로 Planning 반영안과 회의에서 실제로 확정된 Decision만 정리해.
```

### 4.4 문서를 고쳤으면

1. `$kb-quality-checks`로 구조, metadata, 링크를 확인한다.
2. `$kb-audit`로 검토 플래그와 Decision 목록, 대체 관계를 확인한다.
3. 실패 항목이 기획 판단을 요구하면 임의 수정하지 않고 질문으로 남긴다.

예시 요청:

```text
$kb-quality-checks 이 저장소의 전체 결정적 검사를 실행하고 실패 항목을 요약해.
$kb-audit 전체 audit 결과를 요약해.
$kb-review-pack 전체 KB를 사람 검토 전에 점검하고 다음 리뷰 액션을 요약해.
```

## 5. 어디에 무엇을 쓰나

| 위치             | 쓰는 내용                        | 쓰지 않는 내용        |
| -------------- | ---------------------------- | --------------- |
| `10_PLANNING`  | 현재 합의된 문제, 사용자, 범위, 시나리오, 성공 기준 | 하드웨어 상세 구현      |
| `20_TECHNICAL` | 현재 합의된 시스템 개념, 아키텍처, 인터페이스, 제약 | 시장 narrative 반복 |
| `30_DECISIONS` | 실제로 내린 중요한 결정과 이유, 대체 이력       | 결정 전 후보          |
| `40_RAW`       | 초안, 학습 노트, 회의록, 조사 자료와 첨부 원본 | 공식 결론           |
| `90_TEMPLATES` | 반복 문서 템플릿                    | 프로젝트 고유 사실      |

## 6. 초심자가 자주 헷갈리는 규칙

| 헷갈리는 점                      | 기준                                |
| --------------------------- | --------------------------------- |
| Raw에 적혀 있으면 확정인가?           | 아니다. Raw는 비공식 작업 공간이며 최종 결정이 아니다. |
| 작업 브랜치의 공식 문서 변경은 확정인가?      | 아니다. PR 검토 후 `main`에 병합되어야 현재 기준이다. |
| Decision 후보는 어디에 두는가?          | Raw 또는 실제 Questions에 둔다.             |
| 모르는 내용을 추정해서 채워도 되는가?       | 안 된다. `검토 필요` 또는 `추가 확인 필요`로 남긴다. |
| Jira issue에는 무엇을 넣는가?       | 문서 본문 복붙이 아니라 관련 문서 링크를 넣는다.      |
| 제품 구현 코드를 만들어도 되는가?         | 안 된다. 이 저장소는 기획 KB다.              |

## 7. 기본 원칙

- Raw는 근거지만 최종 결정은 아니다.
- 기획서에 없는 내용을 확정 사실처럼 쓰지 않는다.
- Planning과 Technical을 섞지 않는다.
- 폴더는 지식의 성격을, Git 브랜치와 PR은 검토 상태를 나타낸다.
- 팀이 실제로 내리지 않은 결정을 Decision으로 만들지 않는다.
