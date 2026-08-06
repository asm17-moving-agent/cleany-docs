# 범위와 제외 범위(Scope and Non-Goals)

## 요약

1차 MVP는 무인 스터디카페의 개별 좌석을 대상으로, Dashboard 요청부터 로봇의
왕복 이동, 책상 위 물체 처리, 전후 결과 표시까지 연결하는 E2E 데모다.

## In Scope

| 영역 | 포함 범위 |
|---|---|
| 운영 흐름 | Dashboard 수동 요청, Backend 전달, 진행 상태와 최종 결과 표시 |
| 작업 단위 | 운영자가 지정한 개별 좌석의 책상 한 곳 |
| Navigation | 사전 제작 지도에서 대기 위치와 대상 좌석 사이 자율 왕복 |
| 관찰 | 책상 작업 전후 RGB-D 기반 장면 기록 |
| 판단 | 책상 위 여러 물체의 의미, 처리 가능 여부, 작업 순서 판단 |
| 조작 | 허용된 쓰레기 후보를 집어 로봇 탑재 수거함에 투입 |
| 결과 | 성공, 실패, 미처리 대상과 전후 관찰 전달 |
| 검증 | Rule-based 통합 검증 후 AI 계획과 물리 실행 검증 |

분실물 후보는 인식 범위에 포함하지만 물리적 처리 행동은 아직 MVP 범위로
확정하지 않는다.

## Non-Goals

- 데모 중 새로운 지도를 만드는 Mapping 기능
- 의자 정렬, 바닥 청소, 책상 닦기, 소등과 문단속
- 모든 무인점포 유형과 모든 물체를 처리하는 범용 로봇
- 자연어로 임의의 로봇 행동을 생성하는 범용 명령 인터페이스
- 사람이 함께 있는 공간에서의 자율 운영
- 상용 규모의 다점포 관제, 배포, 과금 기능

## 범위 변경 기준

현재 범위를 줄이거나 분실물 처리처럼 새 행동을 넣으려면 Target Scenario와 Success
Criteria를 함께 변경하고 별도 팀 승인을 남긴다. 일정과 담당자는 이 KB가 아니라
Jira에서 관리한다.

## 관련 문서

- [Target Scenario](<02 - Target Scenario.md>)
- [Success Criteria](<05 - Success Criteria.md>)
- [Verification and Simulation Strategy](<../20_TECHNICAL/13 - Verification and Simulation Strategy.md>)

## 출처

- [기획서 원문 요약](<../40_RAW/기획서 원문 요약.md>)

## 관련 결정

- [260708 - MVP 기능 범위](<../30_DECISIONS/Planning/260708 - MVP 기능 범위.md>)
