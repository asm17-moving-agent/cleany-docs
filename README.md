# 끌리니(Cleany) 기획 KB

끌리니는 무인 스터디카페에서 이용자 퇴실 뒤 책상에 남은 물체를 확인하고 처리하는
XLeRobot 기반 모바일 매니퓰레이터 프로젝트다. 현재 MVP는 운영자가 Dashboard에서
지정한 좌석으로 로봇이 왕복하고, 책상 위 물체를 관찰하고 처리한 전후 결과를
제공하는 전체 흐름을 대상으로 한다.

이 저장소는 구현 코드가 아니라 제품 기획, 예비설계, 결정과 원본 기록을 관리하는
Markdown KB다. 사람과 AI 에이전트 모두 이 문서를 공통 지식 진입점으로 사용한다.
AI 에이전트의 작성 및 수정 규칙은 [AGENTS.md](AGENTS.md)를 따른다.

## 처음 읽기

15분 안에 전체 맥락을 파악하려면 다음 순서로 읽는다.

1. [Project Brief](<10_PLANNING/00 - Project Brief.md>)에서 프로젝트 목적을 본다.
2. [Target Scenario](<10_PLANNING/02 - Target Scenario.md>)에서 목표 데모 흐름을 본다.
3. [Success Criteria](<10_PLANNING/05 - Success Criteria.md>)에서 통과 조건을 본다.
4. [Technical Overview](<20_TECHNICAL/00 - Technical Overview.md>)에서 전체 기술
   경계를 본다.
5. [Planning Questions](<10_PLANNING/99 - Questions.md>)와
   [Technical Questions](<20_TECHNICAL/99 - Questions.md>)에서 미결정 사항을 본다.
6. [Decision Index](<30_DECISIONS/00 - Decision Index.md>)에서 실제 결정과 변경
   이력을 확인한다.

기획 검토, 기술 검토, 프로젝트 설명처럼 목적이 정해져 있다면
[Reading Guide](<00_START_HERE/01 - Reading Guide.md>)에서 경로를 고른다. 프로젝트
내부 용어와 책임 경계는 [Glossary](<00_START_HERE/03 - Glossary.md>)에서 확인한다.

## 문서를 해석하는 기준

| 구분 | 의미 |
|---|---|
| Planning | 현재 합의된 문제, 사용자, 범위, 시나리오와 성공 기준 |
| Technical | 현재 합의된 시스템 개념, 아키텍처, 인터페이스, 제약과 리스크 |
| Decision | 실제로 내린 중요한 결정, 이유와 대체 이력 |
| Questions | 팀이 실제로 제기했지만 아직 닫히지 않은 판단 |
| Raw | 초안, 개인 학습 노트, 회의록, 조사 자료와 원본을 두는 비공식 공간 |
| 작업 브랜치 | GitHub PR에서 검토 중인 변경안이며 아직 현재 기준이 아님 |

Planning과 Technical이 현재 기준이고, Decision은 그 기준을 선택하거나 변경한 이유를
설명한다. Raw는 근거와 과거 맥락을 확인할 때 사용하지만 그 자체를 결론으로
인용하지 않는다.

Planning이나 Technical이 Decision과 충돌하면 어느 한쪽을 임의로 우선하지 않는다.
문서 반영 누락이나 Decision의 대체 관계를 확인하고, 해결되지 않은 판단은 계층에
맞는 Questions에 남긴다.

## 문서 지도

| 위치 | 쓰는 내용 | 쓰지 않는 내용 |
|---|---|---|
| `00_START_HERE` | 목적별 읽기 경로와 프로젝트 용어 | 현재 제품 및 기술 기준 |
| `10_PLANNING` | 문제, 사용자, 가치, 범위, 시나리오와 성공 기준 | 하드웨어와 소프트웨어의 상세 설계 |
| `20_TECHNICAL` | 시스템 개념, 아키텍처, 인터페이스, 제약, 가정, 리스크와 평가 | 시장 및 사용자 문제의 반복 설명 |
| `30_DECISIONS` | 실제로 내린 중요한 결정, 이유와 대체 이력 | 결정 전 후보와 미해결 질문 |
| `40_RAW` | 초안, 개인 학습 노트, 회의록, 조사 자료, 임시 메모와 원본 | 공식 결론 |
| `90_TEMPLATES` | 반복 문서의 최소 템플릿 | 프로젝트 고유 사실 |
| `skills` | KB 변환, 정비와 검사 도구 | 제품 및 기술 결정 |

## 지식 반영 흐름

