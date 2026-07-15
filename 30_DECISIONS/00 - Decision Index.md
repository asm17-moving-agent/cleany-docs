---
type: decision-index
status: draft
reviewers:
  -
tags:
  - decision
  - index
  - draft
  - cleany
updated: 2026-07-15
---

# 결정 인덱스(Decision Index)

`selected` Decision은 사람의 확정과 검토자 기록을 근거로 관리한다. 현재 문서는 Decision 후보와 채택·폐기 상태를 추적하기 위한 인덱스다.

## Planning Decisions

| 날짜 | 결정 | 상태 |
|---|---|---|
| 2026-07-08 | [1차 타깃 무인 스터디카페](<Planning/260708 - 1차 타깃 무인 스터디카페.md>) | draft |
| 2026-07-08 | [MVP 기능 범위](<Planning/260708 - MVP 기능 범위.md>) | draft |

## Technical Decisions

| 날짜 | 결정 | 상태 |
|---|---|---|
| 2026-07-08 | [XLeRobot 기반 플랫폼](<Technical/260708 - XLeRobot 기반 플랫폼.md>) | selected |
| 2026-07-08 | [Jetson AGX Orin 64GB](<Technical/260708 - Jetson AGX Orin 64GB.md>) | dropped |
| 2026-07-08 | [Rule-based VLA 3 Layer 구조](<Technical/260708 - Rule-based VLA 3 Layer 구조.md>) | draft |
| 2026-07-08 | [안전 기준과 실패 처리 정책](<Technical/260708 - 안전 기준과 실패 처리 정책.md>) | draft |
| 2026-07-14 | [4륜 메카넘 베이스](<Technical/260714 - 4륜 메카넘 베이스.md>) | selected |
| 2026-07-14 | [Jetson Orin NX 16GB](<Technical/260714 - Jetson Orin NX 16GB.md>) | selected |
| 2026-07-15 | [로봇 프레임 구조](<Technical/260715 - 로봇 프레임 구조.md>) | draft |

## Deprecated / Superseded Decisions

| 날짜 | 결정 | 대체 문서 | 사유 |
|---|---|---|---|
| 2026-07-08 | [Jetson AGX Orin 64GB](<Technical/260708 - Jetson AGX Orin 64GB.md>) | [Jetson Orin NX 16GB](<Technical/260714 - Jetson Orin NX 16GB.md>) | 메모리 가격 상승에 따른 조달 비용 증가 |

## Decision 문서 생성 기준

Decision 문서는 아래 조건 중 2개 이상을 만족할 때만 생성한다.

- 프로젝트 방향에 영향을 준다.
- 나중에 번복하면 비용이 크다.
- Planning 또는 Technical 문서의 핵심 내용을 바꾼다.
- Sprint 계획이나 Jira Epic/Story 구조에 영향을 준다.
- 멘토나 리뷰어가 질문할 가능성이 높다.
- 기술 리스크 또는 안전 리스크에 영향을 준다.

## 초기 Decision 후보

| 후보 | 유형 | 이유 | 상태 |
|---|---|---|---|
| 1차 타깃을 무인 스터디카페로 확정할지 | planning | 기능 범위와 데모 공간에 영향 | 후보 |
| MVP 기능 범위를 어디까지 둘지 | planning | Sprint, 성공 기준, 기술 범위에 영향 | 후보 |
| XLeRobot에서 유지할 플랫폼 범위를 어디까지로 둘지 | technical | 하드웨어, 센서, 조작 범위에 영향 | selected |
| Jetson AGX Orin 64GB를 메인 컴퓨팅으로 확정할지 | technical | 성능, 비용, 개발환경에 영향 | dropped |
| Jetson Orin NX 16GB를 메인 컴퓨팅으로 사용할지 | technical | 비용, 메모리 예산, 개발환경에 영향 | selected |
| Rule-based VLA의 3 Layer 구조를 어떻게 정의할지 | technical | 판단 구조와 평가 방식에 영향 | 후보 |
| 안전 기준과 실패 처리 정책을 어떻게 둘지 | technical | 데모 안정성과 상용화 리스크에 영향 | 후보 |
| 4륜 Mecanum custom base를 사용할지 | technical | BOM, kinematics, robot description과 제어 계약에 영향 | selected |
| 로봇 프레임을 RÅSKOG와 알루미늄 프로파일 중 무엇으로 구성할지 | technical | 매니퓰레이터 도달 범위, 작업 높이, 조립과 기구학 복잡도에 영향 | 후보 |

## 운영 규칙

- 후보는 확정 결정이 아니다.
- `selected` 상태가 된 Decision만 공식 결정으로 취급한다.
- Decision 문서는 관련 Raw 출처와 반영 문서를 반드시 연결한다.
- Raw에서 Decision 초안을 만들 때는 `$kb-ingest` skill prompt를 사용한다.
- Decision 초안은 `status: draft`, 빈 `reviewers`, `tags`로 검토 상태를 표시한다. 검토 후에는 reviewer를 기록하고 `reviewed` 또는 `selected`로 바꾼다.
