---
name: kb-publish
description: Google Drive나 외부 리뷰어 공유용 stable view를 LLM 없이 생성한다. 00_START_HERE, 10_PLANNING, 20_TECHNICAL, 30_DECISIONS 중심으로 Raw를 제외한 배포본을 만들 때 사용한다.
tags:
  - skill
  - publish
  - stable-view
compatibility: Python 3.11 이상, 외부 패키지 불필요
---

# KB Publish

이 skill은 공유 가능한 stable view를 deterministic하게 생성한다.

## 기본 원칙

- 기본 배포 대상은 `README.md`, `00_START_HERE`, `10_PLANNING`, `20_TECHNICAL`, `30_DECISIONS`다.
- `40_RAW`는 기본적으로 제외한다.
- Raw 요약을 포함하려면 명시적으로 옵션을 사용한다.
- 이 작업은 문서를 요약하거나 수정하지 않고 복사한다.

## Stable view 생성

```bash
uv run python skills/kb-publish/scripts/build_stable_view.py . --output "dist/stable-view" --clean
```

Raw 기획서 요약도 포함:

```bash
uv run python skills/kb-publish/scripts/build_stable_view.py . --output "dist/stable-view" --include-raw-summary --clean
```

생성된 `dist/stable-view`를 Google Drive나 외부 공유용으로 업로드한다.
