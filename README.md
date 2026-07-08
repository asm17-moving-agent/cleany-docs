# 끌리니(Cleany) 기획 KB

끌리니(Cleany)는 무인 점포 및 공간 대여 시설의 이용 후 정리·점검 업무를 자동화하기 위한 XLeRobot 기반 관리 로봇 프로젝트입니다.

이 저장소는 구현 레포가 아니라, 팀원이 기획서·회의록·조사 자료·의사결정 기록을 함께 관리하기 위한 **기획/예비설계 중심 Markdown KB**입니다.

## 프로젝트 기본 정보

| 항목     | 내용                                                                                                   |
| ------ | ---------------------------------------------------------------------------------------------------- |
| 프로젝트명  | 끌리니(Cleany) : 무인 점포 관리 로봇                                                                            |
| 팀명     | AI 에이전트는 움직이고 싶어                                                                                     |
| 팀원     | 이동근, 박창수, 이정현                                                                                        |
| 1차 타깃  | 무인 스터디카페 및 공간대여 시설 중심으로 검토                                                                           |
| 핵심 플랫폼 | XLeRobot 기반 모바일 매니퓰레이터                                                                               |
| 주요 기술  | Rule-based VLA, ROS 2, SLAM/Nav2, Jetson AGX Orin, RGB-D, 2D LiDAR, IMU, MuJoCo, Isaac Sim, TensorRT |

## 이 저장소의 목적

이 저장소는 다음을 위해 사용합니다.

- 프로젝트 기획과 문제 정의를 정리합니다.
- 타깃 사용자와 핵심 시나리오를 관리합니다.
- 예비 기술 설계와 기술 리스크를 정리합니다.
- 중요한 결정과 그 이유를 기록합니다.
- 기획서, 회의록, 조사 자료 등 Raw 기록을 보존합니다.
- Obsidian, GitHub, Google Drive, Jira를 함께 사용할 때 문서 기준점을 제공합니다.

## 이 저장소가 아닌 것

- 실제 구현 레포가 아닙니다.
- 로봇 소프트웨어, AI 모델, 서버, 대시보드 구현 코드를 관리하지 않습니다.
- 단, KB 품질 검사용 deterministic tool script는 `skills/*/scripts/` 아래에서 관리합니다.
- Codex가 자동 탐지하는 repo-scoped skill entrypoint는 `.agents/skills` 아래에 둡니다.
- Jira를 대체하지 않습니다.
- AI가 생성한 초안을 사람 검토 없이 공식 문서로 확정하는 공간이 아닙니다.

## 처음 읽는 순서

빠르게 프로젝트를 파악하려면 아래 순서로 읽어주세요.

1. [00_START_HERE/00 - README.md](00_START_HERE/00%20-%20README.md)
2. [00_START_HERE/01 - Reading Guide.md](00_START_HERE/01%20-%20Reading%20Guide.md)
3. [10_PLANNING/00 - Project Brief.md](10_PLANNING/00%20-%20Project%20Brief.md)
4. [10_PLANNING/02 - Target Scenario.md](10_PLANNING/02%20-%20Target%20Scenario.md)
5. [20_TECHNICAL/00 - Technical Overview.md](20_TECHNICAL/00%20-%20Technical%20Overview.md)
6. [30_DECISIONS/00 - Decision Index.md](30_DECISIONS/00%20-%20Decision%20Index.md)
7. [10_PLANNING/08 - Questions.md](10_PLANNING/08%20-%20Questions.md)

## 폴더 구조

```text
00_START_HERE/              처음 읽는 문서, 읽기 가이드, 현재 상태, 용어집
10_PLANNING/                문제, 사용자, 범위, 시나리오, 성공 기준
20_TECHNICAL/               예비 기술 설계, 시스템 개념, 리스크
30_DECISIONS/               중요한 결정과 이유
40_RAW/                     기획서, 회의록, 조사 자료, 멘토 피드백 등 원본 기록
90_TEMPLATES/               반복 작성용 문서 템플릿
.agents/skills/             Codex가 탐지하는 repo-scoped skill entrypoint
.codex/prompts/             Codex 문서화 작업용 프롬프트
skills/                     LLM 없이 실행하는 deterministic skill 원본과 스크립트
pyproject.toml              uv project 설정
uv.lock                     uv dependency lockfile
```

