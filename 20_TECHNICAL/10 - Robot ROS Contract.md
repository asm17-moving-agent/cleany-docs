---
type: technical
status: draft
reviewers:
  -
tags:
  - technical
  - draft
  - ros2
  - contract
  - sim-real
source_refs:
  - "40_RAW/10_Meetings/260710 - Docs 검증 및 ROS 2 Contract 회의 준비.md"
related_decisions:
  -
related_jira:
  -
updated: 2026-07-13
---

# 로봇 ROS 2 공통 계약(Robot ROS Contract)

## 1. 요약

이 문서는 Cleany 상위 소프트웨어가 MuJoCo simulation과 실제 로봇을 같은 방식으로 사용할 수 있도록 로봇 경계의 ROS 2 topic, message type, frame, QoS, 시간 및 안전 의미를 정의하는 초안이다.

현재 이 계약을 채택한 `selected` Decision은 없다. 따라서 이 문서의 MVP 핵심 계약은 구현과 팀 검토를 위한 권고안이며, 실제 XLeRobot 구동 방식과 센서 구성이 확인되기 전까지 수치와 세부 frame 이름을 확정하지 않는다.

## 2. 기획 맥락

Cleany는 같은 Mission Manager, Navigator, Perception, Planner, Skill Executor를 유지하면서 하위 robot backend만 Sim 또는 Real로 교체하는 구조가 필요하다. 상위 모듈은 MuJoCo 내부 actuator나 실제 motor driver를 직접 알지 않고, 이 문서의 공통 ROS 2 계약에만 의존한다.

1차 MVP는 사전에 정한 소수의 쓰레기 물체를 인식·분류·집기하는 흐름을 우선한다. 분실물 후보와 저신뢰 물체는 조작하지 않는다. 자율주행, RGB-D, arm/gripper의 현장 시연 범위는 별도 검토가 필요하다.

## 3. 기술 개념

### 3.1 계약 계층

Navigation goal과 base command는 경쟁하는 하나의 계약이 아니라 서로 다른 계층이다.

```text
Mission Manager
    │ target_id
    ▼
Navigator
    │ NavigateToPose 또는 동등한 navigation action
    ▼
Nav2
    │ geometry_msgs/msg/Twist
    ▼
cmd_vel
    │
    ▼
활성 Sim 또는 Real base backend
```

- 상위 navigation 계약: 목적지까지 오래 걸리는 작업의 goal, feedback, result, cancel을 표현한다.
- 하위 base 계약: 짧은 주기로 전달되는 차체 속도 명령과 odometry를 표현한다.
- Mission Manager는 wheel 속도나 actuator 값을 직접 만들지 않는다.
- Sim과 Real backend는 같은 하위 계약을 구현하되 한 실행에서는 하나만 활성화한다.

### 3.2 이름과 namespace 원칙

노드 구현은 선행 `/`가 없는 상대 이름을 사용한다.

```python
create_subscription(Twist, "cmd_vel", ...)
create_publisher(Odometry, "odom", ...)
```

단일 로봇을 root namespace에서 실행하면 `/cmd_vel`, `/odom`으로 resolve된다. 다중 로봇 또는 Sim/Real 동시 비교가 필요할 때는 namespace와 remap으로 분리한다. Sim과 Real을 같은 canonical topic에 동시에 연결하지 않는다.

### 3.3 MVP 핵심 topic 권고안

아래 표 전체는 아직 팀 검토가 필요한 `draft`다.

| 상대 topic | message type | Publisher | Subscriber | 계약 의미 |
|---|---|---|---|---|
| `cmd_vel` | `geometry_msgs/msg/Twist` | Nav2 controller 또는 수동 제어기 | 활성 base backend | 차체 기준 속도 명령 |
| `odom` | `nav_msgs/msg/Odometry` | 활성 odometry backend | localization, Nav2, logger | `odom` 기준 차체 pose와 twist |
| `joint_states` | `sensor_msgs/msg/JointState` | 활성 robot backend | `robot_state_publisher`, MoveIt, logger | 관절 위치·속도·effort 상태 |
| `scan` | `sensor_msgs/msg/LaserScan` | LiDAR driver 또는 Sim | SLAM, localization, Nav2 | `laser` 기준 2D 거리 측정 |
| `tf` | `tf2_msgs/msg/TFMessage` | transform 소유 node | 전체 시스템 | 동적 frame 변환 |
| `tf_static` | `tf2_msgs/msg/TFMessage` | `robot_state_publisher` 등 | 전체 시스템 | 정적 frame 변환 |
| `clock` | `rosgraph_msgs/msg/Clock` | Sim backend | `use_sim_time` node | simulation 전용 시간 |

