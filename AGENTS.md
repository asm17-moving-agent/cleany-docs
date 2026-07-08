# AGENTS.md

이 문서는 Codex 또는 다른 문서화 에이전트가 이 KB에서 작업할 때 따라야 할 규칙이다.

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

## 3. 문서 계층 규칙

- `10_PLANNING`은 문제, 사용자, 가치, 범위, 시나리오, 성공 기준을 다룬다.
- `20_TECHNICAL`은 시스템 개념, 아키텍처, 인터페이스, 제약, 가정, 리스크, 평가를 다룬다.
- 기획 문서와 기술 문서를 섞지 않는다.
- `30_DECISIONS`는 무엇을 왜 결정했는지 기록한다.
- `40_RAW`는 원본 기록이며 최종 결정이 아니다.
- 초안 여부와 검토 상태는 각 문서의 YAML metadata(`status`, `review_status`, `tags`, `ingest_status`)로 표현한다.
- 사람 검토 없이 `status: selected` 또는 `review_status: reviewed`로 승격하지 않는다.

## 4. Source of Truth 우선순위

문서 간 내용이 충돌할 때는 아래 순서를 따른다.

1. `review_status: reviewed`인 `10_PLANNING` 및 `20_TECHNICAL` 문서
2. `status: selected`인 `30_DECISIONS` 문서
3. `40_RAW` 원본 기록
4. `status: draft` 또는 `review_status: needs-human-review`인 문서

충돌을 임의로 해결하지 않는다. 반드시 `10_PLANNING/08 - Questions.md`에 질문으로 남기고, 필요한 경우 관련 Jira issue 후보를 제안한다.

## 5. 기획서 기반 작성 규칙

- 기획서에 없는 내용을 임의로 확정하지 않는다.
- 기획서의 빈 항목이나 placeholder를 확정 사실처럼 쓰지 않는다.
- 불확실한 내용은 `검토 필요` 또는 `추가 확인 필요`로 표시한다.
- 시장 수치, 일정, 멘토 구성, 역할 분담 등은 기획서에 적힌 수준만 반영한다.
- Raw 문서를 최종 결정으로 취급하지 않는다.

## 6. 공식 문서 갱신 규칙

- 공식 문서를 갱신할 때 `source_refs`, `related_decisions`, `related_jira`를 가능한 한 갱신한다.
- Decision을 반영한 경우 해당 Decision 문서와 반영 문서를 서로 링크한다.
- Jira issue에는 문서 본문을 복붙하지 않고 관련 문서 링크만 둔다.
- 결과물은 사람이 읽기 쉬운 구조로 작성한다.

## 7. AI 작업 규칙

- AI가 만든 문서는 대상 계층에 바로 두되 `status: draft`, `review_status: needs-human-review`, 적절한 `tags`를 반드시 유지한다.
- 공식 문서 직접 수정은 명시적으로 요청받았거나 사람 검토가 끝난 경우에만 수행한다.
- 근거 없는 rationale, 가정, 수치를 만들지 않는다.
- Decision 후보를 selected Decision으로 바꾸지 않는다.
- 작업 후 변경 파일과 사람 검토 필요 항목을 요약한다.

## 8. Codex skill prompt와 deterministic tool 규칙

- 이 저장소는 Office 파일 변환, Markdown 정비, 품질 검사를 LLM 없이 실행하기 위해 `uv` project로 초기화되어 있다.
- Python dependency는 `pyproject.toml`과 `uv.lock`으로 관리한다.
- Codex 문서 작성 워크플로우에서는 사용자가 직접 하위 Python 실행 명령을 작성하지 않고 `$skill-name` 형식의 skill prompt를 사용한다.
- Codex custom prompt(`.codex/prompts`)는 deprecated이므로 이 저장소의 워크플로우 표면으로 사용하지 않는다.
- 재사용 가능한 작업 지침은 `.agents/skills/<skill-name>/SKILL.md`로 노출되는 repo skill에 둔다.
- 현재 repo skill로 명확히 처리 가능한 반복 변경 작업은 요청에 적절한 `$skill-name`이 명시된 경우에만 수행한다.
- `$skill-name` 없는 자연어 요청이 현재 skill로 처리 가능한 반복 작업이면 작업을 실행하지 않고 적절한 skill prompt 예시를 제안한다.
- 같은 세션에서 이어지는 문서 편집, 정책/skill/검사 스크립트 개선, 아직 repo skill이 없는 작업, 조회, 설명, 리뷰, 상태 확인은 자연어로 처리할 수 있다.
- Codex용 skill entrypoint는 `.agents/skills/<skill-name>/SKILL.md`이며, 실행 스크립트는 `skills/<skill-name>/scripts/` 아래에 둔다.
- Office/PDF 원본 변환은 `$office-to-markdown` skill prompt를 우선 사용한다.
- 템플릿 기반 새 문서 생성은 `$kb-doc-factory` skill prompt를 우선 사용한다.
- Markdown 정비와 metadata report는 `$kb-maintenance` skill prompt를 우선 사용한다.
- Raw에서 Planning/Decision으로 변환할 때는 `$kb-ingest` skill prompt를 우선 사용한다.
- 검토 플래그, source_refs, Decision inventory 리포트는 `$kb-audit` skill prompt를 우선 사용한다.
- 사람 검토 준비 패키지는 `$kb-review-pack` skill prompt를 사용한다.
- 외부 공유/게시 방식은 GitHub Pages + obsidian-html 기반으로 별도 설계한다. 이 저장소에서는 더 이상 `$kb-publish` stable view 생성을 사용하지 않는다.
- GitHub draft PR 생성은 `$kb-pr` skill prompt를 사용한다.
- deterministic script는 문서 형식, 변환, 검사, 색인, 리포트, 배포 사본 생성만 수행하며 기획/기술 결정을 자동 확정하지 않는다.

## 9. 결정적 검사 규칙

문서, 템플릿, repo skill, 폴더 구조를 생성하거나 수정한 경우 가능하면 `$kb-quality-checks` skill prompt로 결정적 검사를 요청한다.

```text
$kb-quality-checks 이 저장소의 전체 결정적 검사를 실행하고 실패 항목을 요약해.
```

검사 범위는 다음과 같다.

- 필수 폴더/파일 구조
- Markdown formatting
- Obsidian YAML metadata
- 내부 Markdown 링크와 Obsidian wiki link
- repo skill 구조와 deprecated `.codex/prompts` 부재

검사 실패를 무시하고 공식 문서를 확정하지 않는다. 실패 항목이 기획 판단을 요구하면 `10_PLANNING/08 - Questions.md`에 질문으로 남긴다.
