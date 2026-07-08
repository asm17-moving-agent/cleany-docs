---
name: kb-maintenance
description: 끌리니 Markdown KB를 LLM 없이 정비한다. formatting normalize, 파일 색인 생성, YAML metadata report 같은 deterministic maintenance 작업에 사용한다.
tags:
  - skill
  - maintenance
  - metadata
compatibility: Python 3.11 이상, 외부 패키지 불필요
---

# KB Maintenance

이 skill은 KB 문서 관리에서 LLM이 필요 없는 반복 작업을 처리한다.

## 제공 스크립트

| 스크립트 | 역할 |
|---|---|
| `scripts/normalize_markdown.py` | Markdown 파일의 LF newline, trailing whitespace, EOF newline을 검사하거나 정리 |
| `scripts/generate_file_index.py` | 폴더별 Markdown 파일 색인을 생성 |
| `scripts/metadata_report.py` | YAML frontmatter key를 읽어 metadata report 생성 |

## Formatting normalize

검사만 수행한다.

```bash
uv run python skills/kb-maintenance/scripts/normalize_markdown.py .
```

실제로 수정한다.

```bash
uv run python skills/kb-maintenance/scripts/normalize_markdown.py . --write
```

## 파일 색인 생성

stdout으로 확인한다.

```bash
uv run python skills/kb-maintenance/scripts/generate_file_index.py .
```

문서로 저장한다.

```bash
uv run python skills/kb-maintenance/scripts/generate_file_index.py . --output "00_START_HERE/04 - File Index.md"
```

## Metadata report 생성

```bash
uv run python skills/kb-maintenance/scripts/metadata_report.py . --output "40_RAW/60_External_Artifacts/metadata-report.md"
```

## 사용 원칙

- 이 skill은 문서 형식과 색인 같은 deterministic 작업만 수행한다.
- 기획/기술 판단을 자동으로 확정하지 않는다.
- 공식 문서 생성 또는 수정 후에는 `kb-quality-checks` 검사를 실행한다.