### 3.4 `cmd_vel` 의미 권고안

| 필드 | 단위 | 의미 | 상태 |
|---|---|---|---|
| `linear.x` | m/s | `base_link` 기준 전진·후진 속도 | MVP 후보 |
| `linear.y` | m/s | `base_link` 기준 좌우 속도 | base kinematics 확인 필요 |
| `angular.z` | rad/s | `base_link` 기준 yaw 회전 속도 | MVP 후보 |
| 나머지 필드 | - | 모바일 베이스에서 사용하지 않음 | 0을 요구하는 안 검토 필요 |

`geometry_msgs/msg/Twist`에는 `header`와 `frame_id`가 없으므로 `base_link` 기준이라는 의미는 이 계약과 backend 설정에서 명시한다.

활성 base backend가 가져야 할 기본 방어 동작 후보:

- 마지막 명령 이후 `cmd_vel_timeout`이 지나면 정지한다.
- NaN, infinity 같은 유효하지 않은 값은 실행하지 않고 진단 정보를 남긴다.
- 속도와 가속도 제한은 실제 로봇 사양에 따른 ROS parameter 또는 `configs/robot/` 설정으로 둔다.
- 지원하지 않는 `linear.y`를 다른 축으로 재해석하지 않는다.
- e-stop 또는 hardware fault 상태에서는 새 속도 명령보다 정지 정책을 우선한다.

정확한 timeout, 속도, 가속도 수치는 실제 base 사양과 안전 검토 후 정한다.

### 3.5 상태 topic 의미

#### `odom`

- `header.frame_id`: `odom`
- `child_frame_id`: `base_link`
- pose와 twist 단위는 SI 단위를 사용한다.
- Sim 초기 구현은 ground-truth odometry를 사용할 수 있으나, 실제 wheel odometry와 동일한 정확도를 보장한다고 표현하지 않는다.

#### `joint_states`

- joint 이름은 robot description의 joint 이름과 일치해야 한다.
- revolute joint 위치는 radian, prismatic joint 위치는 meter를 사용한다.
- Sim과 Real은 같은 논리 joint 이름을 사용하는 것을 목표로 한다.

#### `scan`

- `header.frame_id`는 LiDAR frame을 사용한다.
- range는 meter, angle은 radian을 사용한다.
- 유효 범위와 scan 주기는 sensor 또는 simulation config로 관리한다.

### 3.6 sensor 확장 후보

아래 topic은 Perception과 localization에 필요할 가능성이 높지만 정확한 장치와 namespace가 확인되지 않아 MVP 핵심 계약과 분리한다.

| 상대 topic 후보 | message type | 상태 |
|---|---|---|
| `imu/data` | `sensor_msgs/msg/Imu` | IMU 사양과 fusion 방식 확인 필요 |
| `camera/color/image_raw` | `sensor_msgs/msg/Image` | RGB-D driver naming 확인 필요 |
| `camera/color/camera_info` | `sensor_msgs/msg/CameraInfo` | calibration 계약 확인 필요 |
| `camera/depth/image_raw` | `sensor_msgs/msg/Image` | depth encoding 확인 필요 |
| `camera/depth/camera_info` | `sensor_msgs/msg/CameraInfo` | RGB/depth 정합 방식 확인 필요 |

Perception은 Sim/Real 구현을 직접 분기하지 않고, 선택된 sensor topic과 frame 계약을 통해 입력을 받는다.

### 3.7 frame tree와 소유권 권고안

```text
map
└── odom
    └── base_link
        ├── laser
        ├── imu_link
        ├── camera_link
        │   ├── camera_color_optical_frame
        │   └── camera_depth_optical_frame
        └── arm links ...
```

| transform | 소유 컴포넌트 | 상태 |
|---|---|---|
| `map -> odom` | SLAM 또는 localization | navigation 사용 시 필요 |
| `odom -> base_link` | 활성 Sim 또는 Real odometry backend | MVP 후보 |
| `base_link -> sensor/arm links` | `robot_state_publisher` | robot description 필요 |

