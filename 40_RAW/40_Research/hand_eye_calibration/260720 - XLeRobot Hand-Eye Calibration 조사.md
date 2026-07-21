---
type: raw-research
reviewers:
  - 이정현
ingest_status: raw
ingest_targets:
  - technical
  - decision
decision_candidates:
  - OpenCV CALIB_HAND_EYE_PARK를 simulation 기준 알고리즘으로 사용
date: 2026-07-20
related_jira:
  - SCRUM-264
tags:
  - raw
  - research
  - xlerobot
  - hand-eye-calibration
  - simulation
source_refs:
  - 20_TECHNICAL/04 - Robot Platform XLeRobot.md
  - 20_TECHNICAL/10 - Robot ROS Contract.md
  - 30_DECISIONS/Technical/260708 - XLeRobot 기반 플랫폼.md
  - 30_DECISIONS/Technical/260715 - 로봇 프레임 구조.md
---

# 260720 - Simulation 기반 Hand-Eye Calibration 방법론 선정

## 1. 목표와 결론

이 문서에선 XLeRobot simulation에서 사용할 hand-eye calibration 방법론을 비교하고 PnP, solver 알고리즘과 실험 조건을 결정한다. 주 범위는 좌·우 wrist camera의 eye-in-hand calibration이다. Head Pan/Tilt D435의 동적 FK는 향후 고도화 목표로 두고, 현재는 pan/tilt joint를 고정한 뒤 CAD model에서 정한 사전 정의 각도만 검증한다.

선정 후보는 Tsai와 Park이다. 선정 이유는 다음과 같다.

- OpenCV 표준 API로 구현할 수 있어 별도 solver 개발이 필요 없다.
- Rotation을 SO(3) 구조에서 다루는 방식이라 다양한 회전축을 포함한 dataset의 기준 알고리즘으로 쓰기 적합하다.
- 입력과 출력이 다른 OpenCV hand-eye method와 같아 동일 dataset에서 공정하게 비교하기 쉽다.
- Simulation ground truth와 직접 오차를 비교할 수 있어 frame 방향과 구현 오류를 빠르게 찾을 수 있다.

모든 환경에서 항상 가장 정확하다고 전제하지 않는다. 구현과 분석 복잡도를 낮추기 위해 separable method인 Tsai와 Park만 같은 조건에서 비교한다.

## 2. 기초 개념과 구현 범위

### 2.1 필요한 입력과 출력

Eye-in-hand calibration은 camera가 gripper와 함께 움직이고 target은 robot base에 고정된 경우다. Pose마다 다음 두 값을 같은 timestamp로 수집한다.

- Robot FK: base에서 gripper로의 pose ${}^{b}\mathbf{T}_{g}$
- Target detection: camera에서 target으로의 pose ${}^{c}\mathbf{T}_{t}$

구하려는 값은 gripper에서 camera로의 고정 transform ${}^{g}\mathbf{T}_{c}$다. 각 sample은 아래 관계를 만족해야 한다.

$$
{}^{b}\mathbf{T}_{g}\,{}^{g}\mathbf{T}_{c}\,{}^{c}\mathbf{T}_{t}
= {}^{b}\mathbf{T}_{t}
$$

두 pose의 상대 motion을 만들면 hand-eye 문제는 $\mathbf{A}\mathbf{X}=\mathbf{X}\mathbf{B}$ 형태가 된다.

### 2.2 Simulation 실행 경로

Arm pose 생성과 측정은 실제 적용 예정인 아래 경로를 사용한다.

~~~text
MoveIt
  -> FollowJointTrajectory
  -> ros2_control joint_trajectory_controller
  -> mujoco_ros2_control/MujocoSystemInterface
  -> MuJoCo actuator·physics
  -> joint state interface
  -> /joint_states·TF·calibration collector
~~~

Calibration collector는 MuJoCo에서 되돌아온 qFb로 FK를 계산한다. Image와 joint state는 simulation clock 기준으로 묶는다. Calibration 결과는 robot description의 camera mount transform 후보로 적용한다.

### 2.3 Head Pan/Tilt의 현재 범위

