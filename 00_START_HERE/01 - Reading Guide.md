---
type: reading-guide
status: draft
reviewers:
  -
tags:
  - start-here
  - reading-guide
  - cleany
updated: 2026-07-08
---

# 읽기 가이드(Reading Guide)

## 1. 시간이 15분밖에 없을 때

1. [[10_PLANNING/00 - Project Brief|Project Brief]]
2. [[10_PLANNING/02 - Target Scenario|Target Scenario]]
3. [[10_PLANNING/99 - Questions|Planning Questions]]
4. [[20_TECHNICAL/99 - Questions|Technical Questions]]
5. [[30_DECISIONS/00 - Decision Index|Decision Index]]

이 순서로 읽으면 프로젝트가 무엇이고, 아직 무엇이 정해지지 않았는지 빠르게 파악할 수 있다.

## 2. 기획 리뷰를 해야 할 때

1. [[10_PLANNING/00 - Project Brief|Project Brief]]
2. [[10_PLANNING/01 - Problem and Users|Problem and Users]]
3. [[10_PLANNING/02 - Target Scenario|Target Scenario]]
4. [[10_PLANNING/04 - Scope and Non-Goals|Scope and Non-Goals]]
5. [[10_PLANNING/05 - Success Criteria|Success Criteria]]
6. [[10_PLANNING/99 - Questions|Planning Questions]]
7. [[40_RAW/20_Planning/기획서 원문 요약|기획서 원문 요약]]

읽으면서 확인할 것은 세 가지다.

- 기획서 원문에 없는 내용이 확정처럼 쓰였는가?
- MVP 범위와 성공 기준이 충분히 좁혀졌는가?
- 질문으로 남겨야 할 충돌이나 빈 항목이 있는가?

## 3. 기술 리뷰를 해야 할 때

1. [[20_TECHNICAL/00 - Technical Overview|Technical Overview]]
2. [[20_TECHNICAL/01 - System Concept|System Concept]]
3. [[20_TECHNICAL/03 - Rule-based VLA Architecture|Rule-based VLA Architecture]]
4. [[20_TECHNICAL/04 - Robot Platform XLeRobot|Robot Platform XLeRobot]]
5. [[20_TECHNICAL/05 - Navigation and Mapping|Navigation and Mapping]]
6. [[20_TECHNICAL/06 - Edge Runtime Jetson Orin|Edge Runtime Jetson Orin]]
7. [[20_TECHNICAL/07 - Data and Evaluation|Data and Evaluation]]
8. [[20_TECHNICAL/08 - Safety and Risk|Safety and Risk]]
9. [[20_TECHNICAL/99 - Questions|Technical Questions]]

읽으면서 확인할 것은 세 가지다.

- 기획 범위에 비해 기술 범위가 과하게 넓지 않은가?
- 하드웨어, 런타임, 모델 후보가 검증된 사실과 가정을 구분하고 있는가?
- 안전 기준과 실패 처리 정책이 평가 지표와 연결되는가?

## 4. Sprint 계획을 잡아야 할 때

1. [[10_PLANNING/99 - Questions|Planning Questions]]
2. [[20_TECHNICAL/99 - Questions|Technical Questions]]
3. [[10_PLANNING/05 - Success Criteria|Success Criteria]]
4. [[20_TECHNICAL/08 - Safety and Risk|Safety and Risk]]
5. [[30_DECISIONS/00 - Decision Index|Decision Index]]

Sprint 목표는 확정된 결정과 검토 대기 항목을 분리해서 잡는다. Jira issue에는 문서 본문을 붙여 넣지 않고 관련 문서 링크만 둔다.

## 5. Decision을 추적해야 할 때

1. [[30_DECISIONS/00 - Decision Index|Decision Index]]
2. `30_DECISIONS/Planning/`의 Planning Decision 문서
3. `30_DECISIONS/Technical/`의 Technical Decision 문서
4. 관련 `10_PLANNING` 또는 `20_TECHNICAL` 문서
5. 관련 `40_RAW` 원본 기록

Decision 후보와 초안 상태는 [[30_DECISIONS/00 - Decision Index|Decision Index]], [[10_PLANNING/99 - Questions|Planning Questions]], [[20_TECHNICAL/99 - Questions|Technical Questions]]에서 함께 확인한다.

## 6. 외부 공유 전에

1. `draft` 문서를 그대로 공식 결론처럼 공유하지 않는다. `reviewed` 이상 문서는 `reviewers`를 함께 확인한다.
2. Raw 전체를 공유하지 않는다.
3. 공유 전 `$kb-quality-checks`, `$kb-audit`, `$kb-review-pack`을 실행한다.

## 7. Codex 작업 흐름을 확인해야 할 때

1. `AGENTS.md`에서 저장소 작업 규칙을 확인한다.
2. `skills/README.md`에서 사용 가능한 repo skill 목록을 확인한다.
3. 반복 작업은 `.codex/prompts`가 아니라 `$skill-name` 형식의 repo skill prompt로 요청한다.
4. skill이나 검사 스크립트를 바꾼 뒤에는 `$kb-quality-checks`를 실행한다.