## 문서 계층별 역할

| 위치 | 역할 |
|---|---|
| `00_START_HERE` | 새 팀원이 처음 보는 진입점입니다. |
| `10_PLANNING` | 왜 이 프로젝트를 하는지, 누구를 위한 것인지, 어디까지 만들 것인지 정리합니다. |
| `20_TECHNICAL` | 기획을 기술적으로 어떻게 가능하게 할지 예비 설계 수준에서 정리합니다. |
| `30_DECISIONS` | 중요한 결정을 왜 했는지 기록합니다. |
| `40_RAW` | 원본 기록입니다. 최종 결론이 아니며 YAML metadata로 ingest 상태를 추적합니다. |
| `90_TEMPLATES` | 새 문서를 만들 때 사용하는 템플릿입니다. |

## Source of Truth 우선순위

문서 간 내용이 충돌하면 아래 순서를 따릅니다.

1. `review_status: reviewed`인 `10_PLANNING` 및 `20_TECHNICAL` 문서
2. `status: selected`인 `30_DECISIONS` 문서
3. `40_RAW` 원본 기록
4. `status: draft` 또는 `review_status: needs-human-review`인 문서

충돌을 발견하면 임의로 해결하지 않고 [10_PLANNING/08 - Questions.md](10_PLANNING/08%20-%20Questions.md)에 질문으로 남깁니다.

## 작업 방식

### 새 원본 자료를 추가할 때

1. 기획서, 회의록, 조사 자료, 멘토 피드백은 `40_RAW` 아래에 추가합니다.
2. Raw 문서는 최종 결정으로 취급하지 않습니다.
3. Raw frontmatter의 `tags`, `ingest_status`, `ingest_targets`, `decision_candidates`, `planning_targets`를 갱신해 추적합니다.
4. Raw를 Planning 또는 Decision으로 변환해야 하면 `$kb-ingest` skill prompt를 사용합니다.
5. 사람 검토 전 문서는 `status: draft`, `review_status: needs-human-review`를 유지합니다.

### 공식 문서를 수정할 때

1. 기획 내용은 `10_PLANNING`에 반영합니다.
2. 기술 내용은 `20_TECHNICAL`에 반영합니다.
3. 중요한 결정은 `30_DECISIONS`에 Decision 문서로 남깁니다.
4. 가능한 경우 `source_refs`, `related_decisions`, `related_jira`를 갱신합니다.
5. 불확실한 내용은 확정하지 말고 `검토 필요` 또는 `추가 확인 필요`로 표시합니다.

### Jira와 함께 사용할 때

- Jira는 작업 상태, Sprint, 담당자, 일정 관리의 기준입니다.
- Jira issue에는 문서 본문을 복사하지 않습니다.
- Jira issue에는 관련 Planning, Technical, Decision, Raw 문서 링크만 둡니다.

## 현재 상태

현재 KB는 기획서 원문을 기반으로 만든 초기 scaffold입니다.

- Planning 문서는 초안 상태입니다.
- Technical 문서는 예비설계 초안 상태입니다.
- selected Decision은 아직 임의로 생성하지 않았습니다.
- 팀 역할, 멘토 역할, 상세 일정, 평가 지표, 안전 기준은 추가 검토가 필요합니다.

자세한 내용은 [00_START_HERE/02 - Current Status.md](00_START_HERE/02%20-%20Current%20Status.md)를 확인하세요.

## 주요 검토 필요 항목