현재 단계에서는 D435의 pan/tilt joint를 simulation 중 움직이지 않는다. CAD model에서 선택한 pan angle과 tilt angle을 joint 초기값으로 고정하고 다음 항목만 확인한다.

- 고정 각도에서 camera optical frame과 TF 방향이 CAD model과 일치하는가?
- 쓰레기와 작업 영역이 FOV 안에 들어오는가?

Pan/tilt angle별 동적 TF 계산, encoder 오차, backlash와 image timestamp 동기화는 향후 고도화 범위다. 1차 구현에선 Pan / Tilt를 hand-eye solver의 대상에 포함하지 않는다.

## 3. 후보 알고리즘

모든 후보는 OpenCV calibrateHandEye에서 같은 입력 형식으로 실행한다.

| 후보   | 방식                             | 장점                                  | 주요 확인점                              |
| ---- | ------------------------------ | ----------------------------------- | ----------------------------------- |
| Tsai | Rotation과 translation을 순서대로 계산 | 가장 단순한 고전 baseline                  | Rotation 오차가 translation으로 전달되는지 확인 |
| Park | SO(3) 기반 separable method      | Rotation이 다양한 dataset의 기준으로 사용하기 쉬움 | 회전축 다양성이 부족하면 결과가 불안정할 수 있음         |

Tsai와 Park는 모두 OpenCV의 같은 API와 같은 입력을 사용하고 rotation과 translation을 단계적으로 다루므로 구현과 디버깅 범위가 작다. Horaud, Andreff와 Daniilidis는 이번 테스트에서 제외한다. 후보를 더 늘려 얻는 비교 폭보다 quaternion, simultaneous solution과 결과 해석에서 추가되는 복잡도가 더 크다고 판단했다.

PnP는 hand-eye method 비교와 분리한다. 모든 method에 동일한 ${}^{c}\mathbf{T}_{t}$를 제공해야 hand-eye solver만 비교할 수 있다. Planar target에는 SOLVEPNP_IPPE로 복수해를 확인하고, 유효한 해를 solvePnPRefineVVS로 refinement하는 경로를 기준으로 한다.

## 4. 비교 기준과 실험 조건

### 4.1 공통 실험 조건

| 항목            | 조건                                        |
| ------------- | ----------------------------------------- |
| Topology      | 좌측 wrist camera eye-in-hand               |
| Dataset       | Arm별 calibration 20 pose, held-out 5 pose |
| Pose 구성       | 서로 평행하지 않은 3개 이상의 회전축, 같은 pose 반복 제외      |
| 반복            | Noise 조건별 random seed 10개                 |
| Ground truth  | MuJoCo model의 gripper-camera transform    |
| Target pose   | Base에 고정, 모든 pose에서 target이 camera 앞에 존재  |
| 비교 대상         | Tsai, Park                                |
| 단위            | Translation meter, rotation radian으로 입력   |
| Head Pan/Tilt | CAD 기준 사전 정의 각도로 joint 고정, dynamic FK 제외  |

Noise는 세 단계만 사용해 실험 수를 제한한다.

| 조건      | Image point noise | Joint position noise | Timestamp offset |
| ------- | ----------------: | -------------------: | ---------------: |
| Ideal   |              0 px |                   0° |             0 ms |
| Nominal |            0.5 px |                0.05° |            10 ms |
| Stress  |            1.0 px |                0.10° |            30 ms |

총 실행 수는 arm 하나당 2 algorithms × 3 conditions × 10 seeds = 60회다. 좌·우 arm은 dataset과 결과를 분리한다.

### 4.2 비교 지표

- Translation accuracy: ground truth 대비 translation error의 median과 95th percentile, 단위 mm
- Rotation accuracy: ground truth 대비 relative rotation angle의 median과 95th percentile, 단위 degree
- Stability: seed별 결과 분산과 유효 transform 반환 비율
- Held-out consistency: 미사용 pose에서 계산한 base-target pose의 분산
- Implementation difficulty: 추가 dependency, frame 변환, 예외 처리와 결과 해석 복잡도
- Runtime: arm별 1회 calibration 실행 시간. Offline 작업이므로 정확도보다 낮은 우선순위로 둔다.

## 5. 사전 비교와 최종 선정안

