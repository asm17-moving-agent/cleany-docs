# Skills

이 폴더는 끌리니 기획 KB에서 LLM을 거치지 않고 처리할 수 있는 deterministic 작업을 모아둔 skill 원본과 실행 스크립트 위치다.

Codex가 자동 탐지하는 repo-scoped skill 위치는 `.agents/skills`이다. 현재 `.agents/skills/<skill-name>`은 이 폴더의 `skills/<skill-name>`을 가리키는 symlink로 관리한다.

## 운영 원칙

- 기획/기술 판단은 skill이 자동 확정하지 않는다.
- 변환, 정리, 검사, 색인처럼 규칙으로 처리 가능한 작업만 script로 수행한다.
- Codex 문서 작성 워크플로우에서는 직접 하위 Python 실행 명령을 작성하지 않고 `$skill-name` 형식의 skill prompt를 사용한다.
- 문서 변경 후에는 `$kb-quality-checks` skill prompt로 검사를 요청한다.

## Skillsets

| Skill | Codex entrypoint | 스크립트 원본 | 역할 |
|---|---|---|---|
| `office-to-markdown` | `.agents/skills/office-to-markdown` | `skills/office-to-markdown` | DOCX, PPTX, XLSX, PDF를 Markdown으로 변환 |
| `kb-doc-factory` | `.agents/skills/kb-doc-factory` | `skills/kb-doc-factory` | 템플릿 기반 Planning/Technical/Decision/회의록 문서 생성 |
| `kb-maintenance` | `.agents/skills/kb-maintenance` | `skills/kb-maintenance` | Markdown normalize, 파일 색인, metadata report 생성 |
| `kb-ingest` | `.agents/skills/kb-ingest` | `skills/kb-ingest` | Raw 회의록/조사자료를 Planning/Decision 초안으로 변환 |
| `kb-audit` | `.agents/skills/kb-audit` | `skills/kb-audit` | 검토 플래그, source_refs, Decision inventory 리포트 생성 |
| `kb-publish` | `.agents/skills/kb-publish` | `skills/kb-publish` | Google Drive/외부 공유용 stable view 생성 |
| `kb-quality-checks` | `.agents/skills/kb-quality-checks` | `skills/kb-quality-checks` | 구조, formatting, metadata, 링크, prompt 검사 |

## 기본 skill prompt 예시

Office/PDF 변환:

```text
$office-to-markdown "파일.docx"를 Markdown으로 변환해 "40_RAW/00_Inbox/파일 변환.md"에 저장해. 요약이나 해석은 하지 마.
```

문서 생성:

```text
$kb-doc-factory decision 문서 "MVP 범위 확정" 초안을 planning decision으로 생성해.
```

Raw → Planning/Decision 변환:

```text
$kb-ingest "40_RAW/10_Meetings/YYMMDD - MVP 범위 회의.md"를 근거로 Planning 반영 후보와 Decision 초안을 만들어. 별도 working 폴더를 만들지 말고 YAML metadata로 상태를 표시해.
```

KB 정비:

```text
$kb-maintenance Markdown formatting을 정리하고 필요한 metadata report를 생성해.
```

Audit 리포트:

```text
$kb-audit 전체 audit 리포트를 "40_RAW/60_External_Artifacts/audit" 아래에 생성해.
```

Stable view 생성:

```text
$kb-publish 외부 공유용 stable view를 "dist/stable-view"에 생성해. Raw는 기본 제외해.
```

품질 검사:

```text
$kb-quality-checks 이 저장소의 전체 결정적 검사를 실행하고 실패 항목을 요약해.
```
