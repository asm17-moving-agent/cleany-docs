# Planning/Technical 문서 갱신안 작성 프롬프트

Planning 또는 Technical 문서 갱신안을 작성하라. Raw에서 Planning으로 반영하는 경우 `$kb-ingest` 워크플로우를 우선 사용한다.

## 입력

- 대상 문서 경로
- 근거 Raw 문서 또는 Decision 문서
- 갱신 요청 요약

## Office/PDF 입력 처리

근거 문서가 `.docx`, `.pptx`, `.xlsx`, `.pdf`이면 먼저 LLM 없이 `$office-to-markdown` skill prompt로 Markdown 변환본을 만든다.

```text
$office-to-markdown "원본파일.docx"를 Markdown으로 변환해 "40_RAW/00_Inbox/원본파일 변환.md"에 저장해. 요약이나 해석은 하지 마.
```

변환 결과는 공식 문서가 아니라 Raw 근거로만 취급한다.

## 대상별 집중 영역

### 대상 문서가 `10_PLANNING` 아래에 있을 때

- 문제
- 사용자
- 가치
- 범위
- 타깃 시나리오
- 성공 기준
- 미해결 질문

### 대상 문서가 `20_TECHNICAL` 아래에 있을 때

- 시스템 개념
- 아키텍처
- 인터페이스
- 제약
- 가정
- 리스크
- 평가

## 규칙

- Planning 문서에 과도한 기술 상세를 넣지 않는다.
- Technical 문서에 과도한 기획 narrative를 넣지 않는다.
- 현재형으로 작성한다.
- 관련 Decision을 링크한다.
- 필요한 경우 `source_refs`를 갱신한다.
- 해결되지 않은 모호함은 `10_PLANNING/08 - Questions.md`에 추가한다.
- 명시적으로 요청받지 않는 한 `review_status: reviewed`로 바꾸지 않는다.
- 갱신한 문서는 `status: draft`, `review_status: needs-human-review`, 적절한 `tags`를 유지한다.
- 기획서에 없는 내용을 확정하지 않는다.

## 출력

- 대상 `10_PLANNING` 또는 `20_TECHNICAL` 문서의 갱신안 또는 직접 갱신 결과
- 갱신한 문서의 `source_refs`, `related_decisions`, `related_jira`, `tags`, `review_status`
- 필요한 경우 `10_PLANNING/08 - Questions.md`에 추가할 질문
- 관련 Jira Issue 후보

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
