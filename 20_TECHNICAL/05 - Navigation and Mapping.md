# 내비게이션과 매핑(Navigation and Mapping)

## 요약

MVP는 사전 제작 지도와 좌석별 접근 자세를 사용해 대기 위치와 지정 좌석 사이를
이동한다. 지도 제작은 환경 준비 과정이다. 현재 Runtime 구현은 좌석 ID 해석,
Nav2 실행과 도착 확인을 연결하며, 조작 가능한 책상 자세의 실물 검증은 별도로 남아 있다.

이 문서의 구현 근거는 `feat/runtime-integration`의 `65fdf06`이다. 실제 베이스
연결은 별도 구현이며, 이 코드가 실물 자율주행까지 검증됐다는 의미는 아니다.

## 지도 제작과 위치 추정

지도 제작에는 `slam_toolbox`와 Cartographer 설정 및 launch가 있다. 저장한 지도를
사용하는 미션 실행은 AMCL이 위치를 추정하고 Nav2가 경로와 차체 속도를 만든다.
SLAM과 AMCL이 동시에 같은 `map → odom`을 소유하지 않게 실행 구성을 선택한다.
알고리즘 설정의 존재를 최종 채택이나 실제 지도 정확도 검증으로 해석하지 않는다.

Wheel odometry는 연속적인 로컬 이동량을 제공하고 localization은 지도 기준 위치를
보정한다. 실제 wheel odometry, simulator ground truth와 localization pose는 출처가
다르다. 비교할 때 입력 센서, 지도, 기구 보정과 각 TF 소유자를 함께 기록한다.

## 좌석과 접근 자세

좌석 registry는 지도와 frame, home 및 좌석별 pose를 연결한다. Dashboard의 화면
pixel을 주행 목표로 역산하지 않고 canonical 좌석 ID를 Robot의 registry에서 해석한다.
배치가 바뀌면 지도와 registry의 일치 여부를 확인한다.

접근 pose는 책상과 의자에 부딪히지 않고 관찰 및 조작을 시작할 수 있는 후보 자세다.
정적 지도상의 여유, localization 오차, 실제 팔 도달성과 카메라 시야는 각각 검증해야
한다. 시뮬레이션 좌석 pose를 실환경 좌표나 충전 dock으로 간주하지 않는다.

## 주행과 도착 판정

```text
좌석 ID → 지도 기준 접근 pose → Nav2 goal
→ action 종료 + 최신 odometry의 정지 확인
→ 최신 map 기준 실제 추정 pose와 원래 목표 비교
→ 허용 위치 및 방향 오차 안일 때 책상 작업 시작
```

Mission Runtime은 Nav2 action 성공만으로 책상 작업을 시작하지 않는다. 정지 피드백,
위치와 방향 오차 및 pose 최신성을 독립 검사한다. 입력이 없거나 오래됐거나 원래
목표에서 벗어나면 작업 단계로 넘어가지 않는다. Nav2의 목표 허용 오차와 Mission의
도착 조건이 서로 누적돼도 조용히 통과하지 않게 하는 경계다.

이 검사는 localization 기준 도착이다. Simulator ground truth나 실측 위치에 대한
오차, 실제 책상 집기 가능성을 보증하지 않는다. 허용 오차와 대기 상한의 정확한 값은
Runtime 설정이 관리한다. 주행 실패와 취소에서도 terminal 결과와 정지 확인을 구분한다.

## 주행 명령과 관측 보호

공통 직렬 안전 경로는 다음과 같다. 실제 launch에서 선택한 경로와 활성 단계는
실행 근거에 남긴다. Simulator 전용 우회나 대체 모드를 실물 기본값으로 해석하지 않는다.

```text
Nav2 → 카메라 pan 정렬 및 새 depth 확인
→ Collision Monitor → 몸체와 제동 구간 voxel 검사 → 활성 base backend
```

LiDAR와 depth의 장애물 관측을 메모리에 누적하고 global 및 local costmap에 반영한다.
현재 관측되지 않는다는 이유만으로 과거 장애물을 제거하거나 미관측 공간을 안전한
빈 공간으로 취급하지 않는다. 2D 경로의 여유와 3D 몸체 충돌 검사는 다른 경계다.

| 조건 | 동작과 제약 |
|---|---|
| 필수 센서 단절, 오래되거나 미래인 stamp, TF 누락 | 해당 안전 경로에서 속도 차단 |
| 위치 추정 급변, voxel 갱신 중단, 계산 시간 초과 | 최종 속도 0 |
| 후진 | 뒤쪽 관측과 새 depth 확인 필요; 실물 시야는 별도 검증 |
| 횡이동 | 베이스는 지원하지만 확인한 기본 주행 구성은 차단 |
| 몸체 검사 | 설정된 park 팔 자세를 가정; 실시간 팔 FK 감시와 자세 유지까지 구현된 것은 아님 |

카메라 가림, 실제 제동 거리, 장착 오차와 바닥 slip은 실물 검증 대상이다. 안전
node가 0을 발행했다는 사실과 모터가 실제로 멈췄다는 사실을 구분한다.

## 선택과 검증의 경계

확인한 공통 구성에는 DWB 및 lattice 설정이 있으나 planner/controller 비교 브랜치의
모든 결과를 하나의 채택 결론으로 합치지 않는다. 전후 이동과 횡이동 정책, estimator
융합, 정밀 접근 및 복구 방식의 최종 선택 이유는 결정 근거가 확인될 때 기록한다.
관련 판단은 [Technical Questions](<99 - Questions.md>)에서 관리한다.

Gazebo는 센서, 주행, localization, 장애물과 취소 전달을 검증한다. MuJoCo의 고정
책상 조작과 이 주행 경로가 한 미션으로 연결됐는지는 별도로 확인해야 한다.

## 관련 문서

- [Mission Lifecycle](<09 - Mission Lifecycle.md>)
- [Robot ROS Contract](<10 - Robot ROS Contract.md>)
- [Safety and Risk](<08 - Safety and Risk.md>)
- [Verification and Simulation Strategy](<13 - Verification and Simulation Strategy.md>)

## 출처

- [Navigation 안전 및 관측 계약 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_navigation/docs/safety.md)
- [Nav2 도착 및 정지 확인 adapter at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_mission_manager/cleany_mission_manager/adapters/nav2.py)
- [Runtime과 Gateway 계약 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_interfaces/docs/mission.md)
- [Navigation 설정 at 65fdf06](https://github.com/asm17-moving-agent/cleany/tree/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_navigation/config)

## 관련 결정

- [260714 - 4륜 메카넘 베이스](<../30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스.md>)
- [261016 - System Supervisor 책임과 안전 경계](<../30_DECISIONS/Technical/261016 - System Supervisor 책임과 안전 경계.md>)
