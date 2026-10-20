# 인식과 장면 이해(Perception and Scene Understanding)

## 요약

Perception은 센서 입력을 Planner와 Manipulation이 사용할 수 있는 Scene State로
변환한다. 현재 인식 경로는 YOLOE-seg의 물체 영역과 mask 및 Gemini의 의미 분류를
사용한다. Depth와 촬영 시점 TF를 이용한 3D 추정은 별도 단계로 검증한다.

## 출력 계약

Scene State는 최소한 다음 의미를 제공해야 한다.

| 정보 | 소비자 | 용도 |
|---|---|---|
| 관찰 ID, 시점, camera frame | Mission, Logger | 작업 전후 관찰 구분 |
| object ID와 image region | Planner, Segmentation | 장면 내 대상 식별 |
| 의미 후보와 신뢰 정보 | Planner, Mission Manager | 쓰레기, 분실물 후보, 불확실 구분 |
| mask 또는 object extent | 3D Estimation, Manipulation | 물체 영역과 배경 분리 |
| base 기준 위치, 품질 | Manipulation Capability, Robot backend | 접근 가능성, 좌표 유효성 확인 |
| 처리 가능 여부와 이유 | Planner, Reporter | 실행, skip, 실패 구분 |

정확한 ROS message와 schema는 구현 레포의 Scene/Grasp 계약과 Perception reference에서 관리한다.

## 평가할 Perception 경로

```text
동기화 RGB-D와 촬영 시점 TF
→ YOLOE-seg 물체 영역 및 instance mask → Gemini label, category, reason
→ 선택 객체의 depth와 지지면 → base 기준 3D OBB 및 점군
```

`65fdf06`의 인식 경로는 같은 snapshot에서 객체 식별, 분류와 조작용 좌표를 연결한다.
손목 RGB는 HANDOFF와 파지 후 CHECK에서 새 영상을 독립적으로 검출한다.
RGB-only 손목 결과를 독립적인 새 3D 좌표나 실제 물체 보유의 유일한 증거로 쓰지 않는다.
정상 미검출과 sensor, TF, model 오류를 구분한다.

시뮬레이션 학습 checkpoint, 합성 입력의 성능과 실제 D435, 손목 영상의 성능을
구분한다. 현재 경로를 명시하되 Jetson 동시 실행 성능이나 실물 일반화 완료를
선언하지 않는다. ER 2→SAM2→Depth는 과거 사전 실험이며 현재 경로에 포함하지 않는다.

## Adapter 원칙

- 물체 영역과 mask, 의미 분류 및 3D 추정은 구분된 결과로 검증한다.
- 의미 분류와 실행 제안을 같은 값으로 취급하지 않는다.
- 각 단계는 입력, 출력, 품질과 실패 이유를 별도로 검증한다.
- Planner가 낸 의미 판단을 최종 좌표, grasp 가능성으로 사용하지 않는다.
- 장면이 바뀌면 오래된 mask, depth, object ID를 재사용하지 않는다.

## 작업 전후와 행동 checkpoint 관찰

작업 전 관찰은 대상과 초기 상태를, 작업 후 관찰은 실제 변화와 남은 대상을
증명한다. 두 관찰은 Dashboard 결과와 Planner 폐루프에서 같은 ID 체계로 연결되어야
한다. 각 high-level 행동이 성공, 안전하게 정지한 실패 또는 실행 전 차단으로 끝나면
최신 Scene을 생성해 다음 Planner 판단의 checkpoint로 사용한다. VLM을 선택하면
이 checkpoint에서 재추론한다. 취소와 치명 오류의 종료 경로는
[Mission Lifecycle](<09 - Mission Lifecycle.md>)에서 관리한다.
FSM+BT Runtime `65fdf06`에는 행동별 재관찰과 완료 재확인이 있으나 입력은 Mock이다.
별도 Perception 구현은 YOLOE-seg와 Gemini를 사용하며, 실제 관찰 결과를 Runtime에
연결하는 통합이 남아 있다. Supervisor 브랜치의 순차 core와 이 Runtime을 구분한다.

행동별 checkpoint 관찰은 내부 재판단에 사용한다. Backend로 보내는 사진은 작업 시작 전
사진과 최종 사진으로 제한한다. 최종 사진은 처리 가능한 물체를 모두 치웠거나, 남은
물체를 더 처리할 수 없을 때 촬영한다.

