# 로봇 ROS 2 공통 계약(Robot ROS Contract)

## 요약

Navigation goal, 차체 속도, wheel 명령, 관절 trajectory와 센서 상태의 계층을 구분한다.
Sim과 Real은 의미와 소유권을 공유하되 같은 구현이나 정확도를 가정하지 않는다.
정확한 message 필드, endpoint, QoS와 parameter는 구현 레포 reference가 관리한다.

현재 Runtime과 Scene/Grasp는 `65fdf06`, 실물 base와 MCU 계약은 `e8b9f11`,
Supervisor 계약은 `c63fadb`를 근거로 한다. 통합 방향과 각 구현의 현재 상태는
[Technical Overview](<00 - Technical Overview.md>)를 따른다.

## 명령 계층과 단일 소유권

```text
Mission의 좌석 ID → Navigator의 지도 pose와 NavigateToPose
→ Nav2 및 선택된 안전 경로 → cmd_vel
→ Sim base 또는 Real base driver → wheel 명령 → MCU → motor
```

Mission은 wheel command를 만들지 않고 Backend는 Robot 내부 FSM과 motor를 직접
제어하지 않는다. 한 실행에서 최종 차체 명령원, MCU wheel 명령원 및 canonical
odometry와 TF edge의 소유자를 각각 명확히 한다. Nav2, teleop과 시험 명령을 겹쳐
발행하지 않는다. namespace와 remap으로 격리하며 노드는 상대 이름을 사용한다.

`cleany_robot_interface`는 공통 의미 경계다. 현재 모든 명령과 센서가 하나의 완성된
해당 패키지를 통과한다고 가정하지 않는다.

## 차체 명령과 MCU 구동 허가

`cmd_vel`은 `base_link` 기준 x, y 병진 m/s와 yaw rad/s를 나타내는 Twist다.
메카넘 base는 세 축을 지원하지만 상위 주행 profile은 횡이동을 제한할 수 있다.
실물 driver는 유한성 및 속도 한계를 검사하고 wheel 목표가 한계를 넘으면 비율을
유지해 줄인다. 지원하지 않는 축과 잘못된 수치의 처리는 구현 reference에 명시한다.

`e8b9f11`의 ESP32-S3는 native USB의 micro-ROS로 WheelCommand와 WheelState를
교환한다. ROS 배열의 FL, FR, RL, RR 순서와 PCB의 motor 순서를 MCU에서 변환하며,
wheel, encoder 부호를 host에서 다시 반전하지 않는다. 기구 치수와 slip을 반영한
유효 기구학 보정값도 다른 값으로 관리한다.

| 조건 | 명령과 허가 의미 |
|---|---|
| 시작, 재부팅, 연결 복구 | 구동 비허가; 명시적 ENABLE과 그 이후의 새 명령 필요 |
| MCU 명령 | protocol, sequence, 유효 수치와 MCU 기준 deadline 검사 |
| STOP, 만료, 통신 두절 | 목표와 허가 폐기; cached 이동 명령 자동 복구 금지 |
| Host timeout | monotonic 수신 시간으로 판단; MCU watchdog과 별도로 동작 |
| Command 재시도 | 같은 sequence/deadline 유지; 오래된 패킷이 유효기간을 연장하지 않음 |

연결 성공과 `/cmd_vel` 발행은 구동 허가가 아니다. Deadline, slew와 PI+FF 동작은
firmware 계약이 관리한다. MCU의 PWM zero 응답과 실제 정지 거리는 별도 검증한다.
기존 `main`의 바이너리 serial firmware와 micro-ROS 경로를 혼용하지 않는다.

## 상태, TF와 시간

| 데이터 또는 TF | 의미와 소유권 |
|---|---|
| `joint_states` | description과 같은 joint 이름; revolute rad 및 rad/s |
| `wheel/odom` | 누적 wheel 각도에서 계산한 로컬 이동 추정; ground truth 아님 |
| `odom` 및 `odom → base_link` | 선택된 canonical estimator 또는 relay 한 곳이 소유 |
| `map → odom` | SLAM 또는 saved-map localization 중 활성 소유자 한 곳 |
| base와 sensor, arm TF | description과 해당 actuator/backend의 책임; capture-time lookup 사용 |
| `scan` | LiDAR frame, meter와 radian, 유효 촬영 stamp |
| RGB-D, CameraInfo | 정합, encoding, 크기, optical frame과 시각의 일치 |
| `/clock` | simulation 시간; 관측 stamp와 별개인 timeout의 steady clock을 대체하지 않음 |

실물 기본 odometry는 wheel feedback에서 계산하고 relay가 canonical odom과 TF를
소유한다. IMU/EKF 융합을 이미 기본 적용했다고 설명하지 않는다. 융합 estimator를
연결하면 기존 relay 소유권을 넘겨 중복 발행을 막아야 한다.

MCU monotonic microseconds는 ROS epoch가 아니다. Host는 수신 시각, boot ID와
sequence를 구분하며 encoder rollover 및 관측 단절 후 baseline을 처리한다.
미관측 구간의 이동을 임의로 복원하거나 과거 상태를 최신으로 재발행하지 않는다.

Gazebo ground-truth odometry와 encoder 기반 odometry는 profile에 따라 다르다.
평가용 참값을 localization 결과나 실제 wheel feedback으로 표시하지 않는다.
센서의 정확한 이름과 frame은 URDF 및 실행 profile의 실제 계약을 따른다.

