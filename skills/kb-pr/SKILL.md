---
name: kb-pr
description: 끌리니 KB 변경사항을 검토, 검증, 커밋, push, draft PR 생성까지 진행한다. 사용자가 $kb-pr로 PR 생성, 변경사항 발행, GitHub PR 열기를 요청할 때 사용한다.
tags:
  - skill
  - pr
  - github
  - publish
---

# KB PR

이 skill은 끌리니 KB 저장소의 변경사항을 GitHub draft PR로 발행하는 절차다.

## 원칙

- PR 생성은 사용자가 `$kb-pr`를 명시했을 때만 수행한다.
- 먼저 `git status -sb`와 diff를 확인해 PR 범위를 파악한다.
- unrelated change가 있으면 전체 staging을 하지 않고 사용자에게 포함 범위를 확인한다.
- 문서 변경이 포함되어 있으면 push 전 `$kb-quality-checks` 전체 검사를 실행한다.
- 기본 PR은 draft로 생성한다. 사용자가 명시적으로 요청한 경우에만 ready-for-review로 만든다.
- 문서 본문을 PR 설명에 과도하게 복붙하지 않고 변경 요약과 검증 결과를 적는다.

## Workflow

1. 현재 상태 확인
   - `git status -sb`
   - 필요한 경우 `git diff --stat`, `git diff`, `git diff --cached`
2. PR 범위 확정
   - 변경 파일이 모두 같은 작업에 속하면 그 범위를 요약한다.
   - 섞인 변경사항이 있으면 어떤 파일을 포함할지 확인한다.
3. 검증
   - 문서, 템플릿, prompt, skill, 검사 스크립트 변경이 있으면 실행한다.
   - `uv run python skills/kb-quality-checks/scripts/run_checks.py .`
4. 커밋
   - 확정된 파일만 stage한다.
   - 커밋 메시지는 변경 내용을 짧게 설명한다.
5. Push 및 draft PR 생성
   - `git push -u origin $(git branch --show-current)`
   - GitHub app 또는 `gh pr create --draft`를 사용한다.

## PR 설명

PR 본문에는 아래 항목을 포함한다.

- 변경 내용
- 변경 이유
- 사람 검토가 필요한 항목
- 실행한 검사와 결과

## 중단 조건

- GitHub remote나 인증 상태를 확인할 수 없을 때
- unrelated change가 섞여 있는데 포함 범위를 확정할 수 없을 때
- `$kb-quality-checks`가 실패했고 실패를 수정하거나 명시적으로 보류할 수 없을 때
- 사용자가 draft가 아닌 PR을 요구했지만 검토 상태가 불명확할 때
