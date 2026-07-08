# 기획 KB 리뷰 프롬프트

기획 KB 전체를 리뷰하라.

## 점검 항목

1. 새 팀원이 `10_PLANNING`과 `20_TECHNICAL`만 읽고 프로젝트를 이해할 수 있는가?
2. 주요 결정이 공식 문서에 반영되어 있는가?
3. Decision 문서가 Raw 출처를 가지고 있는가?
4. Raw 문서가 확정 결정처럼 취급되고 있지 않은가?
5. 공식 문서와 Decision 사이에 충돌이 있는가?
6. 오래되었거나 중복된 설명이 있는가?
7. Planning 문서에 기술 상세가 과하게 들어가 있지 않은가?
8. Technical 문서에 제품 narrative가 과하게 들어가 있지 않은가?
9. `status: draft` 또는 `review_status: needs-human-review` 문서가 공식 문서처럼 사용되고 있지 않은가?
10. 기획서 기반으로 작성된 내용과 임의 보강된 내용이 구분되어 있는가?

## 출력

- Blocking Issues
- Suggested Edits
- 업데이트가 필요한 문서
- `10_PLANNING/08 - Questions.md`에 추가할 질문

## 규칙

- 문서 충돌을 임의로 해결하지 않는다.
- 해결되지 않은 내용은 질문으로 남긴다.
- Raw와 draft metadata 문서를 공식 문서처럼 취급하지 않는다.
- 기획서에 없는 내용을 새 사실로 만들지 않는다.
- 공식 문서를 직접 수정하지 않고 리뷰 결과를 먼저 제시한다.

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
