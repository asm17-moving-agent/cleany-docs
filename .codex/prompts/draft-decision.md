# Decision 초안 작성 프롬프트

Planning 또는 Technical Decision 초안을 `$kb-ingest` 워크플로우로 작성하라.

## 입력

- Raw 문서
- 관련 Planning/Technical 문서
- 결정 제목
- 결정 날짜
- decision_type: `planning` 또는 `technical`

## Office/PDF 입력 처리

Raw 입력이 `.docx`, `.pptx`, `.xlsx`, `.pdf`이면 먼저 LLM 없이 `$office-to-markdown` skill prompt로 Markdown 변환본을 만든다.

```text
$office-to-markdown "원본파일.docx"를 Markdown으로 변환해 "40_RAW/00_Inbox/원본파일 변환.md"에 저장해. 요약이나 해석은 하지 마.
```

변환 결과도 Raw 출처로 함께 링크한다.

## 출력

- Planning Decision: `30_DECISIONS/Planning/YYMMDD - {제목}.md`
- Technical Decision: `30_DECISIONS/Technical/YYMMDD - {제목}.md`
- 상태는 `status: draft`, `review_status: needs-human-review`로 둔다.

## 필수 섹션

1. 결정
2. 이유
3. 대안
4. 가정
5. 리스크
6. 재검토 조건
7. 반영 문서
8. 출처

## 규칙

- 사용자가 명시하지 않는 한 `status`는 `draft`로 둔다.
- Raw 출처를 링크한다.
- 영향을 받는 Planning/Technical 문서를 링크한다.
- 근거 없는 rationale을 만들지 않는다.
- 기획서나 Raw에 없는 내용을 확정하지 않는다.
- 후보 상태의 결정을 `selected`로 바꾸지 않는다.
- Decision 초안은 공식 Decision이 아니며 사람 검토가 필요하다.

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
