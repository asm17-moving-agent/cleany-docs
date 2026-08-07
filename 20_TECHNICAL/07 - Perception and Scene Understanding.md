# 인식과 장면 이해(Perception and Scene Understanding)

## 요약

Perception은 센서 입력을 Planner와 Manipulation이 사용할 수 있는 Scene State로
변환한다. 로컬 VLM, API 기반 VLM, YOLO와 SAM 계열, YOLO segmentation과 3D 추정은
교체 가능한 adapter 후보이며 아직 최종 경로를 선택하지 않았다.

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

정확한 ROS message와 schema는 구현 시 code, package README에서 관리한다.

## 평가할 Perception 경로

```text
RGB image
  → 로컬 VLM 또는 API 기반 VLM: object, 의미, 2D region 후보
  → YOLO + SAM 계열 또는 YOLO segmentation: object, pixel mask 후보
  → Depth + calibration: base 기준 3D 위치, extent
  → Scene State validation
```

2026-08-04 Raw 실측에서는 정지 이미지 기준 ER 2→SAM2→Depth 파이프라인을
연결했다. 이는 후보 하나의 사전 실험이며, 실제 로봇 폐루프, Streaming 또는 최종 모델
선정을 의미하지 않는다.

## Adapter 원칙

- 로컬 VLM, API 기반 VLM, detector와 segmentation 경로가 같은 Scene State 의미로
  교체 가능해야 한다.
- 의미 분류, segmentation, tracking과 3D 추정 결과를 한 모델의 단일 자유 형식
  응답으로 취급하지 않는다.
- 각 단계는 입력, 출력, 품질과 실패 이유를 별도로 검증한다.
- Planner가 낸 의미 판단을 최종 좌표, grasp 가능성으로 사용하지 않는다.
- 장면이 바뀌면 오래된 mask, depth, object ID를 재사용하지 않는다.

## 작업 전후와 행동 checkpoint 관찰

작업 전 관찰은 대상과 초기 상태를, 작업 후 관찰은 실제 변화와 남은 대상을
증명한다. 두 관찰은 Dashboard 결과와 Planner 폐루프에서 같은 ID 체계로 연결되어야
한다. 각 high-level 행동의 success, failed, blocked 뒤에도 최신 Scene을 생성해 다음
Planner 판단의 checkpoint로 사용한다. VLM을 선택하면 이 checkpoint에서 재추론한다.
현재 Mission Manager 구현에는 작업 후, 행동별
재관찰 단계가 없어 추가 통합이 필요하다.

## 모델 평가 관점

최종 adapter는 고정 수치 목표가 아니라 현재 데모 입력에서 다음을 비교해 선택한다.

- 대상 누락, 오탐과 의미 분류 오류
- region, mask, 3D 좌표의 조작 적합성
- 여러 물체에서의 ID, 순서 일관성
- 처리 지연과 cloud/network 실패
- 실패를 정상 Scene State로 포장하지 않는가
- 비용, 데이터 전송과 개인정보 조건

## 관련 문서

- [Task Planning and Robot Capabilities](<03 - Task Planning and Robot Capabilities.md>)
- [Edge Runtime Jetson Orin](<06 - Edge Runtime Jetson Orin.md>)
- [Verification and Simulation Strategy](<13 - Verification and Simulation Strategy.md>)

## 출처

- [Gemini Robotics API 공식 문서](https://ai.google.dev/gemini-api/docs/robotics-overview)

## 관련 결정

- [260806 - Task Planning과 Robot Capability 경계](<../30_DECISIONS/Technical/260806 - Task Planning과 Robot Capability 경계.md>)