이 KB의 기본 흐름은 `Raw 보존 → 공식 문서 반영 또는 Questions 등록 → 실제 결정
기록 → 검사와 사람 검토`다.

1. 새 자료, 회의록, 조사와 초안은 `40_RAW`에 보존한다.
2. 현재 기준으로 합의한 제품 내용은 Planning, 기술 내용은 Technical에 반영한다.
3. 확정할 수 없는 내용은 계층에 맞는 Questions에 남긴다.
4. 팀이 실제로 내린 중요한 선택만 Decision으로 기록한다.
5. 작업 브랜치에서 형식과 링크를 검사하고 GitHub PR에서 검토한다.

Raw의 독립적인 Markdown 문서는 `40_RAW` 루트에 두고, 공용 첨부 자료는
`40_RAW/assets/`에 둔다. 팀원이 폴더 단위로 관리하는 학습 및 조사 자료는
`40_RAW/YYMMDD - 주제/`에 보존하고 첨부 자료는 해당 묶음의 `assets/`에 둔다.
Meetings나 Research처럼 자료 종류만으로 나눈 고정 분류 폴더는 만들지 않는다.

공식 문서를 갱신할 때 Planning과 Technical에는 직접 근거를 `출처`에, 관련
Decision을 `관련 결정`에 표준 Markdown 링크로 연결한다. Decision은 Raw 및 외부
근거를 `출처`에서 참조하고, Raw는 상위 문서를 역링크하지 않는다.

## 작업별 빠른 안내

| 하려는 일 | 먼저 볼 곳 | 처리 기준 |
|---|---|---|
| 새 자료나 초안 기록 | `40_RAW` | 원본을 보존하고 공식 결론으로 취급하지 않는다. |
| 기획 범위 정리 | `10_PLANNING` | 합의된 내용만 작업 브랜치에서 반영한다. |
| 기술 전제 정리 | `20_TECHNICAL` | 목표 구조, 현재 구현과 실험 후보를 구분한다. |
| 미결정 사항 기록 | 계층별 `99 - Questions.md` | 팀이 실제로 제기한 질문만 남긴다. |
| 중요한 선택 기록 | `30_DECISIONS` | 팀의 실제 결정이 확인된 뒤 작성한다. |
| 공유 전 검토 | Reading Guide와 Decision Index | 현재 기준, 미결정 사항과 변경 이력을 구분한다. |

변환, Raw 반영, audit와 품질 검사 방법은 [Skills 안내](skills/README.md)를 따른다.
세부 명령을 여러 안내 문서에 중복해서 적지 않는다.

## 협업 도구와 구현 문서의 경계

| 위치 | 관리하는 정보 |
|---|---|
| GitHub KB | 제품 및 기술 지식, 결정 이유와 근거 |
| GitHub PR | 문서 변경의 검토와 승인 이력 |
| Jira | 작업 상태, 담당자와 일정 |
| Discord | 대화와 빠른 논의 |
| Cleany 구현 레포 | 구현 사실, ROS interface, 설정, 실행과 검증 방법 |

Discord에서 지속적으로 참고해야 할 합의가 나오면 KB에 반영하고, 실행할 작업이
생기면 Jira에 기록한다. Jira issue에는 KB 본문을 복사하지 않고 관련 문서 링크를
둔다.

## 자주 헷갈리는 기준

| 질문 | 기준 |
|---|---|
| Raw에 적혀 있으면 확정인가? | 아니다. Raw는 비공식 작업 공간이다. |
| 작업 브랜치의 변경은 현재 기준인가? | 아니다. 사람 검토가 끝난 뒤 공유 기준에 반영한다. |
| Decision 후보는 어디에 두는가? | 실제 결정을 내리기 전에는 Raw 또는 Questions에서 관리한다. |
| 모르는 내용을 추정해서 채워도 되는가? | 안 된다. `검토 필요` 또는 `추가 확인 필요`로 남긴다. |
| Questions를 미리 많이 만들어도 되는가? | 안 된다. 팀이나 근거 문서에서 실제로 제기된 질문만 기록한다. |
| 일정과 담당자를 metadata에 넣어야 하는가? | 넣지 않는다. Jira를 Source of Truth로 사용한다. |
| 구현 방법은 어디에 쓰는가? | 구현 레포의 관련 package README에 쓴다. |

문서나 구조를 수정한 뒤에는 [품질 검사 안내](skills/kb-quality-checks/SKILL.md)에 따라
구조, Markdown formatting, metadata와 내부 링크를 검사한다. 검사를 통과해도 작업
브랜치의 변경은 사람 검토와 PR 병합 전까지 현재 기준이 아니다.
