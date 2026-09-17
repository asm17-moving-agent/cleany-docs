---
ingest_targets:
  - technical
decision_candidates: []
date: 2026-08-26
source_type: personal-learning
---

# 260826 - SLAM과 Localization

## 1. 학습 목표

SLAM으로 지도를 만드는 단계와 이미 만든 지도에서 현재 위치를 찾는 운영 단계를
구분한다. 두 단계가 공유하는 sensor와 TF, 서로 다른 출력과 실패 형태를 함께
정리한다.

## 2. 두 실행 모드

| 구분 | 주된 입력 | 주된 출력 | 목적 |
|---|---|---|---|
| Mapping, SLAM | LiDAR scan, Odometry와 TF | 지도, pose graph와 `map → odom` | 환경 지도를 만들고 일관된 trajectory 추정 |
| Localization | 저장된 지도, LiDAR scan, Odometry와 TF | 지도 기준 robot pose와 `map → odom` | 지도를 바꾸지 않고 현재 위치 추정 |

Cleany의 현재 공식 기준은 지도를 데모 전에 제작하고 검증하는 것이다. 따라서
Mapping은 환경 준비 과정으로, 운영 주행은 저장된 지도 기반 Localization으로
나누어 학습한다.

## 3. SLAM의 큰 흐름

```text
LiDAR scan + Odometry + TF
  → 전처리와 유효 관측 선택
  → Scan matching과 상대 pose 추정
  → Pose graph에 node와 constraint 추가
  → 재방문 후보와 loop closure 확인
  → Graph 최적화
  → 보정된 pose, 지도와 map → odom 출력
```

### 3.1 채워갈 개념

| 개념 | 확인할 질문 | 학습 기록 |
|---|---|---|
| Scan matching | 현재 scan을 무엇과 비교해 상대 이동을 구하는가? | 작성 예정 |
| Pose graph | Node와 constraint는 각각 무엇을 나타내는가? | 작성 예정 |
| Loop closure | 같은 장소의 재방문을 어떻게 판별하고 검증하는가? | 작성 예정 |
| Optimization | 누적 오차를 어떤 목적 함수로 줄이는가? | 작성 예정 |
| Occupancy grid | 관측을 free, occupied와 unknown cell로 어떻게 바꾸는가? | 작성 예정 |

## 4. Localization의 큰 흐름

```text
저장된 지도 + 초기 pose 후보
  → LiDAR 관측과 지도 비교
  → Odometry로 짧은 시간의 이동 예측
  → 지도 기준 pose와 불확실성 갱신
  → map → odom 발행
  → 위치 추정 품질을 Nav2에 제공
```

AMCL과 SLAM Toolbox의 Localization mode는 비교 가능한 후보지만 이 문서에서 하나를
미리 선택하지 않는다. 같은 sensor, map, trajectory와 평가 지표로 비교한 뒤
Cleany 적용 여부를 별도로 검토한다.

## 5. 학습과 실험 기록

### 5.1 비교 기준

| 항목 | 후보 A | 후보 B | 근거 또는 실측 |
|---|---|---|---|
| 필요한 입력과 TF | 작성 예정 | 작성 예정 | 작성 예정 |
| 초기 pose와 재위치 추정 | 작성 예정 | 작성 예정 | 작성 예정 |
| 지도 저장과 재사용 | 작성 예정 | 작성 예정 | 작성 예정 |
| Odometry 오차 민감도 | 작성 예정 | 작성 예정 | 작성 예정 |
| CPU, memory와 지연시간 | 작성 예정 | 작성 예정 | 작성 예정 |
| 실패 감지와 복구 방법 | 작성 예정 | 작성 예정 | 작성 예정 |

### 5.2 실행 기록

| 항목 | 기록 |
|---|---|
| 날짜와 환경 | 작성 예정 |
| 패키지와 버전 | 작성 예정 |
| 센서, map과 trajectory | 작성 예정 |
| 주요 파라미터 | 작성 예정 |
| 위치와 지도 품질 지표 | 작성 예정 |
| 실패와 한계 | 작성 예정 |
| 원본 artifact 위치 | 작성 예정 |

## 6. 출처

- [SLAM Toolbox 공식 저장소](https://github.com/SteveMacenski/slam_toolbox)
- [Nav2 Mapping and Localization](https://docs.nav2.org/setup_guides/sensors/mapping_localization.html)
- [내비게이션과 매핑](<../../20_TECHNICAL/05 - Navigation and Mapping.md>)
- [Robot ROS Contract](<../../20_TECHNICAL/10 - Robot ROS Contract.md>)

## 7. 주의점

- 좋은 지도 모양과 정확한 trajectory를 같은 지표로 취급하지 않는다.
- 단일 실행 결과를 알고리즘의 일반 성능으로 해석하지 않는다.
- Simulation noise와 실제 LiDAR 오차를 같은 근거로 취급하지 않는다.
- 지도 작성 성공을 운영 Localization과 Navigation 성공으로 확대 해석하지 않는다.