- MVP 기능 범위
- 무인 스터디카페 1차 타깃 확정 여부
- 팀원별 역할 분담
- 멘토별 역할
- 월별 추진 일정
- 정량 성공 기준
- 안전 기준 및 실패 처리 정책
- Jetson AGX Orin 64GB 확정 여부
- 관제 대시보드의 MVP 포함 여부
- 기획서 시장 수치의 출처 검증

## 문서 작성 원칙

- 기획서에 없는 내용을 그럴듯하게 확정하지 않습니다.
- Raw 문서는 최종 결론이 아닙니다.
- `status: draft` 또는 `review_status: needs-human-review` 문서는 사람 검토 전까지 공식 문서가 아닙니다.
- Planning 문서와 Technical 문서를 섞지 않습니다.
- Decision 문서는 “무엇을 정했는가”보다 “왜 그렇게 정했는가”를 남기는 데 집중합니다.

## Codex skill prompt 기반 deterministic workflow

이 저장소는 문서 저장소이지만, Office 파일 변환과 품질 검사를 LLM 없이 실행하기 위해 `uv` project로 초기화되어 있습니다. 다만 문서 작성 워크플로우에서는 사용자가 직접 하위 Python 실행 명령을 작성하지 않고, Codex에 skill prompt로 요청합니다.

Codex 공식 skill 탐지 위치는 repo 기준 `.agents/skills`이므로, 이 저장소는 `.agents/skills/<skill-name>`을 `skills/<skill-name>`으로 연결해 둡니다. Codex는 skill의 `SKILL.md`를 읽고 필요한 deterministic script를 실행합니다.

Office/PDF 파일을 Markdown으로 변환:

```text
$office-to-markdown "파일.docx"를 Markdown으로 변환해 "40_RAW/00_Inbox/파일 변환.md"에 저장해. 요약이나 해석은 하지 마.
```

Markdown formatting 정리:

```text
$kb-maintenance Markdown formatting을 정리해. trailing whitespace, newline, fence 균형을 확인하고 필요한 경우 수정해.
```

Metadata report 생성:

```text
$kb-maintenance YAML metadata report를 "40_RAW/60_External_Artifacts/metadata-report.md"에 생성해.
```

Raw → Planning/Decision 변환:

```text
$kb-ingest "40_RAW/10_Meetings/YYMMDD - MVP 범위 회의.md"를 근거로 Planning 반영 후보와 Decision 초안을 만들어. 별도 working 폴더를 만들지 말고 YAML metadata로 상태를 표시해.
```

템플릿 기반 새 문서 생성:

```text
$kb-doc-factory planning 문서 "운영자 페르소나" 초안을 템플릿으로 생성해.
```

Audit 리포트 생성:

```text
$kb-audit 전체 audit 리포트를 "40_RAW/60_External_Artifacts/audit" 아래에 생성해.
```

Google Drive/외부 리뷰어용 stable view 생성:

```text
$kb-publish 외부 공유용 stable view를 "dist/stable-view"에 생성해. Raw는 기본 제외해.
```

## 결정적 검사

문서, 템플릿, 프롬프트, 폴더 구조를 수정한 뒤에는 가능하면 아래처럼 Codex에 검사를 요청합니다.

```text
$kb-quality-checks 이 저장소의 전체 결정적 검사를 실행하고 실패 항목을 요약해.
```

검사 항목은 다음과 같습니다.

- 필수 폴더/파일 구조
- Markdown formatting
- Obsidian YAML metadata
- 내부 링크
- Codex prompt 검사 규칙 포함 여부

## AI/Codex 작업 규칙

AI 또는 Codex가 이 저장소에서 작업할 때는 [AGENTS.md](AGENTS.md)를 반드시 따릅니다.

핵심 규칙은 다음과 같습니다.

- 이 저장소에서 제품 구현 코드를 생성하거나 수정하지 않습니다.
- 사람 검토 없이 공식 문서로 승격하지 않습니다.
- 기획서에 없는 내용을 임의로 확정하지 않습니다.
- 문서 간 충돌은 질문으로 남깁니다.
