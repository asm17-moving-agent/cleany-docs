---
type: start-here
status: draft
review_status: needs-human-review
tags:
  - start-here
  - start-here
  - cleany
updated: 2026-07-08
---

# 끌리니(Cleany) 기획 KB

## 1. 프로젝트 한 줄 요약

끌리니(Cleany)는 무인 점포 및 공간 대여 시설의 이용 후 정리·점검 업무를 자동화하기 위한 XLeRobot 기반 관리 로봇 프로젝트다.

## 2. 이 KB의 목적

이 KB는 기획서 원문을 바탕으로 팀원이 Obsidian에서 읽고 관리할 수 있는 기획/예비설계 중심 지식 저장소다.

- 프로젝트의 문제, 사용자, 타깃 시나리오를 정리한다.
- 예비 기술 개념과 주요 기술 리스크를 정리한다.
- 중요한 결정과 그 이유를 추적할 수 있게 한다.
- Raw 기록, draft 문서, reviewed 문서의 경계를 YAML metadata로 분리한다.
- Jira, GitHub 문서 레포, Google Drive, Obsidian을 함께 운영하기 위한 기준을 제공한다.

## 3. 이 KB가 아닌 것

- 실제 구현 레포가 아니다.
- 코딩 에이전트용 구현 컨텍스트가 아니다.
- SDD 수행 결과물이 아니다.
- Jira 작업 상태를 대체하는 저장소가 아니다.
- 사람 검토 전 `status: draft` 문서를 공식화하는 공간이 아니다.

## 4. 프로젝트 기본 정보

| 항목     | 내용                                                                                                      |
| ------ | ------------------------------------------------------------------------------------------------------- |
| 프로젝트명  | 끌리니(Cleany) : 무인 점포 관리 로봇                                                                               |
| 팀명     | AI 에이전트는 움직이고 싶어                                                                                        |
| 팀원     | 이동근, 박창수, 이정현                                                                                           |
| 1차 타깃  | 무인 스터디카페/공간대여 시설 중심으로 고려                                                                                |
| 핵심 플랫폼 | XLeRobot 기반 모바일 매니퓰레이터                                                                                  |
| 주요 기술  | Embodied AI, VLA, ROS 2, SLAM, Nav2, Jetson AGX Orin, RGB-D, 2D LiDAR, IMU, MuJoCo, Isaac Sim, TensorRT |

## 5. 문서 계층 설명

| 계층               | 역할                                                 | 주의점                                |
| ---------------- | -------------------------------------------------- | ---------------------------------- |
| `00_START_HERE`  | 처음 읽는 사람의 진입점, 읽는 순서, 현재 상태, 용어 정의                 | 전체를 요약하지만 세부 결정의 원본은 아니다.          |
| `10_PLANNING`    | 문제, 사용자, 범위, 시나리오, 성공 기준을 다루는 기획 문서                | 과도한 기술 구현 상세를 넣지 않는다.              |
| `20_TECHNICAL`   | 기획을 가능하게 할 예비 기술 설계 문서                             | 제품/시장 narrative를 과도하게 반복하지 않는다.    |
| `30_DECISIONS`   | 중요한 결정과 이유를 기록                                     | selected 상태가 아니면 확정 결정으로 취급하지 않는다. |
| `40_RAW`         | 기획서, 회의록, 조사, 멘토 피드백 등 원본 기록                       | Raw는 최종 결론이 아니며 ingest metadata로 추적한다. |
| `90_TEMPLATES`    | 반복 작성용 문서 템플릿                                      | 템플릿 사용 후 출처와 상태를 갱신한다.             |
| `.agents/skills` | Codex가 탐지하는 repo-scoped skill entrypoint              | 현재 `skills/*`를 가리키는 symlink로 관리한다.     |
| `.codex/prompts`  | Codex 문서화 작업 프롬프트                                  | 공식 문서 직접 수정 여부를 항상 확인한다.           |
| `skills`          | Office 변환, KB 정비, deterministic check용 skill 원본과 스크립트 | 기획/기술 결정을 자동 확정하지 않는다.             |

## 6. Source of Truth 우선순위

문서 간 내용이 충돌할 때는 아래 순서를 따른다.

1. `review_status: reviewed`인 `10_PLANNING` 및 `20_TECHNICAL` 문서
2. `status: selected`인 `30_DECISIONS` 문서
3. `40_RAW` 원본 기록
4. `status: draft` 또는 `review_status: needs-human-review`인 문서