| 후보   | 예상 정확도·안정성                   | 구현 난이도 | 이번 선정     |
| ---- | ---------------------------- | ------ | --------- |
| Tsai | 기준선. Rotation noise 영향 확인 필요 | 낮음     | 비교군       |
| Park | 다양한 회전축에서 우선 검증할 기준 후보       | 낮음     | **1차 선정** |

### 5.1 선정 규칙

Park과 Tsai 중 하나를 최종안으로 사용한다. 다음 경우엔 다른 방법론을 고려한다.

1. 유효 결과 비율이 전체 반복의 95% 미만이다.
2. Held-out consistency에서 특정 seed에 결과가 크게 의존하고 같은 현상이 재실행된다.

실제 robot의 mm, degree 합격 기준은 시뮬레이션 상 비교 후 확정한다. 그 값은 gripper, object 크기와 collision margin에서 별도로 정해야 한다.

## 6. SCRUM-264 산출물

~~~yaml
topology: eye_in_hand
arms: [left, right]
primary_method: CALIB_HAND_EYE_PARK
comparison_methods:
  - CALIB_HAND_EYE_TSAI
pnp:
  method: SOLVEPNP_IPPE
  refinement: solvePnPRefineVVS
samples:
  calibration: 20
  held_out: 5
repeats: 10
random_seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
noise_conditions:
  - {name: ideal, pixel_px: 0.0, joint_deg: 0.0, timestamp_ms: 0}
  - {name: nominal, pixel_px: 0.5, joint_deg: 0.05, timestamp_ms: 10}
  - {name: stress, pixel_px: 1.0, joint_deg: 0.10, timestamp_ms: 30}
metrics:
  - translation_error_mm
  - rotation_error_deg
  - held_out_consistency
  - valid_result_rate
  - runtime_ms
head_camera:
  mode: fixed_joint
  pan_angle_deg: from_cad_model
  tilt_angle_deg: from_cad_model
  dynamic_fk: future_advanced_goal
~~~

SCRUM-264 완료 시 다음 산출물을 남긴다.

1. Arm·algorithm·noise·seed별 raw result CSV
2. Translation/rotation error의 median과 95th percentile 비교표
3. Valid result rate와 held-out consistency 표
4. 실패 seed의 pose 분포와 frame 방향 점검 기록
5. Park 유지 또는 Tsai 변경 결론과 근거
6. 최종 transform, dataset revision, OpenCV version과 실행 parameter

## 7. 참고자료

1. [OpenCV Hand-Eye Calibration API](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html#gad3d8c1953e9a6cb109a32e7f7d8dc13d)
2. [OpenCV Perspective-n-Point Reference](https://docs.opencv.org/4.x/d5/d1f/calib3d_solvePnP.html)
3. [MoveIt Low Level Controllers](https://moveit.picknik.ai/main/doc/examples/controller_configuration/controller_configuration_tutorial.html)
4. [ros2_control Controller Manager](https://control.ros.org/jazzy/doc/ros2_control/controller_manager/doc/userdoc.html)
5. [mujoco_ros2_control](https://control.ros.org/humble/doc/mujoco_ros2_control/doc/index.html)
6. [Tsai and Lenz, Hand/Eye Calibration](https://kmlee.gatech.edu/me6406/handeye.pdf)

## 8. 용어 정리

| 용어                               | 설명                                             |
| -------------------------------- | ---------------------------------------------- |
| FK (Forward Kinematics)          | joint 각도로부터 gripper pose를 계산하는 정기구학            |
| PnP (Perspective-n-Point)        | 2D 이미지 점과 3D 점 대응으로 카메라-target pose를 추정하는 문제   |
| SO(3) (Special Orthogonal group) | 3차원 회전만 모은 수학적 군. rotation을 이 구조에서 다룸          |
| TF (Transform)                   | 좌표 프레임 간 변환 트리                                 |
| Quaternion                       | 회전을 4개 수로 표현하는 방식                              |
| Optical frame                    | 카메라 광학 중심 기준 좌표계                               |
| Planar target                    | 평면 위 보정 패턴(예: 체커보드)                            |
| Backlash                         | 기어 유격으로 생기는 위치 오차                              |
| q_fb                             | feedback joint position. 시뮬레이터가 되돌린 실제 joint 값 |
