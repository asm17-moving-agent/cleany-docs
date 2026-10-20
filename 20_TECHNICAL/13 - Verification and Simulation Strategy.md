# 검증과 시뮬레이션 전략(Verification and Simulation Strategy)

## 요약

Cleany는 Rule-based E2E 통합, 후보 추론 경로 비교, physical execution, 실제 로봇 순으로
검증한다. Gazebo와 MuJoCo는 서로 대체하는 simulator가 아니라 다른 subsystem 경계를
담당한다.

## 검증 단계

| 단계 | 검증 목표 | 통과 기준 |
|---|---|---|
| Core | Mission, Planner, Capability와 Supervisor 검증 순수 logic | 성공, 실패, 차단, Fault, 허가와 복구 경로가 재현됨 |
| Supervisor ROS 통합 | Health, 실행 허가, Mission stop과 component recovery 경계 | synthetic peer에서 만료, 재시작, 완료 확인과 실패 제한이 재현됨 |
| Rule-based 통합 | Dashboard 요청부터 report까지 E2E 경계 | 고정 입력에서 전체 lifecycle이 연결됨 |
| Perception | image→mask→3D→Scene State | 실패를 포함한 각 adapter 계약이 확인됨 |
| Navigation Sim | 좌석 왕복과 cancel, failure | Gazebo에서 Nav2, base, sensor 경계가 동작함 |
| Manipulation Sim | 여러 물체와 physical skill | MoveIt, 규칙 기반 Skill의 계획, 실행과 물체, 놓기 결과를 구분해 확인함 |
| Perception baseline | YOLOE-seg 물체 영역과 instance mask 및 Gemini 의미 분류 | 정확도, 지연, 실패 사례를 같은 Scene State 계약에서 검증함 |
| Planner 통합 | 선택된 Planner adapter의 task order와 tool orchestration | 행동마다 허용 tool 하나만 실행되고 새 장면으로 재판단함 |
| Real Robot | 실제 sensor, base, arm, safety | 승인된 통제 시나리오를 전후 결과와 함께 수행함 |

현재는 정량 성공률보다 각 단계의 pass/fail과 실패 증거를 우선 기록한다.

## 구현별 검증 경계

| 근거와 경로 | 판정에 필요한 증거 | 합쳐서 주장하지 않는 것 |
|---|---|---|
| 소스, 설정, reference 대조 | 저장소, branch, commit과 실제 선택된 profile | 실행 성공이나 팀의 과거 채택 이유 |
| Core와 합성 ROS transport | 상태, 계약, 실패 입력, 취소와 중복 실행 결과 | 실제 센서, motor 및 물체 정리 |
| Gateway와 Runtime Mock | 요청, 수락, journal, 재연결, 원래 outcome 보존 | 사진 저장 확인이나 실제 책상 조작 |
| Gazebo 주행 | 목표와 localization 오차, 정지, 별도 ground-truth 오차 | 팔 도달성, 실환경 위치 정확도 |
| MuJoCo 조작 | 인식 입력, 후보, 실제 controller 실행, 물체, 놓기 확인 | Runtime 전체 통합과 실물 파지 |
| 관찰 모드의 놓기 | `placement_verified=false` 및 작업자 관찰 | 자동 안착 확인 성공 |
| 실물 통합 | 실제 sensor 수신, 구동, 정지, 관찰, 물체 상태와 전후 결과 | 열거, node 준비나 합성 응답만으로 완료 판정 |

2026-10-17 KB 최신화는 문서와 소스를 대조했다. 위 Runtime, base, Supervisor와
Control Plane의 서로 다른 commit을 하나의 현재 배포나 새 E2E 시험으로 합치지 않았다.
과거 실행 원본은 구현 레포의 `docs/EVIDENCE.md`에서 찾고, 현재 검증은 새 run의
입력과 환경 및 최초 실패부터의 결과를 남겨야 한다.

## Supervisor 검증 증거의 경계

`feat/system-supervisor`의 `c63fadb`에서 기록한 검증은 로컬 Humble build, pure core와
synthetic ROS graph다. 이 기록을 원격 CI 실행, Nav2 실주행이나 실제 하드웨어
안전 검증으로 확대 해석하지 않는다. 실행 명령, 결과 수와 fixture는 구현 README를 따른다.

| 검증 | 확인하는 것 | 확인하지 못하는 것 |
|---|---|---|
| Pure core | 상태 전이, 동시 Fault, 해제 조건, 기능 의존성, 허가 만료 및 복구 예산 | 실제 sensor, actuator와 통신 지연 |
| Synthetic ROS graph | health와 lifecycle 입력, 허가 갱신 및 철회, restart, Action 수락과 완료 구분 | 실제 Nav2 경로 실행, Arm 정지와 물리 Recovery |
| 기본 launch | 필수 상태 증거가 없으면 자동 운영이 잠김 | 실물 안전 회로 또는 센서 정확성 |
| 실물 통합 | 추가 검증 필요 | 위 자동 검사만으로 통과를 선언하지 않음 |

실물 검증에서는 ESP32 통신 차단과 하위 watchdog, 실제 모터 정지, Supervisor 및
Mission 종료, E-stop 작동과 물리 해제, 팔 상태와 물체 보유를 포함한 재개 판단을
각각 확인해야 한다. 정지 요청 전달, 수락, 실제 정지와 복구 뒤 health 증거를 별도로
기록한다. 실제 safety 및 Recovery 제공자가 없으면 성공을 모사해 실물 통과로 기록하지 않는다.

## Simulator 책임

### Gazebo

