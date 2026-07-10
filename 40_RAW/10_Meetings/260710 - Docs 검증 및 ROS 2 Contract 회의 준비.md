---
type: raw-meeting
review_status: needs-human-review
ingest_status: raw
ingest_targets:
  - technical
  - decision
planning_targets:
  -
technical_targets:
  - "20_TECHNICAL/10 - Robot ROS Contract.md"
decision_candidates:
  -
related_decisions:
  -
related_planning:
  - "10_PLANNING/08 - Questions.md"
related_technical:
  - "20_TECHNICAL/00 - Technical Overview.md"
  - "20_TECHNICAL/01 - System Concept.md"
  - "20_TECHNICAL/07 - Data and Evaluation.md"
  - "20_TECHNICAL/09 - Mission Manager FSM.md"
date: 2026-07-10
participants:
  -
related_jira:
  -
tags:
  - raw
  - meeting
  - ingest-source
  - ros2
  - contract
---

# 260710 - Docs 검증 및 ROS 2 Contract 회의 준비

## 1. 회의 맥락

Cleany 구현 레포에는 Docker 기반 ROS 2 Humble 개발 환경과 일부 ROS 패키지 초안이 준비되어 있다. `cleany_mujoco_sim`은 MuJoCo simulation을 ROS 2 node로 감싸 `joint_states`, `odom`, `scan`, `tf`, `tf_static`을 publish하고, 현재는 simulation test hook 성격의 `~/joint_cmd`를 subscribe한다.

오늘 회의에서는 먼저 `cleany-docs` 전체 문서를 훑어보며 현재 프로젝트 이해를 맞추고, 그 다음 sim과 실제 로봇을 갈아끼울 수 있게 하기 위한 ROS 2 공통 contract 초안을 논의한다. 이 문서는 회의 전 안건 정리용 raw note이며, 합의된 내용은 이후 `20_TECHNICAL` 문서 또는 Decision draft로 승격한다.

## 2. 회의 목표

- `cleany-docs` 전체 문서를 훑어보며 현재 프로젝트 상태와 남은 질문을 공유한다.
- 기획/기술 문서에서 팀이 같은 이해를 가져야 하는 지점을 확인한다.
- sim/real 교체를 전제로 한 ROS 2 topic, frame, action, launch contract 범위를 논의한다.
- 다음 구현 우선순위를 정한다.
## 3. Docs 전체 훑어보기 가이드

- 문서 전체를 훑으며 팀원 간 이해가 다른 부분을 표시한다.
- 확정된 내용, draft로 남길 내용, 추가 질문으로 남길 내용을 구분한다.
- 구현과 충돌하거나 이미 구현이 앞서간 내용을 표시한다.
- Mission Manager, Navigator, Perception, Planner, Skill Executor 책임 경계를 확인한다.
- sim/real 교체와 ROS 2 Contract 논의로 넘길 항목을 표시한다.
- 합의된 내용은 결정 후보로, 확정 못 한 내용은 미해결 질문으로 남긴다.

## 4. ROS 2 Contract 논의 안건

### 4.1 ROS 2 통신 기본 개념

- Topic은 publish/subscribe 방식이며, 센서값/상태/속도 명령처럼 계속 흐르는 데이터에 사용한다.
- Service는 request/response 방식이며, reset/상태 조회처럼 짧게 끝나는 요청에 사용한다.
- Action은 goal/feedback/result 방식이며, navigation/trajectory 실행처럼 오래 걸리고 취소나 진행률이 필요한 작업에 사용한다.
- Frame은 좌표계 이름이며, `base_link`, `laser`, `camera_link`처럼 데이터가 어느 기준 좌표계인지 나타낸다.
- `tf`/`tf_static`은 frame 사이의 위치·회전 관계를 공유하는 topic이다.
- sim과 real robot을 바꿔 끼우려면 노드가 특정 구현이 아니라 같은 topic/message/action /frame contract에 의존해야 한다.

### 4.2 공통 topic 후보

MVP 공통 contract 후보:

```text
/joint_states
/odom
/tf
/tf_static
/scan
/cmd_vel
```

논의할 질문:

- `/joint_states`, `/odom`, `/scan`을 global topic으로 둘지 namespace 아래에 둘지?
- `/cmd_vel`을 공통 base command contract로 채택할지?
- Nav2를 직접 contract로 볼지, `/cmd_vel`을 하위 contract로 볼지?
- `cleany_mujoco_sim`이 `/cmd_vel`을 받아 base motion을 제공해야 하는지?

