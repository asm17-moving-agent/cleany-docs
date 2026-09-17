---
ingest_targets:
  - technical
decision_candidates: []
date: 2026-08-26
source_type: personal-learning-index
---

# 260826 - ROS 2 자율주행 스택 학습

## 1. 목적과 범위

이 묶음은 실내 모바일 로봇이 목표 pose를 받아 이동하고 도착 결과를 반환하기까지의
ROS 2 자율주행 스택을 큰 흐름부터 학습하는 공간이다.

- `40_RAW`의 개인 학습 기록이며 공식 기술 기준이나 Decision이 아니다.
- 2D LiDAR 기반 Mapping, Localization과 Nav2 주행을 중심으로 본다.
- 센서, TF, Odometry와 모바일 베이스는 자율주행 흐름을 이해하는 범위에서 다룬다.
- Dashboard 관제와 책상 위 Perception, Manipulation은 Navigation 경계만 확인한다.
- 특정 알고리즘, 패키지와 파라미터를 이 문서 묶음에서 확정하지 않는다.

## 2. 전체 흐름

```text
목표 pose
  → Navigation 실행 조정
  → 경로 계획
  → 경로 추종과 장애물 회피
  → 차체 속도 명령
  → 모바일 베이스 이동
  → 센서와 Odometry 갱신
  → 지도 또는 현재 위치 보정
  → 다음 제어 주기
```

SLAM은 이 흐름 전체가 아니라 센서와 Odometry를 사용해 지도와 전역 위치 관계를
만드는 한 부분이다. 세부 책임과 데이터 흐름은
[자율주행 스택 전체 흐름](<01 - 자율주행 스택 전체 흐름.md>)에서 정리한다.

## 3. 문서 지도

| 문서 | 중심 내용 |
|---|---|
| [자율주행 스택 전체 흐름](<01 - 자율주행 스택 전체 흐름.md>) | 센서부터 구동까지의 폐루프와 계층별 책임 |
| [SLAM과 Localization](<02 - SLAM과 Localization.md>) | 지도 작성, 지도 관리와 전역 위치 추정 |
| [Nav2 주행](<03 - Nav2 주행.md>) | Costmap, 경로 계획, 제어, 실행 조정과 복구 |
| [Cleany 적용과 검증](<04 - Cleany 적용과 검증.md>) | 좌석 이동 흐름, ROS interface와 단계별 실험 기록 |

권장 순서는 `01 → 02 → 03 → 04`다. 필요한 개념은 앞 문서로 돌아가 보완한다.

## 4. 작성과 분리 원칙

- 새 학습 내용은 먼저 가장 가까운 기존 문서의 하위 절에 추가한다.
- 사실, 개인 해석과 직접 실행한 결과를 구분하고 사실에는 출처와 확인일을 남긴다.
- 실행 결과에는 환경, 입력, 파라미터, 관찰 결과와 원본 artifact 위치를 함께 남긴다.
- 내용이 커져 독립적인 읽기 순서나 별도 실험 이력이 필요해지면 사용자 요청 후 분리한다.
- 첨부 자료가 생기면 이 묶음의 `assets/`에 두고 문서에서 링크한다.

## 5. 관련 KB 기준

- [내비게이션과 매핑](<../../20_TECHNICAL/05 - Navigation and Mapping.md>)
- [Robot ROS Contract](<../../20_TECHNICAL/10 - Robot ROS Contract.md>)
- [Hardware Configuration](<../../20_TECHNICAL/12 - Hardware Configuration.md>)
- [Verification and Simulation Strategy](<../../20_TECHNICAL/13 - Verification and Simulation Strategy.md>)