- 4륜 Mecanum base와 `cmd_vel` 의미
- odometry, LiDAR, IMU, camera와 TF
- prebuilt map, localization, Nav2 goal과 복귀
- 장애물, timeout, cancel, safe stop 전달

### MuJoCo

- 좌석 도착 후 arm과 gripper의 tabletop workspace
- pick, place, collect 같은 Manipulation Skill
- MoveIt, 규칙 기반 Skill과 controller backend
- collision, timeout, grasp 실패, 물체의 낙하 또는 전도와 결과 반환

Isaac Sim은 현재 공식 검증 구조에 역할을 배정하지 않는다. 필요하면 Raw 연구
후보로만 평가한다.

## E2E 검증 흐름

1. Dashboard가 개별 좌석 요청을 보낸다.
2. Mission Manager가 Gazebo 또는 실제 Navigator로 좌석 도착을 확인한다.
3. 작업 전 관찰을 Scene State로 변환한다.
4. RuleBasedPlanner 또는 측정 중인 Planner adapter가 다음 high-level 행동 하나를 제안한다.
5. Mission Manager가 상태, allowlist, 기본 argument를 검증한다.
6. MuJoCo 또는 실제 Manipulation backend가 물리 제약을 검증하고 skill을 실행한다.
7. 행동 결과와 안전 상태를 기록하고, 다음 판단을 안전하게 진행할 수 있으면 장면을 재관찰한다.
8. 실행 결과와 최신 Scene으로 다음 행동 또는 완료 여부를 재판단한다.
9. 최종 관찰을 확인한 뒤 복귀와 MissionReport를 완료한다.

작업 전 자료의 로컬 저장 실패에서는 첫 조작을 시작하지 않는다. 취소는 진행 기록을
보존해 종료 경로로 연결하고, 치명 오류 또는 정지 미확인에서는 후속 동작을 차단해
사람 확인 필요를 보고한다.

Simulator 사이를 반드시 실시간으로 연결할 필요는 없다. 공통 Mission, Scene, Capability
결과 계약으로 subsystem 검증 결과를 연결한다.

## 증거와 실패 기록

- 저장소별 commit, 실행 환경, 입력 Mission, 모델, 지도와 config 식별자
- 각 단계의 real/sim/mock 출처, 비활성화한 보호 단계와 최초 실패 및 후속 재실행 결과
- 작업 전후 관찰
- Planner proposal과 Mission, Capability 검증의 승인, 거절 이유
- Capability별 success, failed, blocked 결과
- Manipulation의 취소와 치명 오류, 실패 이유, 정지 확인, 물체 보유 상태와 놓기 검증 상태
- 작업 전후 자료의 로컬 저장 결과, Backend 저장 확인, 전송 재시도와 중복 저장 판별 결과
- 행동 전후 Scene과 물체의 낙하 또는 전도 같은 예상 밖 변화
- Navigation, Perception, Planning, Manipulation 중 실패 경계
- Supervisor 실행 세대와 허가 철회 및 만료, 중단 요청 수락과 실제 정지 완료의 구분
- 활성 Fault 집합, 제한된 기능, recovery 시도 및 취소 확인과 복구 뒤 fresh health 증거
- 실제 로봇에서는 감독자, 작업 구역, e-stop 준비 확인

## 구현 검증 문서 경계

정확한 build, pytest, colcon, launch와 CI 명령은 구현 레포의 실행, 검증 가이드와
해당 패키지 reference가 관리한다. KB는 제품 단계와 검증 증거의 의미를 관리한다. KB 자체 Markdown
무결성 검사는 AGENTS와 repo skill 안내를 따른다.

## 관련 문서

- [Manipulation and Calibration](<15 - Manipulation and Calibration.md>)
- [Success Criteria](<../10_PLANNING/05 - Success Criteria.md>)
- [Navigation and Mapping](<05 - Navigation and Mapping.md>)
- [Perception and Scene Understanding](<07 - Perception and Scene Understanding.md>)
- [System Supervisor](<14 - System Supervisor.md>)

## 출처

- [현재 검사 선택과 증거 범위 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/docs/TESTING.md)
- [과거 실행 원본 색인 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/docs/EVIDENCE.md)
- [조작의 미검증 놓기 모드 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_skill_executor/docs/manipulation.md)

- [Supervisor 구현 및 검증 기록 at c63fadb](https://github.com/asm17-moving-agent/cleany/blob/c63fadb467afac08cc62a3cfd0a5af7c59b6e8b7/ros2_ws/src/cleany_system_supervisor/README.md)
- [05 - Success Criteria](<../10_PLANNING/05 - Success Criteria.md>)
- [Action 결과와 관찰 자료 전달 정책 합의](<../40_RAW/261002 - Action 결과와 관찰 자료 전달 정책 합의.md>)

## 관련 결정

- [261016 - System Supervisor 책임과 안전 경계](<../30_DECISIONS/Technical/261016 - System Supervisor 책임과 안전 경계.md>)
- [260708 - MVP 기능 범위](<../30_DECISIONS/Planning/260708 - MVP 기능 범위.md>)
- [260806 - Task Planning과 Robot Capability 경계](<../30_DECISIONS/Technical/260806 - Task Planning과 Robot Capability 경계.md>)
- [261002 - Manipulation 결과와 안전 상태 보존](<../30_DECISIONS/Technical/261002 - Manipulation 결과와 안전 상태 보존.md>)
- [261002 - 관찰 자료 로컬 저장과 Backend 재전송](<../30_DECISIONS/Technical/261002 - 관찰 자료 로컬 저장과 Backend 재전송.md>)