충돌을 발견하면 임의로 해결하지 않는다. `10_PLANNING/08 - Questions.md`에 질문으로 남기고, 필요한 경우 관련 Jira issue 후보를 제안한다.

## 7. Raw → KB ingest 흐름

1. 기획서, 회의록, 조사 자료, 멘토 피드백을 `40_RAW`에 보존한다.
2. Raw frontmatter의 `tags`, `ingest_status`, `ingest_targets`, `decision_candidates`, `planning_targets`로 반영 상태를 추적한다.
3. Raw를 Planning 또는 Decision으로 변환해야 하면 `$kb-ingest` skill prompt를 사용한다.
4. 기획 내용은 `10_PLANNING`, 예비 기술 내용은 `20_TECHNICAL`, 중요한 이유와 선택은 `30_DECISIONS`에 분리해 반영한다.
5. 사람 검토 전 문서는 `status: draft`, `review_status: needs-human-review`를 유지한다.
6. 공식 문서 갱신 시 `source_refs`, `related_decisions`, `related_jira`를 가능한 한 갱신한다.
7. Jira issue에는 문서 본문을 복붙하지 않고 관련 문서 링크만 둔다.

## 8. 도구별 역할

### Jira

- 작업, Sprint, 담당자, 상태, 일정 관리에 사용한다.
- Jira는 작업 상태의 source of truth다.
- 문서 본문을 Jira에 복붙하지 않는다.
- Jira issue에는 관련 Planning/Technical/Decision/Raw/Project Repo 링크만 둔다.

### GitHub 문서 레포

- Markdown KB의 원본과 변경 이력을 관리한다.
- Raw 추가는 직접 commit 가능하다.
- Planning/Technical/Decision 변경은 리뷰를 권장한다.

### Google Drive

- 멘토, 팀원, 외부 리뷰어에게 공유할 stable view로 사용한다.
- 전체 Raw와 `status: draft` 문서를 무조건 공유하지 않는다.
- 공유 대상은 기본적으로 `00_START_HERE`, `10_PLANNING`, `20_TECHNICAL`, `30_DECISIONS`다.

### Obsidian

- 문서 작성, 탐색, 내부 링크 관리를 위한 인터페이스다.
- 링크와 백링크로 Planning, Technical, Decision, Raw의 연결을 추적한다.

### uv project / deterministic skills

- `uv`는 Office 파일 변환과 KB 품질 검사용 Python dependency를 관리한다.
- Codex 문서 작성 워크플로우에서는 직접 하위 Python 실행 명령을 작성하지 않고 `$skill-name` 형식의 skill prompt를 사용한다.
- Codex skill entrypoint는 `.agents/skills/<skill-name>`에 있으며, 실행 스크립트는 `skills/<skill-name>/scripts/`에 둔다.
- Office/PDF 원본 변환은 `$office-to-markdown` skill prompt를 사용한다.
- 템플릿 기반 새 문서 생성은 `$kb-doc-factory` skill prompt를 사용한다.
- 파일 색인과 metadata report 등 반복 정비는 `$kb-maintenance` skill prompt를 사용한다.
- Raw에서 Planning/Decision으로 변환할 때는 `$kb-ingest` skill prompt를 사용한다.
- 검토 플래그와 source_refs 리포트는 `$kb-audit` skill prompt를 사용한다.
- Google Drive/외부 공유용 stable view 생성은 `$kb-publish` skill prompt를 사용한다.
- Formatting, metadata, 링크, 구조 검사는 `$kb-quality-checks` skill prompt를 사용한다.
- deterministic script는 문서 변환, 정비, 리포트, 배포 사본 생성을 돕지만, 기획/기술 판단을 자동 확정하지 않는다.

## 9. 주요 문서 링크

- [[00_START_HERE/01 - Reading Guide|Reading Guide]]
- [[00_START_HERE/02 - Current Status|Current Status]]
- [[00_START_HERE/03 - Glossary|Glossary]]
- [[10_PLANNING/00 - Project Brief|Project Brief]]
- [[10_PLANNING/02 - Target Scenario|Target Scenario]]
- [[10_PLANNING/08 - Questions|Questions]]
- [[20_TECHNICAL/00 - Technical Overview|Technical Overview]]
- [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]]
- [[30_DECISIONS/00 - Decision Index|Decision Index]]
- [[40_RAW/20_Planning/기획서 원문 요약|기획서 원문 요약]]
