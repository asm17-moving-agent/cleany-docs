---
name: office-to-markdown
description: DOCX, PPTX, XLSX, PDF 파일을 LLM 없이 결정적으로 읽어 Markdown으로 변환한다. 기획서, 발표자료, 스프레드시트, 외부 산출물을 Raw 문서로 ingest할 때 사용한다.
tags:
  - skill
  - raw
  - conversion
compatibility: Python 3.11 이상, uv project dependencies 사용
---

# Office to Markdown

이 skill은 Office 계열 파일과 PDF를 LLM 없이 Markdown으로 변환한다.

## 지원 형식

| 형식 | 처리 내용 |
|---|---|
| `.docx` | 문단, 제목 스타일, 목록 스타일, 표 |
| `.pptx` | 슬라이드 제목, 텍스트 박스, 표 |
| `.xlsx` | 시트별 표 데이터 |
| `.pdf` | 페이지별 텍스트 추출 |

## 사용 원칙

- 변환은 deterministic하게 수행한다.
- 내용을 요약하거나 해석하지 않는다.
- 원문에 없는 내용을 추가하지 않는다.
- 변환 결과는 기본적으로 Raw 또는 Working 계층에 둔다.
- 변환 후 공식 문서 반영 여부는 사람 검토를 거친다.

## 단일 파일 변환

저장소 루트에서 실행한다.

```bash
uv run python skills/office-to-markdown/scripts/office_to_markdown.py "40_RAW/00_Inbox/[기획서] AI 에이전트는 움직이고 싶어(3).docx" --output "40_RAW/20_Planning/기획서 원문 변환.md"
```

stdout으로 확인하려면 `--output`을 생략한다.

```bash
uv run python skills/office-to-markdown/scripts/office_to_markdown.py "파일.docx"
```

## 폴더 일괄 변환

```bash
uv run python skills/office-to-markdown/scripts/office_to_markdown.py "40_RAW/00_Inbox" --output "40_RAW/00_Inbox/converted"
```

입력이 폴더인 경우 `--output`은 출력 폴더로 해석된다.

## 출력 frontmatter

기본 출력에는 아래 YAML metadata가 포함된다.

```yaml
---
type: raw-converted
source_file: "원본 파일명"
source_format: "docx"
converter: office-to-markdown
review_status: needs-human-review
---
```

frontmatter가 필요 없으면 `--no-frontmatter`를 사용한다.

## 한계

- 이미지 OCR은 수행하지 않는다.
- DOCX/PPTX의 복잡한 레이아웃은 완전히 보존하지 않는다.
- PDF는 텍스트 추출 가능한 문서만 안정적으로 처리한다.
- 표 병합 셀은 단순 텍스트 표로 평탄화한다.
