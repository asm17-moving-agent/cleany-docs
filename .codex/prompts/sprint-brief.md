# Sprint Brief 작성 프롬프트

Scrum Planning을 위한 Sprint Brief를 작성하라.

## 읽을 문서

- `00_START_HERE/02 - Current Status.md`
- `10_PLANNING/`
- `20_TECHNICAL/`
- `30_DECISIONS/00 - Decision Index.md`
- `10_PLANNING/08 - Questions.md`
- 최근 `40_RAW/` 문서

## 출력

- `40_RAW/60_External_Artifacts/Sprint_Briefs/YYMMDD - Sprint Brief.md`
- `status: draft`, `review_status: needs-human-review`, `ingest_status: raw`, `tags: [raw, sprint, draft]`를 사용한다.

## 포함할 항목

1. 현재 프로젝트 상태
2. Sprint 목표 후보
3. 관련 Planning 문서
4. 관련 Technical 문서
5. 관련 Decision
6. 미해결 질문
7. 리스크
8. Jira Issue 후보

## 규칙

- Jira Issue를 직접 생성하지 않는다.
- Issue 제목과 참고 문서만 제안한다.
- 확정되지 않은 내용을 Sprint 목표로 단정하지 않는다.
- Decision 후보는 후보로 표시하고 selected Decision처럼 쓰지 않는다.
- Sprint 목표는 현재 기획/기술 문서와 연결한다.
- 문서 본문을 Jira에 복붙하지 않는 전제를 유지한다.

## Codex skill prompt 우선

Codex 문서 작성 워크플로우에서는 사용자가 직접 하위 Python 실행 명령을 작성하지 않는다. 필요한 skill을 `$skill-name` 형식으로 명시해 요청한다. Codex는 해당 skill의 `SKILL.md`를 읽고 필요한 deterministic script를 실행한다.

- Office/PDF 원본 변환: `$office-to-markdown`
- 템플릿 기반 새 문서 생성: `$kb-doc-factory`
- Raw → Planning/Decision 변환: `$kb-ingest`
- Markdown formatting 정리, 파일 색인, metadata report: `$kb-maintenance`
- 검토 플래그, source_refs, Decision inventory 리포트: `$kb-audit`
- Google Drive/외부 공유용 stable view 생성: `$kb-publish`
- 구조/formatting/metadata/link/prompt 검사: `$kb-quality-checks`

## 결정적 검사

문서, 템플릿, 프롬프트, 폴더 구조를 생성하거나 수정한 경우 가능하면 `$kb-quality-checks` skill prompt로 검사를 요청한다.

```text
$kb-quality-checks 이 저장소의 전체 결정적 검사를 실행하고 실패 항목을 요약해.
```

검사 범위는 다음과 같다.

- 필수 폴더/파일 구조
- Markdown formatting
- Obsidian YAML metadata
- 내부 Markdown 링크와 Obsidian wiki link
- Codex prompt의 결정적 검사 안내 포함 여부

검사 실패 시 실패 항목을 요약하고, 공식 문서를 임의로 확정하지 않는다.
