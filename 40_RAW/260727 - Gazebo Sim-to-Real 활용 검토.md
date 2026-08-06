---
ingest_targets:
  - technical
decision_candidates: []
date: 2026-07-27
source_type: literature-and-official-documentation
---

# 260727 - Gazebo Sim-to-Real 활용 검토

> [!IMPORTANT]
> 2026-08-03 기준으로 perception 모델 파인튜닝은 진행하지 않는다. 이 문서의
> 파인튜닝·학습 데이터 생성 관련 제안은 취소하며, Gazebo의 인터페이스·센서·실기
> 검증 관련 내용만 참고한다.

## 1. 출처

- [Tobin et al., *Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World* (2017)](https://arxiv.org/abs/1703.06907)
- [Peng et al., *Sim-to-Real Transfer of Robotic Control with Dynamics Randomization* (2018)](https://arxiv.org/abs/1710.06537)
- [Gazebo Sensors 공식 문서](https://gazebosim.org/libs/sensors/)
- Cleany 내부 기준: `cleany_gazebo_sim` README 및
  `20_TECHNICAL/12 - Gazebo 자율주행 시뮬레이션 개발 로드맵.md`

이 문서는 위 자료와 현재 구현 상태를 바탕으로 작성한 조사 메모다. 아직 프로젝트의
선택된 기술 결정이나 학습 파이프라인 사양이 아니다.

## 2. 조사 이유

Gazebo를 자율주행·인식·조작 기능의 검증 환경으로 구축하는 과정에서, 시뮬레이션
출력을 실제 로봇 데이터 학습에 보조적으로 사용할 수 있는지 검토한다. 핵심 질문은
"합성 데이터 또는 시뮬레이터에서 학습한 정책을 실제 로봇에 어느 범위까지 전이할 수
있는가"다.

## 3. 핵심 내용

### 3.1 Sim-to-Real의 전제

Sim-to-Real은 시뮬레이션의 데이터 또는 정책을 실제 환경으로 전이하려는 접근이다.
시뮬레이션은 대량의 장면·상태·실패 사례를 안전하게 생성할 수 있지만, 렌더링,
센서, 물리, 구동계 모델이 실제와 다르면 reality gap 때문에 실제 성능이 낮아질 수
있다.

Tobin et al.은 texture, 조명, 카메라 등 시각적 조건을 넓게 변화시키는 domain
randomization으로 합성 RGB 기반 물체 위치 추정기를 실제 환경으로 전이한 사례를
제시한다. Peng et al.은 질량, 마찰, 제어 지연 등 dynamics를 무작위화해, simulation
policy가 실제 arm pushing에 적응하도록 하는 사례를 제시한다. 두 자료는 가능성을
보이지만, Cleany의 센서·기구·작업 환경에서 동일한 성능을 보장하지는 않는다.

Gazebo Sensors는 camera, laser range finder, IMU 등 센서 모델과 noise model을
제공한다. 따라서 sensor noise와 환경 조건을 명시적으로 바꾼 합성 데이터·회귀
시나리오는 만들 수 있다.

### 3.2 Cleany에 적용 가능한 범위

| 영역 | Gazebo 활용 가설 | 실제 데이터·실기 검증 필요 범위 |
|---|---|---|
| Navigation | `cmd_vel`, TF, goal 처리, obstacle·timeout 실패 흐름의 회귀 테스트 | wheel slip, LiDAR 반사·가림, 실제 통로·가구 변화, 제동 거리 |
| LiDAR·위치 추정 | 고정 월드의 `/scan`, `/imu`, map/localization 계약과 노이즈 후보 비교 | sensor extrinsic, 실제 noise·drift, localization 안정성 |
| Perception | 파인튜닝·학습 데이터 생성 활용은 취소 | 사전 학습 모델의 D435 실제 장면 추론 품질만 검증 |
| Manipulation policy | 초기 pose·trajectory·접촉 실패 시나리오 생성 후보 | servo backlash, 마찰, 힘·접촉, 물체 변형과 그리퍼 특성 |

Navigation의 Nav2는 일반적으로 지도·센서·경로 계획을 사용하는 소프트웨어
구성이므로, 현재 단계에서는 학습 데이터 생성보다 Sim/Real 공통 계약과 반복
시나리오 검증에 우선 활용하는 편이 적절하다.

### 3.3 권장 실험 순서

1. Gazebo에서 LiDAR·IMU·실내 월드와 `map -> odom -> base_link` 계약을 구성한다.
2. 실제 D435·LiDAR로 소량의 기준 장면과 센서 로그를 수집한다.
3. 카메라 기반 인식은 선택한 사전 학습 모델을 실제 D435 장면에서 검증한다.
4. 합성 데이터 생성과 실제 데이터 fine-tuning 비교는 취소한다.
5. arm·gripper policy의 직접 전이는 실제 기구학, 구동계, 접촉 특성 측정 이후의
   후속 실험으로 둔다.

## 4. 프로젝트 관련성

현재 `cleany_gazebo_sim`은 메카넘 `cmd_vel`, `/odom`, `odom -> base_link` TF와
camera bridge를 제공한다. LiDAR·IMU·Nav2·SLAM/localization은 아직 포함하지
않는다. 따라서 현 상태의 Gazebo는 synthetic perception dataset 또는 학습 정책의
즉시 생성 환경으로 보기보다, 주행 인터페이스와 실패 처리를 검증하는 기반으로
해석하는 것이 타당하다.

또한 WSL 환경에서 Gazebo camera sensor renderer와 GUI를 함께 사용할 때 안정성
문제가 관찰됐다. 합성 image data 생성 실험은 렌더링과 sensor topic이 안정적으로
동작하는 GPU 환경에서 별도 확인해야 한다.

## 5. 결정 후보

현재 결정 후보 없음.

향후 아래 항목이 확인되면 Technical Decision 후보가 될 수 있다.

- ~~perception 학습에서 합성 데이터와 실제 데이터의 사용 비율·fine-tuning 방식~~
  (2026-08-03 취소)
- Sim-to-Real 대상 범위가 인식 보조인지, base control 또는 manipulation policy까지인지
- domain randomization에 포함할 camera, sensor, 물리 parameter와 평가 기준

## 6. 리스크 / 주의점

- 합성 데이터의 label은 자동 생성되지만, 실제 조명·재질·가림·센서 결측을 충분히
  표현하지 못하면 실제 일반화가 낮을 수 있다.
- dynamics randomization은 실제 parameter 범위를 모르면 임의의 무작위화가 될 수
  있으므로, 실제 측정과 calibration이 필요하다.
- 실제 데이터가 없는 상태에서 simulator 성공률만으로 실기 성능이나 안전성을
  주장할 수 없다.
- Gazebo 렌더러의 host 호환성 문제는 image dataset 생성 자체를 왜곡하거나 막을 수
  있다.
- 개인정보가 포함될 수 있는 실제 카메라 데이터는 수집·보관·라벨링 정책을 별도로
  검토해야 한다.

## 7. 후속 작업

- LiDAR·IMU를 포함한 Gazebo 주행 센서 contract와 headless 검증 시나리오 정의
- 실제 D435·LiDAR 기준 로그의 수집 항목, 보관 위치, calibration 절차 정의
- 사전 학습 인식 모델의 실제 D435 장면 검증 조건 정의
- 실제 검증 세트의 성공 지표와 안전 중단 기준 정의
## 3. 핵심 내용

## 4. 프로젝트 관련성

## 5. 결정 후보

## 6. 리스크 / 주의점

## 7. 후속 작업
