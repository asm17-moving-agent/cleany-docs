---
type: raw-research
reviewers:
  - 이정현
ingest_status: raw
ingest_targets:
  - technical
  - decision
decision_candidates:
  - 정확도 비교 결과에 따라 OpenCV CALIB_HAND_EYE_PARK 또는 CALIB_HAND_EYE_TSAI를 simulation 기준 알고리즘으로 사용
date: 2026-07-20
related_jira:
  - SCRUM-264
tags:
  - raw
  - research
  - xlerobot
  - hand-eye-calibration
  - simulation
---

# 260720 - Simulation 기반 Hand-Eye Calibration 방법론 선정

## 1. 목표와 결론

이 문서에선 XLeRobot simulation에서 사용할 hand-eye calibration 방법론을 비교하고 PnP, solver 알고리즘과 실험 조건을 결정한다. 1차 범위는 좌측 wrist camera의 eye-in-hand calibration이다. 우측 wrist camera는 이번 실험에서 제외한다. Head Pan/Tilt D435의 동적 FK는 향후 고도화 목표로 두고, 현재는 XLeRobot의 D435 gimbal STL과 robot description에서 정한 pan/tilt joint 초기값을 고정한 뒤 camera optical frame과 FOV만 검증한다.

선정 후보는 Tsai와 Park이다. 선정 이유는 다음과 같다.

- OpenCV 표준 API로 구현할 수 있어 별도 solver 개발이 필요 없다.
- Rotation을 SO(3) 구조에서 다루는 방식이라 다양한 회전축을 포함한 dataset의 기준 알고리즘으로 쓰기 적합하다.
- 입력과 출력이 다른 OpenCV hand-eye method와 같아 동일 dataset에서 비교하기 쉽다.
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

### 2.2 ROS 2 Humble 기준 Simulation 실행 경로

SCRUM-264의 목표 실행 경로는 ROS 2 Humble을 기준으로 아래와 같이 구성한다. 현재 `cleany_mujoco_sim`의 private `~/joint_cmd`는 simulation test hook이며, 아래 경로가 구현됐다고 간주하지 않는다. 실제 실험 전 `FollowJointTrajectory` action, `joint_trajectory_controller`와 `MujocoSystemInterface` 연결을 별도로 확인한다.

~~~text
MoveIt
  -> FollowJointTrajectory
  -> ros2_control joint_trajectory_controller
  -> mujoco_ros2_control/MujocoSystemInterface
  -> MuJoCo actuator·physics
  -> joint state interface
  -> /joint_states·TF·calibration collector
~~~

Calibration collector는 MuJoCo state interface가 반환한 feedback joint position `q_fb`로 FK를 계산한다. Image와 joint state는 ROS simulation clock 기준으로 묶고, 원본 timestamp와 보간에 사용한 timestamp를 모두 기록한다. Calibration 결과는 robot description의 camera mount transform 후보로만 적용하며, 실험 결과 검토 전에는 공식 transform으로 확정하지 않는다.

### 2.3 Head Pan/Tilt의 현재 범위

