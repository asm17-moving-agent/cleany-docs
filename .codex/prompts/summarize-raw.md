# Raw ingest 프롬프트

지정된 Raw 문서를 `$kb-ingest` 워크플로우로 triage하라.

## 입력

- 요약할 `40_RAW` 문서 경로
- 필요한 경우 관련 Planning/Technical 문서 경로

## Office/PDF 입력 처리

입력이 `.docx`, `.pptx`, `.xlsx`, `.pdf`이면 먼저 LLM 없이 `$office-to-markdown` skill prompt로 Markdown 변환본을 만든 뒤 그 결과를 읽는다.

```text
$office-to-markdown "원본파일.docx"를 Markdown으로 변환해 "40_RAW/00_Inbox/원본파일 변환.md"에 저장해. 요약이나 해석은 하지 마.
```

변환은 원문 구조를 보존하기 위한 작업이며, 이 단계에서 요약이나 해석을 추가하지 않는다.

## 추출할 항목

1. 핵심 논의
2. 결정 후보
3. 미해결 질문
4. 후속 작업
5. 영향을 받을 Planning/Technical 문서
6. 새 Decision 문서 필요 여부

## 규칙

- 결정 후보를 확정된 결정으로 바꾸지 않는다.
- 근거 없는 이유를 만들지 않는다.
- 별도 working 폴더를 만들지 않는다.
- Raw 문서의 YAML metadata(`tags`, `ingest_status`, `ingest_targets`, `decision_candidates`, `planning_targets`)를 갱신한다.
- 생성/갱신하는 Planning 또는 Decision 문서에는 `source_refs`를 반드시 포함한다.
- 공식 확정 상태(`review_status: reviewed`, `status: selected`)로 바꾸지 않는다.
- Raw 문서의 빈 항목이나 placeholder는 `검토 필요`로 표시한다.
- Planning 내용과 Technical 내용을 섞지 않고 구분한다.

## 출력 형식

- Raw 문서 frontmatter 갱신안 또는 직접 갱신 결과
- 필요한 경우 `30_DECISIONS/Planning` 또는 `30_DECISIONS/Technical`의 `status: draft` Decision 초안
- 필요한 경우 `10_PLANNING` 문서 갱신안 또는 직접 갱신 결과
- 필요한 경우 `10_PLANNING/08 - Questions.md`에 추가할 질문
- 모든 생성/갱신 문서의 `tags`, `source_refs`, `related_decisions`, `review_status` 갱신

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