## 조작 요청과 controller

Mission의 단일 객체 Action은 승인한 snapshot, object, destination과 execution ID를
전달한다. 재전송, 결과 불명확과 재시작 시 같은 행동이 새 실행으로 중복되지 않아야
한다. 결과에는 행동 outcome, 정지, 물체 보유와 놓기 확인이 함께 보존된다.

Scene inspection, grasp planning과 reachable-grasp 선택은 조작 실행과 다른 계약이다.
plan-only 성공은 controller 실행이나 실제 수거 성공이 아니다.

현재 MuJoCo 조작은 MoveIt과 trajectory controller를 사용한다. 팔의 표준
FollowJointTrajectory와 joint feedback 의미를 유지하며, simulator qpos나 private
hook을 실물 제어 계약으로 승격하지 않는다. 실물 arm/gripper driver의 실행과 정지
조건 및 보정값은 별도 통합 대상이다.

## 시스템 가용성, 허가와 복구

System Supervisor는 시스템 운영 상태, Capability, Fault, 복구 상태와 heartbeat를
제공한다. 상태 snapshot에는 프로세스 실행 세대와 순서를 구분할 수 있는 정보가
필요하며, 오래된 snapshot 수신을 유효한 실행 허가로 취급하지 않는다.

- Mission 실행 허가는 필요한 Capability, Mission 식별자, 실행 세대, version과
  유효기간을 연결한다. Mission client는 실행 중 철회와 로컬 만료를 반영해야 한다.
- Supervisor 재시작은 이전 허가를 무효화한다. 센서 시간과 통신 수신 시각을 구분하고,
  simulation clock 정지나 변경이 허가 및 안전 timeout을 무기한 연장하지 않게 한다.
- Mission 중단은 Action 수락과 실제 완료를 구분한다. component recovery도 Action
  결과 이후 health가 실제로 복귀했는지 별도로 확인한다.
- component health는 단순 node 존재나 Topic 수신과 구분하며, 안전 상태 보고는
  독립 안전 계층의 실제 증거를 표현한다. 보고 interface가 있다는 사실만으로 해당
  실물 기능이 구현됐다고 가정하지 않는다.
- Supervisor의 복구 정책과 Mission 허가는 하위 command, controller 및 하드웨어
  안전 계약을 대신하지 않는다.

개념과 책임은 [System Supervisor](<14 - System Supervisor.md>)를 따른다.
`feat/system-supervisor`의 `c63fadb`에서 추가한 정확한 message, service, action과
QoS는 해당 구현 reference에서 관리한다. 기존 sensor, arm/gripper와 base 명령 계약을
새로운 Supervisor 명령 체계로 대체하지 않는다.

## 실패와 안전의 해석

- Action 수락, 완료 결과와 실제 정지 확인을 구분한다.
- 입력이 오래됐거나 TF와 calibration이 없으면 정상 관측, 준비 상태를 합성하지 않는다.
- Wheel feedback 정상, 팔 통신 정상과 Mission을 실행할 수 있는 안전 상태는 다르다.
- Fault release, 복구 Action 성공과 새 Mission 실행 허가는 각각 다른 조건이다.
- 물리 e-stop과 하드웨어 보호는 Supervisor, ROS, cloud 연결의 생존에 의존하지 않는다.

## 관련 문서

- [Navigation and Mapping](<05 - Navigation and Mapping.md>)
- [Mission Lifecycle](<09 - Mission Lifecycle.md>)
- [System Supervisor](<14 - System Supervisor.md>)
- [Manipulation and Calibration](<15 - Manipulation and Calibration.md>)

## 출처

- [현재 계약 reference 색인 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/docs/INTEGRATION.md)
- [Base 명령, 구동 허가와 odometry at e8b9f11](https://github.com/asm17-moving-agent/cleany/blob/e8b9f114518cda1e213cd6ba4fb8fcfce979f951/ros2_ws/src/cleany_base_driver/README.md)
- [micro-ROS firmware와 motor task at e8b9f11](https://github.com/asm17-moving-agent/cleany/blob/e8b9f114518cda1e213cd6ba4fb8fcfce979f951/esp32/README.md)
- [Wheel protocol v2 at e8b9f11](https://github.com/asm17-moving-agent/cleany/blob/e8b9f114518cda1e213cd6ba4fb8fcfce979f951/ros2_ws/src/cleany_base_interfaces/README.md)
- [Scene와 Grasp at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_interfaces/docs/scene-and-grasp.md)
- [단일 객체 Manipulation at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_interfaces/docs/manipulation.md)
- [Supervisor ROS 계약 at c63fadb](https://github.com/asm17-moving-agent/cleany/blob/c63fadb467afac08cc62a3cfd0a5af7c59b6e8b7/ros2_ws/src/cleany_system_supervisor/README.md)

## 관련 결정

- [260714 - 4륜 메카넘 베이스](<../30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스.md>)
- [261002 - Manipulation 결과와 안전 상태 보존](<../30_DECISIONS/Technical/261002 - Manipulation 결과와 안전 상태 보존.md>)
- [261016 - System Supervisor 책임과 안전 경계](<../30_DECISIONS/Technical/261016 - System Supervisor 책임과 안전 경계.md>)