### 4.3 frame 후보

MVP frame 후보:

```text
map
odom
base_link
laser
camera_link
end_effector
```

논의할 질문:

- `map -> odom -> base_link` 구조를 MVP에서도 유지할지?
- MuJoCo와 실제 XLeRobot에서 동일한 frame 이름을 쓸 수 있는지?
- `laser`, `camera_link`, `end_effector` frame 이름을 확정할지?

### 4.4 Arm / Gripper command

논의할 질문:

- arm command는 단순 joint command topic으로 시작할지?
- ROS 표준 `FollowJointTrajectory` action을 목표 contract로 둘지?
- gripper는 별도 command topic/action이 필요한지?
- MVP에서는 direct joint command를 simulation hook으로만 둘지, 공통 contract로 볼지?

### 4.5 Sensor contract

논의할 질문:

- LiDAR는 `/scan` 하나로 충분한지?
- RGB-D camera topic 이름은 어떻게 둘지?
- Perception이 sim/real 차이를 모르도록 어떤 sensor topic을 공통화할지?
- camera/depth/image/camera_info는 MVP에 포함할지?

### 4.6 launch / bringup 구조

논의할 launch 분리안:

```text
mission_stack.launch.py
  mission_manager
  navigator
  perception
  planner
  skill_executor

sim_bringup.launch.py
  cleany_mujoco_sim

real_bringup.launch.py
  real robot drivers
```

논의할 질문:

- mission stack과 robot bringup을 분리할지?
- sim과 real이 같은 mission stack launch를 재사용하는 것을 목표로 할지?
- common parameter와 sim-only parameter를 어디서 나눌지?

## 5. 현재 구현 기준 확인 사항

`cleany_mujoco_sim` 현재 상태:

```text
node name: mujoco_sim
executable: mujoco_sim_node
launch: mujoco_sim.launch.py

publish:
- joint_states
- odom
- scan
- tf
- tf_static

subscribe:
- ~/joint_cmd

not implemented:
- /cmd_vel
- Nav2-compatible base command
- camera topics
- gripper command
- binding to Mission Manager / Perception / Skill Executor
```

## 6. 결정 후보

| 후보 | 선택지 | 비고 |
|---|---|---|
| ROS contract 문서 위치 | `20_TECHNICAL/10 - Robot ROS Contract.md` | 회의 후 draft 생성 후보 |
| base command | `/cmd_vel` 사용 / Nav2 action 우선 / 미정 | sim과 real 공통화 필요 |
| frame 이름 | `map`, `odom`, `base_link`, `laser`, `camera_link`, `end_effector` | 실제 XLeRobot frame과 맞춰야 함 |
| launch 구조 | mission stack과 robot bringup 분리 / 단일 launch 유지 | sim-real 교체성에 영향 |
| arm command | direct joint topic / trajectory action / 미정 | MVP 범위와 구현 난이도 검토 |

## 7. 후속 작업 후보

| 작업 | 담당자 | 관련 Jira |
|---|---|---|
| docs 전체 훑어보기 결과 정리 |  |  |
| `Robot ROS Contract` draft 작성 |  |  |
| `cleany_mujoco_sim` `/cmd_vel` 지원 여부 결정 |  |  |
| Mission Manager ROS node wrapper 구현 범위 결정 |  |  |
| sim bringup / mission stack launch 분리안 작성 |  |  |

## 8. 미해결 질문

- MVP에서 반드시 필요한 공통 ROS topic은 무엇인가?
- `cleany_mujoco_sim`의 `~/joint_cmd`는 simulation-only hook으로 유지할 것인가?
- 실제 XLeRobot driver가 제공할 topic/action/frame과 현재 sim node가 맞출 수 있는가?
- Perception 입력으로 RGB-D camera topic을 MVP에 포함할 것인가?
- Navigation은 Nav2 기반으로 바로 갈 것인가, 단순 `/cmd_vel` 기반 navigator부터 시작할 것인가?
- arm/gripper 제어는 ROS 표준 action을 사용할 것인가, 단순 topic으로 시작할 것인가?
- 내일 회의에서 확정할 항목과 추가 검토로 넘길 항목을 어떻게 나눌 것인가?
