---
name: kb-audit
description: 끌리니 KB의 검토 필요 항목, source_refs, Decision inventory를 LLM 없이 리포트로 생성한다. 리뷰 준비와 문서 품질 점검에 사용한다.
tags:
  - skill
  - audit
  - report
compatibility: Python 3.11 이상, 외부 패키지 불필요
---

# KB Audit

이 skill은 KB 상태를 deterministic report로 만든다.

## 제공 리포트

| 스크립트 | 역할 |
|---|---|
| `scripts/review_flags_report.py` | `검토 필요`, `추가 확인 필요`, `placeholder`, `미정` 등 검토 플래그 수집 |
| `scripts/source_refs_report.py` | Planning/Technical/Decision 문서의 source_refs 상태 점검 |
| `scripts/decision_inventory.py` | Decision 문서 inventory 생성 |
| `scripts/audit_all.py` | 위 리포트를 한 번에 생성 |

## 전체 audit 실행

```bash
uv run python skills/kb-audit/scripts/audit_all.py .
```

기본 실행은 파일을 생성하지 않고 stdout으로 Markdown audit 결과를 출력한다. Codex는 이 출력을 그대로 읽어 요약한다.

## 전체 audit 파일 생성

파일 리포트가 명시적으로 필요할 때만 `--output-dir`를 사용한다.

```bash
uv run python skills/kb-audit/scripts/audit_all.py . --output-dir "40_RAW/60_External_Artifacts/audit"
```

## 개별 리포트

```bash
uv run python skills/kb-audit/scripts/review_flags_report.py . --output "40_RAW/60_External_Artifacts/audit/review-flags.md"
uv run python skills/kb-audit/scripts/source_refs_report.py . --output "40_RAW/60_External_Artifacts/audit/source-refs-report.md"
uv run python skills/kb-audit/scripts/decision_inventory.py . --output "40_RAW/60_External_Artifacts/audit/decision-inventory.md"
```

## 사용 원칙

- 리포트는 상태 점검 결과이며 공식 결정이 아니다.
- 플래그 발견은 자동 수정이 아니라 사람 검토 대상으로 연결한다.
- 문서 수정 후에는 `kb-quality-checks`를 실행한다.
