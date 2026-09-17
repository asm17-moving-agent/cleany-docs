---
ingest_targets:
  - technical
decision_candidates: []
date: 2026-08-26
source_type: personal-learning
---

# 260826 - Cleany 적용과 검증

## 1. 목적과 현재 경계

일반적인 자율주행 스택의 개념을 Cleany의 좌석 이동과 복귀 흐름에 연결하고,
구조 확인과 실제 실행 증거를 구분해 기록한다.

현재 KB 기준에서 Mapping은 데모 전에 수행하는 환경 준비 단계다. 운영 중에는
저장된 지도에서 위치를 추정하고, Backend의 좌석 ID를 Robot이 사용할 목표 pose로
해석해 Nav2에 전달하는 흐름을 전제로 한다.

```text
좌석 ID
  → 접근 pose 조회
  → Nav2 goal
  → Localization, Planning과 Control
  → 좌석 도착 결과
  → 책상 작업
  → 대기 위치 Nav2 goal
  → 복귀 결과
```

## 2. Cleany Navigation 계약

### 2.1 주요 topic과 action

| 경계 | 메시지 또는 의미 | 확인할 소유자 |
|---|---|---|
| 상위 Navigation | `NavigateToPose` 또는 동등한 action | Navigator와 Nav2 |
| Base command | `cmd_vel`, `geometry_msgs/msg/Twist` | Nav2 Controller와 활성 base backend |
| Odometry | `odom`, `nav_msgs/msg/Odometry` | 활성 Sim 또는 Real Odometry backend |
| LiDAR | `scan`, `sensor_msgs/msg/LaserScan` | LiDAR driver 또는 Sim sensor |
| Transform | `tf`, `tf_static` | 각 transform의 단일 소유 node |

### 2.2 Frame 소유권

| Transform | 후보 소유자 | 확인 상태 |
|---|---|---|
| `map → odom` | SLAM 또는 Localization | 실행 profile에서 확인 필요 |
| `odom → base_link` | Gazebo 또는 Real Odometry backend | 실행 profile에서 확인 필요 |
| `base_link → laser` | Robot description 또는 sensor publisher | 실제 장착값 확인 필요 |

## 3. 단계별 학습과 검증

한꺼번에 전체 Nav2를 성공시키려 하지 않고 아래 증거를 앞 단계부터 쌓는다.

| 단계 | 확인할 동작 | 최소 증거 |
|---|---|---|
| 1. Base | `cmd_vel`에 맞는 Mecanum 이동과 정지 | Pose sample, Odometry와 명령 timeout |
| 2. Sensor와 TF | LiDAR, IMU와 frame 연결 | Topic rate, timestamp와 TF tree |
| 3. Odometry | 이동 중 연속적인 `odom → base_link` | Pose 변화, rate와 drift 관찰 |
| 4. Mapping | 지도와 `map → odom` 생성 | Map artifact, trajectory와 loop closure 기록 |
| 5. Localization | 저장된 지도에서 pose 유지와 재위치 추정 | Pose, covariance와 relocalization 결과 |
| 6. Nav2 | 목표 pose 이동, 장애물 대응과 cancel | Path, Costmap, `cmd_vel`, result와 정지 |
| 7. Mission | 좌석 이동, 작업 후 복귀 | 두 Navigation result와 최종 Mission report |

설치됨, launch가 종료되지 않음, topic 이름이 존재함과 같은 상태는 해당 단계의 동작
증거를 대신하지 않는다.

## 4. 실험 기록

| 항목 | 기록 |
|---|---|
| 날짜와 실행 profile | 작성 예정 |
| Sim 또는 Real | 작성 예정 |
| ROS와 패키지 버전 | 작성 예정 |
| World, map과 시작 pose | 작성 예정 |
| 목표 pose와 경로 | 작성 예정 |
| 센서와 파라미터 | 작성 예정 |
| 성공 기준과 정량 결과 | 작성 예정 |
| 실패 위치와 원인 | 작성 예정 |
| Log, bag과 map artifact | 작성 예정 |

## 5. 평가 항목

- Mapping: 지도 일관성, trajectory 오차와 loop closure 영향
- Localization: 초기화, 위치 유지, 재위치 추정과 pose 오차
- Navigation: 성공률, 소요 시간, path 길이와 도착 pose 오차
- Safety: 장애물 정지, cancel latency와 명령 timeout
- Sim-to-Real: 같은 interface 의미, sensor 차이와 Mecanum slip 영향

정확한 metric과 합격 수치는 실험 목적과 팀 검토가 확인된 뒤 정한다.

## 6. 출처

- [내비게이션과 매핑](<../../20_TECHNICAL/05 - Navigation and Mapping.md>)
- [Robot ROS Contract](<../../20_TECHNICAL/10 - Robot ROS Contract.md>)
- [Hardware Configuration](<../../20_TECHNICAL/12 - Hardware Configuration.md>)
- [Verification and Simulation Strategy](<../../20_TECHNICAL/13 - Verification and Simulation Strategy.md>)

## 7. 주의점

- 이 문서의 학습 순서가 현재 구현 완료 상태를 뜻하지 않는다.
- Gazebo 결과를 실제 base의 Odometry, slip과 sensor 성능으로 일반화하지 않는다.
- 단일 성공 실행을 안정성 또는 반복 성공률로 표현하지 않는다.
- 학습 결과가 공식 기준 변경으로 이어질 때는 별도 검토와 Decision 절차를 따른다.
