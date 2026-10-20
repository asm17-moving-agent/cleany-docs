# 조작과 보정(Manipulation and Calibration)

## 요약

조작은 관찰한 물체에 대해 파지 후보를 만들고, 팔의 도달성과 충돌을 검사한 뒤
접근, 집기, 운반, 놓기와 정지를 확인하는 실행 경계다. Task Planner는 다음 행동을
제안하고 Skill이 승인된 행동 하나의 내부 순서를 소유한다.

현재 구현 설명은 `feat/runtime-integration`의 `65fdf06`을 기준으로 한다. Runtime의
외부 조작 Action Mock, plan-only 파지 선택과 MuJoCo sorting은 서로 다른 경로다.

## 경로별로 확인할 수 있는 것

| 경로 | 역할 | 완료로 확대 해석하지 않는 것 |
|---|---|---|
| Runtime의 단일 객체 Action adapter | 승인된 snapshot/object/destination과 execution ID 전달, 결과 보존과 주행 gate | 실제 카메라 및 팔 연결 |
| 파지 후보와 도달성 선택 | 같은 객체의 후보를 양팔 IK, 상태, 충돌 검사와 계획으로 평가 | 실제 trajectory 실행, 파지나 수거 성공 |
| MuJoCo sorting | 센서 기반 인식, 파지, 운반, 놓기와 팔 복귀 실행 | 실물 조작 및 이동 미션과의 통합 |

## 관찰에서 실행까지

```text
같은 시점의 RGB-D와 TF → 객체 mask와 3D OBB 및 점군
→ 파지 후보 생성 → 팔 선택과 IK, 충돌, 계획 검사
→ 접근, 닫기, 접촉 확인 → 들기, 운반 → 놓기, 확인, 팔 복귀
```

인식의 label과 category만으로 파지 가능성을 판정하지 않는다. snapshot/object ID,
좌표와 촬영 시점이 후보 생성부터 실행까지 일치해야 한다. 후보가 없거나 도달할 수
없으면 실패를 반환하고 성공 pose를 합성하지 않는다.

후보 생성에는 geometric predictor와 AnyGrasp adapter가 있다. 모델, checkpoint와
SDK를 요구하는 경로와 모델 없이 동작하는 경로를 구분한다. 특정 launch가 선택한
predictor를 모든 실행의 기본값이나 Jetson에서 검증된 선택으로 일반화하지 않는다.

## 5축 팔과 계획의 한계

기본 MoveIt 팔 그룹은 5개 관절의 position-only IK를 사용한다. 이 IK의 성공만으로
목표 TCP 방향을 만족했다고 판단하지 않는다. 조작 실행 경로는 aim-tip 및 FK 방향
검사 같은 추가 조건을 사용하며, 각 경로가 확인한 위치, 방향 조건을 구분해야 한다.

실행 전 검사에서는 최신 joint state, 객체와 환경 충돌 형상, 접근과 운반 경로를
확인한다. plan-only 결과를 나중에 그대로 재생하지 않고 현재 상태에 맞는 실행 계획과
controller 결과를 확인한다. Simulation 전용 접근 보정과 속도는 실물 허용값이 아니다.

## 결과, 물체 상태와 놓기 검증

Runtime은 ROS terminal 상태뿐 아니라 payload의 행동 결과, execution ID, 출처,
물체 상태, 놓기 확인, 팔 복귀와 정지를 대조한다. 결과가 불명확하면 같은 execution
ID의 기록을 조회하며 새 ID로 같은 동작을 자동 재실행하지 않는다.

물체를 잡았거나 보유 여부가 불명확하거나 팔 복귀, 정지를 확인하지 못하면 다음
미션과 home 이동을 허용하지 않는다. 실패와 취소에서도 이미 확인한 상태를 보존한다.
일반적인 결과 원칙은 [Mission Lifecycle](<09 - Mission Lifecycle.md>)을 따른다.

MuJoCo sorting의 작업자 관찰 모드는 놓기 자동 검증을 생략하고
`complete_unverified`, `placement_verified=false`로 기록한다. 이 결과는 안착 검증
성공이 아니다. 자동 검증 모드의 simulator ground truth도 평가자 입력이며 제어와
인식의 입력으로 섞지 않는다. 실물 수거 완료 기준은 해당 센서와 검증 근거가 필요하다.

분실물의 전용 보관함 투입은 시뮬레이션에 존재한다. 이를 제품 처리 정책으로
채택할지는 [Planning Questions](<../10_PLANNING/99 - Questions.md>)의 판단을 따른다.
VLA는 확장 후보이며 현재 MoveIt 실행을 VLA 구현으로 부르지 않는다.

## 보정과 좌표, 시간

Hand-eye 보정 도구는 촬영 시점의 관절 피드백 FK와 ChArUco PnP를 짝지어 손목
카메라 변환을 추정한다. 명령한 joint 목표값을 실제 촬영 시점의 팔 자세로 대신하지
않는다. 카메라 내부 보정, 장착 TF와 시간 동기화는 함께 확인해야 한다.

보정 solver 입력과 평가용 ground truth를 구분하고, 추정에 사용하지 않은 held-out
관찰의 일관성도 확인한다. 생성된 변환은 검토용 산출물이며 자동으로 calibration TF에
적용되지 않는다. 실제 장착, 촬영 조건과 다른 synthetic 또는 MuJoCo 결과만으로
실물 보정 정확성을 선언하지 않는다.

## 통합 시 확인할 경계

실제 관찰을 Runtime에 공급하고 승인된 행동을 조작 서버에 연결할 때 snapshot,
중복 실행, 취소, 정지와 물체 보유 의미가 보존돼야 한다. 첫 조작 전 자료 로컬 저장과
Backend 재전송은 합의된 목표 정책이며 파지 데모의 이미지 표시와 구분한다.

## 관련 문서

- [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>)
- [Perception and Scene Understanding](<07 - Perception and Scene Understanding.md>)
- [Mission Lifecycle](<09 - Mission Lifecycle.md>)
- [Verification and Simulation Strategy](<13 - Verification and Simulation Strategy.md>)

## 출처

- [단일 객체 Action과 결과 계약 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_interfaces/docs/manipulation.md)
- [조작 실행 및 시뮬레이션의 제약 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_skill_executor/docs/manipulation.md)
- [MoveIt planning 계약 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_moveit_config/docs/planning.md)
- [파지 predictor 경계 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_grasping/docs/predictors.md)
- [보정 좌표와 dataset 계약 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_handeye_calibration/docs/frames-and-data.md)

## 관련 결정

- [261017 - MoveIt과 규칙 기반 조작의 MVP 인정](<../30_DECISIONS/Planning/261017 - MoveIt과 규칙 기반 조작의 MVP 인정.md>)
- [260806 - Task Planning과 Robot Capability 경계](<../30_DECISIONS/Technical/260806 - Task Planning과 Robot Capability 경계.md>)
- [261002 - Manipulation 결과와 안전 상태 보존](<../30_DECISIONS/Technical/261002 - Manipulation 결과와 안전 상태 보존.md>)
- [261002 - 관찰 자료 로컬 저장과 Backend 재전송](<../30_DECISIONS/Technical/261002 - 관찰 자료 로컬 저장과 Backend 재전송.md>)