XLeRobot 공식 저장소에는 D435용 [`Gimbal_mesh_all_d435.stl`](https://github.com/Vector-Wangel/XLeRobot/blob/main/hardware/camera_connector/Gimbal_mesh_all_d435.stl)이 있다. 현재 단계에서는 이 STL을 D435 장착 가능성의 근거로 사용하되, 실험에 사용한 XLeRobot commit SHA, robot description revision과 실제 pan/tilt 초기 각도를 dataset manifest에 기록한다.

D435의 pan/tilt joint는 simulation 중 움직이지 않는다. 기록한 pan angle과 tilt angle을 joint 초기값으로 고정하고 다음 항목만 확인한다.

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

PnP는 hand-eye method 비교와 분리한다. 모든 method에 동일한 ${}^{c}\mathbf{T}_{t}$를 제공해야 hand-eye solver만 비교할 수 있다. Planar target의 PnP 처리 순서는 다음과 같다.

1. `solvePnPGeneric(..., flags=SOLVEPNP_IPPE)`로 두 pose 후보를 받는다. `solvePnP()`는 복수해 확인 경로로 사용하지 않는다.
2. NaN·infinity가 있거나 target의 3D point 중 하나라도 camera 뒤쪽($Z \le 0$)에 놓이는 후보는 제외한다.
3. 남은 각 후보를 동일한 object point, image point, camera intrinsics와 distortion coefficients로 `solvePnPRefineVVS`에 전달한다.
4. refinement 뒤 cheirality를 다시 확인하고 전체 point의 reprojection RMSE를 계산한다.
5. 유효 후보가 하나면 그 후보를 사용한다. 두 후보가 모두 유효하면 reprojection RMSE가 작은 후보를 사용한다.
6. `best_rmse > 10^{-12}`일 때 `second_best_rmse / best_rmse < 1.05`면 두 해가 충분히 구분되지 않는 것으로 본다. 두 RMSE가 모두 $10^{-12}$ 이하면 같은 이유로 모호한 해로 본다. 해당 pose는 `ambiguous_pnp`로 제외한 뒤 더 큰 관측 각도로 다시 수집한다.
7. Simulation ground truth는 PnP 후보 선택에 사용하지 않고 최종 calibration accuracy 평가에만 사용한다.

각 pose에는 두 원본 후보, refinement 결과, cheirality 판정, reprojection RMSE와 최종 선택 사유를 남긴다.

## 4. 비교 기준과 실험 조건

### 4.1 공통 실험 조건

| 항목            | 조건                                                    |
| ------------- | ----------------------------------------------------- |
| Topology      | 좌측 wrist camera eye-in-hand                           |
| Dataset       | 좌측 arm calibration 20 pose, held-out 5 pose            |
| Pose 구성       | 서로 평행하지 않은 3개 이상의 회전축, 같은 pose 반복 제외                  |
| 반복            | Noise 조건별 random seed 10개                             |
| Ground truth  | MuJoCo model의 left gripper-camera transform             |
| Target pose   | Base에 고정, 모든 pose에서 target 전체가 image 안에 있고 camera 앞에 존재 |
| 비교 대상         | Tsai, Park                                            |
| 단위            | Translation meter, rotation matrix 또는 Rodrigues vector radian |
| Head Pan/Tilt | 기록한 초기 각도로 joint 고정, dynamic FK 제외                    |

두 알고리즘은 동일한 underlying pose, PnP 결과와 noise sample을 사용한다. Dataset revision이 바뀌면 이전 실행 결과와 섞지 않는다. 실험 전에 다음 값을 dataset manifest에 고정한다.

- Camera: image width·height, camera matrix, distortion coefficients, optical frame 이름과 MuJoCo camera parameter
- Target: pattern 종류, 행·열 수, point ordering, 전체 크기, square 또는 marker 크기와 target frame 정의
- Robot: URDF/MJCF revision, XLeRobot commit SHA, D435 STL 경로, left gripper frame, pan/tilt 초기 각도
- Acquisition: trajectory revision, simulation timestep, render rate, joint state rate, interpolation 방식과 sample timestamp

Image point와 joint position noise는 평균이 0인 독립 Gaussian noise로 생성하고 아래 값은 표준편차 $\sigma$로 해석한다. Image point noise는 각 corner의 $u$, $v$에 독립 적용한다. Joint position noise는 각 pose의 measured `q_fb`에 joint별로 적용한 뒤 FK를 다시 계산한다. 같은 condition·seed에서는 두 알고리즘에 동일한 noise sample을 사용한다.

| 조건      | Image point noise $\sigma$ | Joint position noise $\sigma$ |
| ------- | --------------------------: | -----------------------------: |
| Ideal   |                        0 px |                             0° |
| Nominal |                      0.5 px |                          0.05° |
| Stress  |                      1.0 px |                          0.10° |

알고리즘 비교는 좌측 arm에서 2 algorithms × 3 conditions × 10 seeds = 60회 실행한다.

Timestamp 영향은 정지 pose에서 의미가 없으므로 알고리즘 정확도 비교와 분리한다. 최종 선정된 method로 non-zero joint velocity가 있는 동일한 continuous trajectory log를 재생하고, image timestamp $t$에 대해 FK 입력을 $t + \Delta t$에서 선형 보간한다. $\Delta t \in \{-30, -10, 10, 30\}$ ms를 seed별 10회 적용해 40회 추가 실행한다. 이 결과는 synchronization 민감도 지표로만 사용하고 hand-eye method 정확도 순위를 뒤집는 근거로 사용하지 않는다.

### 4.2 비교 지표

- Translation accuracy: ground truth 대비 translation error의 median과 95th percentile, 단위 mm
- Rotation accuracy: ground truth 대비 relative rotation angle의 median과 95th percentile, 단위 degree
- Stability: seed별 결과 분산과 유효 transform 반환 비율
- Held-out consistency: 미사용 pose에서 계산한 base-target pose의 분산
- Implementation difficulty: 추가 dependency, frame 변환, 예외 처리와 결과 해석 복잡도
- Runtime: arm별 1회 calibration 실행 시간. Offline 작업이므로 정확도보다 낮은 우선순위로 둔다.

유효 transform은 모든 값이 finite이고, $\lVert R^T R-I\rVert_F \le 10^{-6}$이며, $|\det(R)-1| \le 10^{-6}$인 결과로 정의한다.

## 5. 사전 비교와 최종 선정안

| 후보   | 예상 정확도·안정성                   | 구현 난이도 | 이번 역할      |
| ---- | ---------------------------- | ------ | ---------- |
| Tsai | 기준선. Rotation noise 영향 확인 필요 | 낮음     | 정확도 비교 후보   |
| Park | 다양한 회전축에서 우선 검증할 기준 후보       | 낮음     | 초기 reference |

### 5.1 선정 규칙

Park과 Tsai 중 정확도가 우수한 방법을 최종안으로 사용한다. 선정 순서는 다음과 같다.

1. 유효 결과 비율이 전체 반복의 95% 이상인 후보만 비교한다.
2. Translation error와 rotation error의 median·95th percentile 네 지표에서 한 후보가 모두 같거나 낮고 하나 이상에서 낮으면 그 후보를 선택한다.
3. 두 후보의 accuracy 지표가 서로 엇갈리면 held-out consistency가 더 낮은 후보를 우선한다.
4. Held-out consistency까지 엇갈리면 자동 선정하지 않고 gripper, object 크기와 collision margin에서 정한 translation·rotation 허용오차로 사람이 검토한다.
5. Implementation difficulty와 runtime은 정확도가 동등한 경우에만 보조 기준으로 사용한다.
6. 두 후보 모두 유효 결과 비율이 95% 미만이거나 특정 seed 의존성이 재현되면 Horaud, Andreff 또는 Daniilidis를 추가 비교한다.

실제 robot의 mm, degree 합격 기준은 시뮬레이션 비교 후 확정한다. 기준 확정 전에는 Park 또는 Tsai를 selected Decision으로 승격하지 않는다.

## 6. SCRUM-264 산출물

~~~yaml
topology: eye_in_hand
arms: [left]
initial_reference_method: CALIB_HAND_EYE_PARK
candidate_methods:
  - CALIB_HAND_EYE_PARK
  - CALIB_HAND_EYE_TSAI
selection_priority: accuracy
pnp:
  solver: solvePnPGeneric
  method: SOLVEPNP_IPPE
  expected_solutions: 2
  refinement: solvePnPRefineVVS
  selection: minimum_reprojection_rmse
  ambiguity_ratio_min: 1.05
  ground_truth_for_selection: false
samples:
  calibration: 20
  held_out: 5
repeats: 10
random_seeds: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
noise_conditions:
  distribution: independent_zero_mean_gaussian
  values_are: standard_deviation
  levels:
    - {name: ideal, pixel_px: 0.0, joint_deg: 0.0}
    - {name: nominal, pixel_px: 0.5, joint_deg: 0.05}
    - {name: stress, pixel_px: 1.0, joint_deg: 0.10}
timestamp_sensitivity:
  selected_method_only: true
  moving_trajectory_only: true
  offsets_ms: [-30, -10, 10, 30]
  repeats: 10
metrics:
  - translation_error_mm
  - rotation_error_deg
  - held_out_consistency
  - valid_result_rate
  - runtime_ms
head_camera:
  model: Intel RealSense D435
  cad_source: XLeRobot/hardware/camera_connector/Gimbal_mesh_all_d435.stl
  mode: fixed_joint
  pan_angle_deg: record_in_dataset_manifest
  tilt_angle_deg: record_in_dataset_manifest
  dynamic_fk: future_advanced_goal
~~~

SCRUM-264 완료 시 다음 산출물을 남긴다.

1. 좌측 arm의 algorithm·noise·seed별 raw result CSV
2. Translation/rotation error의 median과 95th percentile 비교표
3. Valid result rate와 held-out consistency 표
4. PnP 후보별 refinement·cheirality·reprojection RMSE와 ambiguity 판정 기록
5. Timestamp offset별 synchronization 민감도 표
6. 실패 seed의 pose 분포와 frame 방향 점검 기록
7. 정확도 우선 선정 결과와 근거
8. 최종 transform, dataset manifest, OpenCV version과 실행 parameter

## 7. 참고자료

1. [OpenCV Hand-Eye Calibration API](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html#gad3d8c1953e9a6cb109a32e7f7d8dc13d)
2. [OpenCV Perspective-n-Point Reference](https://docs.opencv.org/4.x/d5/d1f/calib3d_solvePnP.html)
3. [MoveIt Humble Low Level Controllers](https://moveit.picknik.ai/humble/doc/examples/controller_configuration/controller_configuration_tutorial.html)
4. [ros2_control Humble Controller Manager](https://control.ros.org/humble/doc/ros2_control/controller_manager/doc/userdoc.html)
5. [mujoco_ros2_control](https://control.ros.org/humble/doc/mujoco_ros2_control/doc/index.html)
6. [Tsai and Lenz, Hand/Eye Calibration](https://kmlee.gatech.edu/me6406/handeye.pdf)
7. [Park and Martin, Robot Sensor Calibration](https://doi.org/10.1109/70.326576)
8. [XLeRobot D435 Gimbal STL](https://github.com/Vector-Wangel/XLeRobot/blob/main/hardware/camera_connector/Gimbal_mesh_all_d435.stl)

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
