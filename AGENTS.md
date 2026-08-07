# AGENTS.md

이 문서는 Codex 또는 다른 문서화 에이전트가 이 KB에서 작업할 때 따라야 할 규칙이다.

## 0. KB 읽기 진입점

- KB 전체, 제품 범위 또는 기술 맥락이 필요한 작업은 루트
  [README.md](README.md)에서 시작한다.
- 목적별 읽기 순서는 [Reading Guide](<00_START_HERE/01 - Reading Guide.md>)를 따른다.
- 현재 기준은 관련 Planning과 Technical에서 읽고, 미결정 사항은 각 Questions,
  결정 이유는 Decision에서 확인한다.
- Raw는 공식 문서의 `출처`를 따라 근거와 과거 맥락이 필요할 때만 읽는다.

## 1. 저장소 성격

- 이 저장소는 끌리니(Cleany) 프로젝트의 기획 KB 저장소다.
- 이 저장소는 구현 레포가 아니다.
- 제품 구현 코드를 생성하거나 수정하지 않는다.
- 단, KB 품질 검사용 deterministic tool script는 `skills/*/scripts/` 아래에서만 관리할 수 있다.
- Codex repo-scoped skill 탐지는 `.agents/skills`를 사용하며, 이 저장소에서는 `skills/*`를 가리키는 symlink로 노출한다.
- 실제 구현 상세, 빌드 스크립트, 배포 설정을 이 저장소에 만들지 않는다.
- 이 저장소의 목적은 기획, 예비설계, 결정, 원본 기록을 Markdown으로 관리하는 것이다.

## 2. 작성 언어

- 모든 문서와 repo skill 안내는 한국어로 작성한다.
- YAML frontmatter key, 폴더명, 파일명, 명령 파일명, 기술 고유명사, 코드 블록 안의 구조 예시는 영어를 허용한다.
- 복수 항목은 문맥에 맞게 쉼표와 `와/과`, `및`, `또는`으로 연결하고 가운데점을 목록 구분자로 사용하지 않는다.

## 3. 문서 계층 규칙

- `10_PLANNING`은 문제, 사용자, 가치, 범위, 시나리오, 성공 기준 등의 기획을 다룬다.
- `20_TECHNICAL`은 시스템 개념, 아키텍처, 인터페이스, 제약, 가정, 리스크, 평가를 다룬다.
- 기획 문서와 기술 문서를 섞지 않는다.
- `30_DECISIONS`는 무엇을 왜 결정했는지 기록한다.
- `40_RAW`는 초안, 개인 학습 노트, 회의록, 조사 자료, 임시 메모와 첨부 원본을 두는 비공식 작업 공간이며 최종 결정이 아니다.
- 독립적인 Raw Markdown은 `40_RAW` 루트에, 해당 문서의 공용 첨부 자료는 `40_RAW/assets/`에 둔다. 팀원이 폴더 단위로 관리하는 학습, 조사 자료는 `40_RAW/YYMMDD - 주제/`로 보존하고 첨부 자료는 해당 묶음의 `assets/`에 둔다. Meetings, Research 같은 자료 종류별 분류 폴더는 만들지 않는다.
- 미해결 기획 질문은 `10_PLANNING/99 - Questions.md`, 미해결 기술 질문은 `20_TECHNICAL/99 - Questions.md`에서 중앙 관리한다. 개별 Planning과 Technical 문서 및 템플릿에는 별도 미해결 질문 섹션을 두지 않는다.
- 폴더는 지식의 성격을, Git은 검토 상태를 나타낸다. YAML `status`와 `ingest_status`는 사용하지 않는다.
- Planning과 Technical은 현재 팀이 합의한 기준이고, Decision은 실제로 내린 결정과 변경 이력이다.
- Raw와 작업 브랜치의 변경은 공식 기준이 아니다. 검토자와 승인 이력은 GitHub PR에 남긴다.
- Decision 후보는 Raw 또는 Questions에서 관리하고, 실제 결정이 확인된 뒤 작업 브랜치에서 Decision 문서를 작성한다.

## 4. 현재 기준과 결정 이력

`10_PLANNING`과 `20_TECHNICAL`을 현재 기준으로 사용한다. `30_DECISIONS`는 그 기준을
선택한 이유와 대체 이력을 설명하며, 이전 결정은
`supersedes`, `superseded_by`로 연결한다.

Planning이나 Technical이 Decision과 충돌하면 어느 한쪽을 임의로 우선하지 않는다.
문서 반영 누락이나 대체 관계를 확인하고, 기획 판단은
`10_PLANNING/99 - Questions.md`, 기술 판단은 `20_TECHNICAL/99 - Questions.md`에
질문으로 남긴다. `40_RAW`는 근거와 맥락을 확인할 때만 참고한다.

## 5. 기획서 기반 작성 규칙

- 기획서에 없는 내용을 임의로 확정하지 않는다.
- 기획서의 빈 항목이나 placeholder를 확정 사실처럼 쓰지 않는다.
- 불확실한 내용은 `검토 필요` 또는 `추가 확인 필요`로 표시한다.
- 시장 수치, 일정, 멘토 구성, 역할 분담 등은 기획서에 적힌 수준만 반영한다.
- Raw 문서를 최종 결정으로 취급하지 않는다.

## 6. 공식 문서 갱신 규칙

- 공식 문서를 갱신할 때 본문의 `출처`와 `관련 결정`을 가능한 한 갱신한다.
- 관계는 YAML 경로 문자열이나 Obsidian wiki link가 아니라 표준 Markdown 링크로 작성한다.
- Planning과 Technical 문서는 직접 근거를 `출처`에, 관련 Decision을 `관련 결정`에 둔다. Decision은 Raw 및 외부 근거를 `출처`에서 참조한다. Raw 문서는 상위 계층을 역링크하지 않는다.
- Jira issue에는 문서 본문을 복붙하지 않고 관련 문서 링크만 둔다.
- 결과물은 사람이 읽기 쉬운 구조로 작성한다.

## 7. AI 작업 규칙

- AI가 만든 Planning과 Technical 변경은 작업 브랜치에 두고 GitHub PR에서 사람이 검토한다.
- AI는 팀이 실제로 내린 결정이 확인된 경우에만 작업 브랜치에 Decision 문서를 작성한다.
- 공식 문서 직접 수정은 명시적으로 요청받았거나 사람 검토가 끝난 경우에만 수행한다.
- 근거 없는 rationale, 가정, 수치를 만들지 않는다.
- 가능한 미결정 사항을 추측해 Questions를 채우지 않는다. 팀이 실제로 제기했거나 출처에 명시된 질문만 정리한다.
- 작업 후 변경 파일과 사람 검토 필요 항목을 요약한다.

## 8. Skill과 결정적 검사

- 요청에 적합한 repo skill이 있으면 해당 `SKILL.md`를 따른다. skill과 script의 위치와
  사용법은 [skills 안내](skills/README.md)에서 확인한다.
- deterministic script는 변환, 형식 정비, 색인, 검사와 리포트만 수행하며 제품 또는
  기술 결정을 자동 확정하지 않는다.
- 문서, 템플릿, repo skill 또는 폴더 구조를 수정한 뒤에는 `kb-quality-checks`로 구조,
  Markdown formatting, metadata와 내부 링크를 검사한다.
- 검사 실패를 무시하지 않는다. 해결에 판단이 필요하면 기획 항목은 Planning
  Questions, 기술 항목은 Technical Questions에 남긴다.