## 상위단에 전달할 관찰 자료

전달 자료의 필수 항목은 같은 관찰의 원본 이미지, bbox, 물체별 라벨과 분류다. bbox는
원본 이미지의 크기와 같은 좌표 기준을 사용하며 자료에는 snapshot ID, 촬영 시각과
이미지 가로, 세로 크기도 포함한다. 분류 결과와 Planner의 처리 제안은 구분한다.
상위단은 전달 자료로 이미지 위에 물체 영역과 라벨을 표시할 수 있다.

작업 전 사진과 해당 관찰의 인식 정보는 첫 조작 전에 로컬에 저장한다. Mission
Manager는 저장 성공을 확인한 뒤 조작을 허용하며, 저장에 실패하면 첫 조작을
시작하지 않는다. Backend 전송과 저장 확인은 로컬 저장과 구분하고, Backend 저장
확인을 기다리지 않고 물체 처리를 진행한다. 최종 사진과 인식 정보도 로컬에 저장해
같은 미션 결과에 연결한다. 빈 관찰은 원본 사진과 빈 물체 목록으로 표현한다.

사진 전송은 제한된 자동 재시도와 운영자의 수동 재전송을 지원한다. 같은 관찰 ID로
사진과 인식 정보를 재전송하고 Backend가 중복 저장을 막는다. 로컬 발행이나 전송
요청의 성공만으로 Backend 저장이 확인됐다고 판단하지 않는다.

Backend 저장이 확인되면 로컬 사본을 삭제할 수 있다. 미전송 자료는 별도로 정할
보관 기한을 적용하고, 삭제하더라도 미전송 사실과 사유는 기록에 남긴다. 전송
재시도와 조작 재실행은 구분한다. 이 절은 목표 전달 정책이며 전송 기능의 구현
완료를 뜻하지 않는다. 정확한 payload와 전송 interface는 구현 명세에서 정하고,
재시도 설정과 미전송 자료의 보관 기한은 [Technical Questions](<99 - Questions.md>)에서
관리한다. Backend에 저장된 자료의 보관 기간과 접근 권한은
[Planning Questions](<../10_PLANNING/99 - Questions.md>)에서 관리한다.

## 모델 평가 관점

현재 인식 경로는 현재 데모 입력에서 다음 항목을 기준으로 검증한다.

- 대상 누락, 오탐과 의미 분류 오류
- region, mask, 3D 좌표의 조작 적합성
- 여러 물체에서의 ID, 순서 일관성
- 처리 지연과 cloud/network 실패
- 실패를 정상 Scene State로 포장하지 않는가
- 비용, 데이터 전송과 개인정보 조건

## 관련 문서

- [Manipulation and Calibration](<15 - Manipulation and Calibration.md>)
- [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>)
- [Edge Runtime Jetson Orin](<06 - Edge Runtime Jetson Orin.md>)
- [Verification and Simulation Strategy](<13 - Verification and Simulation Strategy.md>)

## 출처

- [현재 Perception 입력, 실패, 손목 관측 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_perception/docs/runtime.md)
- [Scene와 Grasp 공유 의미 at 65fdf06](https://github.com/asm17-moving-agent/cleany/blob/65fdf061bcc564f4d362b1994b633d7235df66d7/ros2_ws/src/cleany_interfaces/docs/scene-and-grasp.md)

- [과거 ER 2와 SAM2 사전 실측](<../40_RAW/260804 - 인식 파이프라인 로컬 실측 검증/00 - README.md>)
- [책상 정리 작업 흐름과 Action 최신화 논의](<../40_RAW/260930 - Table Cleanup Workflow.md>)
- [Action 결과와 관찰 자료 전달 정책 합의](<../40_RAW/261002 - Action 결과와 관찰 자료 전달 정책 합의.md>)

## 관련 결정

- [260806 - Task Planning과 Robot Capability 경계](<../30_DECISIONS/Technical/260806 - Task Planning과 Robot Capability 경계.md>)
- [261002 - Manipulation 결과와 안전 상태 보존](<../30_DECISIONS/Technical/261002 - Manipulation 결과와 안전 상태 보존.md>)
- [261002 - 관찰 자료 로컬 저장과 Backend 재전송](<../30_DECISIONS/Technical/261002 - 관찰 자료 로컬 저장과 Backend 재전송.md>)
