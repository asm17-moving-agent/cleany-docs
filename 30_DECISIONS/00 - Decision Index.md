---
status: draft
---

# 결정 인덱스(Decision Index)

실제 Decision 문서와 현재 status만 표시한다. 아직 문서가 없는 결정 후보와 열린
질문은 Planning·Technical Questions에서 관리한다. `reviewed`·`selected` 승격의
검토자와 승인 이력은 GitHub PR에 남긴다.

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
| 2026-07-08 | [안전 기준과 실패 처리 정책](<Technical/260708 - 안전 기준과 실패 처리 정책.md>) | draft |
| 2026-07-14 | [4륜 Mecanum 베이스](<Technical/260714 - 4륜 메카넘 베이스.md>) | selected |
| 2026-07-14 | [Jetson Orin NX 16GB](<Technical/260714 - Jetson Orin NX 16GB.md>) | selected |
| 2026-07-15 | [로봇 프레임 구조](<Technical/260715 - 로봇 프레임 구조.md>) | draft |
| 2026-08-06 | [Task Planning과 Robot Capability 경계](<Technical/260806 - Task Planning과 Robot Capability 경계.md>) | draft |

## 상태 해석

- `draft`: 선택안 또는 선택지가 있으나 PR 사람 검토 전
- `reviewed`: 사람이 검토했으나 최종 채택 전
- `selected`: 현재 Source of Truth인 채택 결정
- `dropped`: 사용하지 않거나 다른 Decision으로 대체된 안
