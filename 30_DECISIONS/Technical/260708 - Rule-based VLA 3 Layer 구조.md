---
type: decision
decision_type: technical
status: draft
reviewers:
  -
tags:
  - decision
  - draft
  - technical
  - vla
  - cleany
date: 2026-07-08
impact: high
source_refs:
  - "40_RAW/20_Planning/기획서 원문 요약.md"
related_jira:
  -
supersedes:
superseded_by:
updated: 2026-07-08
---

# 260708 - Rule-based VLA 3 Layer 구조

## 1. 결정

Rule-based VLA의 3 Layer 구조와 각 계층 책임을 확정하기 위한 Technical Decision 초안이다. 사람 검토 전이므로 아직 확정 결정이 아니다.

## 2. 이유

- Raw 요약에는 `3 Layer Rule-based VLA 작업 계획`이 포함되어 있다.
- VLA 판단 구조는 객체 의미 해석, 행동 후보 생성, 규칙 기반 검증, 실행 정책, 평가 기준에 영향을 준다.
- 계층 책임이 불명확하면 구현 범위와 실패 처리 기준을 정하기 어렵다.

## 3. 대안

| 대안                                                                       | 선택하지 않은 이유                            |
| ------------------------------------------------------------------------ | ------------------------------------- |
| Perception, Semantic/Action Candidate, Rule Validation/Execution 계층으로 둔다 | 현재 기술 문서의 초안과 맞지만 공식 명칭과 책임 검토가 필요하다. |
| VLA가 행동 결정을 직접 내리도록 한다                                                   | 안전 규칙과 디버깅 기준이 약해질 수 있다.              |
| 순수 rule-based 구조로 제한한다                                                   | 물체 의미와 주변 맥락 해석의 유연성이 부족할 수 있다.       |

## 4. 가정

- VLA 판단은 긴 주기로 행동 후보를 만들고, 실행은 짧은 주기로 수행한다.
- 모든 행동은 규칙 기반 검증을 통과해야 실행된다.
- 불확실하거나 위험한 경우 대기 또는 운영자 확인으로 빠지는 정책이 필요하다.

## 5. 리스크

- 계층 간 책임이 겹치면 디버깅과 평가가 어려워진다.
- 규칙이 단순하면 실제 상황 대응력이 낮고, 복잡하면 유지보수가 어려워진다.
- VLA 판단 근거가 불투명하면 안전 검토가 어려울 수 있다.

## 6. 재검토 조건

- VLA 후보 모델과 경량 VLM 후보가 확정된다.
- 실제 시나리오에서 규칙 기반 검증이 너무 많은 false positive 또는 false negative를 만든다.
- 안전 기준과 실패 처리 정책이 더 엄격한 구조를 요구한다.

## 7. 출처

- [[40_RAW/20_Planning/기획서 원문 요약|기획서 원문 요약]]
