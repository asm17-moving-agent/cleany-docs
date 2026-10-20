---
date: 2026-10-17
---

# 261017 - FSM과 BT Runtime 기준 Supervisor 통합

## 결정

FSM+BT Mission Runtime을 기준으로 System Supervisor를 통합한다. 상위 FSM은 수락,
이동, 작업, 복귀와 보고를 소유하고 청소 BT는 관찰, 행동 제안, 하나의 실행과 재관찰을
소유한다. Supervisor는 별도의 가용성, Fault, 실행 허가와 복구 조정 경계를 유지한다.

## 이유

KB 최신화 중 두 Mission 구현의 통합 기준을 질문했고, 사용자가 FSM+BT Runtime을
기준으로 지정했다. 이 기록은 이번 통합 기준 선택을 보존한다. 과거에 FSM+BT를
처음 도입한 이유와 비교했던 대안은 추가 확인이 필요하다.

## 대안의 처리

순차 FSM에 Supervisor bridge를 붙인 브랜치는 허가, 중단 계약의 구현 근거로 유지한다.
해당 순차 FSM을 통합의 기준 Runtime으로 삼는 방식은 이번 선택에서 채택하지 않는다.
별도의 성능 비교나 팀 회의가 있었다고 추정하지 않는다.

## 결과

- Runtime의 Gateway, journal, 청소 BT와 조작 결과, 주행 gate를 보존하면서 Supervisor
  허가 취득, 갱신, 철회와 실제 중단 확인을 연결해야 한다.
- Supervisor 복구 성공이 BT나 미션의 자동 재개를 뜻하지 않는다. 재개 전 상태와
  최신 관찰의 재검증은 Mission이 소유한다.
- 두 브랜치의 인터페이스가 이미 호환되거나 통합됐다는 뜻이 아니다. 통합, 검증은 남아 있다.
- 기존 Supervisor 책임 및 독립 안전 경계는 유지한다.

## 재검토 조건

통합 과정에서 실행 허가, 중단 완료와 재개 의미를 보존할 수 없으면 근거를 남겨
기준과 adapter 책임을 재검토한다.

## 출처

- [기술 KB 구현 대조와 사용자 결정](<../../40_RAW/261017 - 기술 KB 구현 대조와 사용자 결정.md>)
- [System Supervisor 설계 지시](<../../40_RAW/261016 - System Supervisor 설계 지시.md>)
- [FSM과 BT Runtime 계약 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_interfaces/docs/mission.md)
- [기존 Supervisor 구현 at c63fadb](https://github.com/asm17-moving-agent/cleany/blob/c63fadb467afac08cc62a3cfd0a5af7c59b6e8b7/ros2_ws/src/cleany_system_supervisor/README.md)