하나의 transform은 한 컴포넌트만 발행한다. `laser`, `camera_link`, optical frame, end-effector의 최종 이름과 실제 변환 수치는 URDF/Xacro 및 XLeRobot 사양 확인 후 확정한다.

### 3.8 Arm / Gripper 계약 후보

- 현재 `cleany_mujoco_sim`의 private `~/joint_cmd`는 qpos를 직접 바꾸는 simulation test hook으로만 유지한다.
- private test hook을 Sim/Real 공통 제어 계약으로 사용하지 않는다.
- arm 공통 계약은 ROS 표준 `control_msgs/action/FollowJointTrajectory` 사용을 우선 검토한다.
- gripper 공통 계약은 `control_msgs/action/GripperCommand` 또는 실제 gripper driver가 제공하는 표준 호환 action을 검토한다.
- MoveIt 또는 Skill Executor가 표준 action을 호출하고, Sim/Real controller가 같은 joint 의미를 구현하는 구조를 목표로 한다.

arm joint, gripper, controller 이름과 허용 범위는 아직 확정하지 않는다.

### 3.9 QoS 권고안

| 데이터 | QoS 후보 | 이유 |
|---|---|---|
| `cmd_vel` | reliable, volatile, keep last | 최신 제어 명령 전달 |
| `odom`, `joint_states` | reliable, volatile | 상태 전달과 디버깅 |
| `scan`, IMU, camera | ROS 2 Sensor Data QoS | 지연보다 최신 sensor sample 우선 |
| `tf`, `tf_static` | tf2 표준 broadcaster/listener QoS | ROS 2 TF 생태계 호환 |

정확한 depth와 deadline/liveliness 정책은 주기와 네트워크 환경을 측정한 뒤 정한다.

## 4. 인터페이스 / 경계

| 구성요소 | 책임 | 경계 |
|---|---|---|
| Navigator/Nav2 | 목적지 해석, 경로 계획, base 속도 생성 | actuator와 motor protocol을 직접 다루지 않음 |
| Sim base backend | 공통 명령을 MuJoCo actuator로 변환하고 상태 발행 | 실제 hardware protocol을 포함하지 않음 |
| Real base backend | 공통 명령을 motor driver로 변환하고 상태 발행 | mission과 navigation 판단을 수행하지 않음 |
| Robot description | joint/link 이름과 정적·관절 TF 제공 | 동적 odometry를 소유하지 않음 |
| Sensor driver/Sim sensor | 표준 sensor message 발행 | 물체 의미와 행동을 결정하지 않음 |
| Skill Executor/MoveIt | high-level skill과 manipulation motion 실행 | private simulation hook에 의존하지 않음 |

## 5. 가정

- 기본 실행은 단일 Cleany 로봇이며 root namespace를 사용한다.
- Sim 또는 Real backend 중 하나만 canonical robot topic과 TF를 소유한다.
- 상위 mission stack은 backend 종류를 알지 않는다.
- 실제 XLeRobot base kinematics, joint 이름, sensor 장착 위치는 추가 확인 필요다.
- 모든 node가 simulation에서 `use_sim_time`을 일관되게 적용할 수 있다고 가정한다.

## 6. 리스크

- base가 holonomic인지 확인하지 않고 `linear.y`를 구현하면 실제 동작과 simulation이 달라질 수 있다.
- Sim과 Real이 동시에 같은 topic 또는 transform을 발행하면 navigation과 상태 추정이 깨질 수 있다.
- frame 이름과 joint 이름이 driver, URDF, MoveIt 사이에서 다르면 integration 비용이 커진다.
- QoS가 publisher/subscriber 사이에서 호환되지 않으면 sensor data가 보이지 않을 수 있다.
- command timeout과 e-stop 경계가 없으면 node 중단 시 마지막 명령이 계속 적용될 수 있다.

## 7. 관련 결정

- 현재 selected Decision 없음.
- `/cmd_vel`, frame, arm/gripper, sensor naming의 최종 채택은 Technical Decision 또는 팀 검토가 필요하다.
- 관련 미해결 항목은 [[20_TECHNICAL/99 - Questions|Technical Questions]]에서 관리한다.
- 회의 준비 근거는 [[40_RAW/10_Meetings/260710 - Docs 검증 및 ROS 2 Contract 회의 준비|Docs 검증 및 ROS 2 Contract 회의 준비]]다.
