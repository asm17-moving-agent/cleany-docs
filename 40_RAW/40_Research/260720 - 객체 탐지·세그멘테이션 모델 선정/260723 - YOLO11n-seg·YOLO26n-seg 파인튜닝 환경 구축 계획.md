---
type: raw-research
reviewers:
  -
ingest_status: raw
ingest_targets:
  - technical
decision_candidates:
  - 객체 탐지·세그멘테이션 최종 모델 선정
  - YOLO 파인튜닝 학습 환경(브랜치·프로젝트 구조) 구성 방식
date: 2026-07-23
source_type: implementation-plan
source_url:
related_jira:
  -
tags:
  - raw
  - research
  - ingest-source
  - perception
  - segmentation
  - yolo
  - training
  - finetuning
  - infrastructure
  - dataset
  - labeling
---

# 260723 - YOLO11n-seg·YOLO26n-seg 파인튜닝 환경 구축 계획

## 1. 목표 및 결론

이 문서는 끌리니 객체 탐지·인스턴스 세그멘테이션 모델을 파인튜닝하기 위한 코드와 실행 환경의 구현 계획을 정리한다. 데이터셋 수집·다운로드·라벨링은 이번 범위에 포함하지 않고, 외부에서 준비된 Ultralytics segmentation 데이터셋을 검증하고 학습에 전달하는 경계까지만 다룬다.

기존 모델 비교 조사에서는 `YOLO11n-seg`를 우선 선정안으로 두었다. 이후 YOLO26의 NMS-free 구조와 공개 성능을 추가로 검토했지만, 이것만으로 기존 우선안을 변경하거나 최종 모델을 확정하지 않는다. 대신 동일한 학습 코드와 데이터 계약에서 다음 두 모델을 교체해 실행할 수 있는 공통 환경을 만든다.

- `YOLO11n-seg`: 기존 우선 선정안의 기준선
- `YOLO26n-seg`: 같은 조건에서 비교할 신규 실험 후보

학습 파이프라인은 모델 이름을 코드에 고정하지 않고 model profile로 분리한다. 공통 조건 비교와 모델별 최적화 실험도 분리해, 서로 다른 학습 recipe가 비교 결과에 섞이지 않도록 한다.

## 2. 배경과 관련 문서

이 계획은 다음 기존 조사 자료를 바탕으로 한다.

- [[260720 - 객체 탐지·세그멘테이션 모델 비교 조사|객체 탐지·세그멘테이션 모델 비교 조사]]: `YOLO11n-seg` 우선안과 엣지 추론 후보 비교
- [[260722 - YOLO 방법론 정리 - 탐지·세그·NMS·버전 변천|YOLO 방법론 정리]]: YOLO11과 YOLO26의 구조 및 NMS 차이
- [[260722 - 객체 탐지·세그멘테이션 클래스 정의 및 라벨링 가이드라인|클래스 정의 및 라벨링 가이드라인]]: segmentation annotation과 클래스 경계 초안
- [[260723 - 클래스별 공개 데이터셋 매핑 및 데이터 확보 방안|공개 데이터셋 매핑 및 데이터 확보 방안]]: 외부 데이터 후보와 확보 절차
- [[20_TECHNICAL/07 - Data and Evaluation|Data and Evaluation]]: 데이터·평가 후보와 미확정 평가 기준

기존 계획을 다시 검토하면서 다음 보완점이 확인됐다.

| 기존 계획의 한계 | 보완 방향 |
|---|---|
| 브랜치와 코드가 `YOLO26n-seg`에 종속됨 | 모델 중립적인 `yolo-seg` 학습 환경으로 변경 |
| 가중치 파일명이 학습 코드에 고정됨 | 모델별 profile과 checksum으로 분리 |
| YOLO11과 YOLO26 비교 조건이 정의되지 않음 | 공통 조건 비교와 모델별 최적화 run을 구분 |
| Mac MPS와 CUDA 결과의 역할이 불명확함 | MPS는 기능 smoke, RTX 3080 CUDA는 기준선 학습으로 분리 |
| dataset·weights·checkpoint가 저장소에 유입될 수 있음 | 모든 대용량 산출물을 외부 경로에 저장 |
| dry-run 의미가 불명확함 | 학습·다운로드·파일 쓰기 없는 설정 해석으로 정의 |
| 서로 다른 모델 checkpoint의 resume 위험 | model family와 입력 artifact identity가 다르면 거부 |

## 3. 범위와 제외 범위

### 3.1 포함 범위

- 학습 전용 Git 브랜치와 변경 단위
- ROS workspace와 분리된 Python 학습 프로젝트
- YOLO11n-seg·YOLO26n-seg model profile
- dataset·weights·device·output 사전검사
- 신규 학습, 중단 재개와 validation CLI
- MacBook M5 Pro의 네이티브 `uv`·MPS 개발 환경
- RTX 3080 GPU 클러스터의 단일 GPU 학습 환경
- Slurm+Apptainer 실행 템플릿과 직접 `uv` 실행 fallback
- 실행 설정, 환경, 가중치와 산출물 provenance 기록
- 단위검사, dry-run과 환경별 smoke 절차
- 상황 특화 데이터 직접 촬영·라벨링 작업의 소요기간·인원 배분 계획 수립(12장, 실행은 제외)

### 3.2 제외 범위

- 프로젝트 데이터셋의 실제 촬영·수집·다운로드와 라벨링 실행(계획 수립은 3.1·12장 참고)
- 클래스 목록, train/validation/test split과 정량 목표 확정
- ROS 2 perception node와 MuJoCo 연결
- Jetson Orin 배포와 성능 측정
- ONNX·TensorRT export와 양자화
- 모델 registry, 원격 artifact store, W&B와 MLflow
- RTX 3080 4장·8장을 사용하는 DDP 분산학습
- 모델의 최종 제품 채택과 기존 KB Decision 상태 변경

## 4. 브랜치와 구현 경계

### 4.1 브랜치 전략

학습 환경은 Cleany 구현 저장소의 최신 `main`에서 새 브랜치를 만든다.

```bash
git switch main
git pull --ff-only origin main
git switch -c feat/yolo-seg-training-env
```

기존 `test/yolo-mujoco-detection` 브랜치는 ROS inference와 MuJoCo scene 변경이 함께 들어 있어 학습 환경의 기반 브랜치로 사용하지 않는다. 이번 브랜치에는 학습 code·config·container·cluster launcher만 두고, 학습된 checkpoint를 ROS inference에 연결하는 작업은 후속 브랜치로 분리한다.

### 4.2 구현 위치

학습 환경은 구현 저장소 최상위 `training/`에 독립 Python project로 둔다. `ros2_ws/`의 ROS package dependency와 학습용 PyTorch·Ultralytics dependency를 섞지 않는다.

```text
training/
├── pyproject.toml
├── uv.lock
├── README.md
├── configs/
│   ├── comparison.yaml
│   ├── mps-smoke.yaml
│   └── profiles/
│       ├── yolo11n-seg.yaml
│       └── yolo26n-seg.yaml
├── containers/
│   └── Containerfile.cuda
├── cluster/
│   ├── cluster.example.yaml
│   └── slurm/
├── src/
│   └── cleany_yolo_training/
└── tests/
```

예상 변경은 `training/`과 root `.gitignore`, 필요한 최소한의 root README 안내로 제한한다. ROS package, KB submodule과 기존 simulation 파일은 수정하지 않는다.

### 4.3 커밋 단위

|  순서 | 커밋 목적               | 포함 내용                                               |
| --: | ------------------- | --------------------------------------------------- |
|   1 | 학습 project scaffold | Python 3.12, `pyproject.toml`, `uv.lock`, 품질 도구     |
|   2 | 공통 학습 CLI           | config, preflight, dry-run, train, resume, validate |
|   3 | model profile       | YOLO11n-seg·YOLO26n-seg profile와 weights checksum   |
|   4 | 실행 인프라              | Mac MPS, CUDA container, Slurm·Apptainer            |
|   5 | 검증과 문서              | 단위검사, smoke 절차, artifact·재현성 문서                     |

## 5. 학습 코드와 공개 인터페이스

### 5.1 공통 CLI

CLI 이름은 특정 YOLO 버전을 포함하지 않는 `cleany-yolo`로 둔다.

| 명령             | 책임                                  | 주요 입력                                  |
| -------------- | ----------------------------------- | -------------------------------------- |
| `preflight`    | dataset, weights, output과 device 검사 | profile, data, weights, output, device |
| `dry-run`      | 설정 해석과 실행 계획 출력                     | train과 같은 입력                           |
| `train`        | 신규 파인튜닝 실행                          | profile, common config, run name       |
| `resume`       | 명시적 `last.pt`에서 재개                  | checkpoint, 기존 manifest                |
| `validate`     | 명시적 checkpoint 평가                   | checkpoint, data, device               |
| `render-slurm` | Slurm 제출 명령 생성                      | cluster config, train arguments        |

예상 사용 방식은 다음과 같다.

```bash
cleany-yolo train \
  --profile yolo11n-seg \
  --config configs/comparison.yaml \
  --data /datasets/cleany/data.yaml \
  --weights /weights/yolo11n-seg.pt \
  --output /artifacts/cleany-yolo \
  --run-name comparison-yolo11n-seg \
  --device 0
```

```bash
cleany-yolo train \
  --profile yolo26n-seg \
  --config configs/comparison.yaml \
  --data /datasets/cleany/data.yaml \
  --weights /weights/yolo26n-seg.pt \
  --output /artifacts/cleany-yolo \
  --run-name comparison-yolo26n-seg \
  --device 0
```

`dry-run`은 config와 경로를 해석해 redacted command와 manifest preview를 표준 출력으로 보여 주고 종료한다. 다음 작업은 수행하지 않는다.

- weights·dataset 다운로드
- Ultralytics trainer 생성
- CUDA·MPS device 초기화
- run directory와 manifest 생성
- checkpoint와 metrics 쓰기

### 5.2 경계와 오류 처리

- 학습 명령은 `mps` 또는 명시적인 CUDA device만 허용한다.
- 요청한 accelerator가 없으면 CPU로 fallback하지 않고 non-zero로 실패한다.
- 기존 run name의 directory가 있으면 덮어쓰지 않는다.
- `resume`은 명시적인 `last.pt`만 받는다.
- YOLO11 checkpoint에서 YOLO26을 resume하거나 반대 방향으로 재개하지 않는다.
- data, profile, common config 또는 weights identity가 기존 manifest와 다르면 resume을 거부한다.
- `validate`는 `best.pt` 또는 `last.pt`와 평가할 dataset YAML을 명시적으로 받는다.

## 6. Model profile과 비교 규칙

### 6.1 Model profile

model profile은 모델별로 달라야 하는 값만 가진다.

| profile       | 사전학습 가중치         | 역할                |
| ------------- | ---------------- | ----------------- |
| `yolo11n-seg` | `yolo11n-seg.pt` | 기존 우선안 기준선        |
| `yolo26n-seg` | `yolo26n-seg.pt` | 신규 NMS-free 후보 비교 |

각 profile은 다음 정보를 포함한다.

- 고유 model family와 profile schema version
- 공식 weights filename과 source
- 기대 SHA-256
- Ultralytics task `segment`
- 허용되는 model-specific override
- checkpoint와 output namespace

weights는 학습 명령에서 자동으로 내려받지 않는다. 별도의 명시적 fetch 절차로 공식 asset을 외부 weights directory에 준비하고, 학습 전 committed checksum과 일치하는지 확인한다.

### 6.2 공통 조건 비교

두 architecture를 비교하는 run은 다음 조건을 동일하게 유지한다.

- dataset version과 train/validation split
- image size
- epoch 수와 batch size
- seed와 deterministic mode
- augmentation과 early-stopping 설정
- validation dataset과 metrics 추출 방식
- Ultralytics package version
- RTX 3080 단일 GPU

첫 비교 config의 계획값은 다음과 같다.

| 항목 | 값 | 비고 |
|---|---:|---|
| `epochs` | 100 | dataset 규모에 따른 변경은 별도 기록 |
| `imgsz` | 640 | 공개 사전학습·평가 기본 크기 |
| `batch` | 8 | RTX 3080에서 preflight 후 확인 |
| `workers` | 8 | cluster CPU allocation과 함께 기록 |
| `seed` | 0 | 모든 비교 run 동일 |
| `deterministic` | true | 성능 저하 가능성도 manifest에 기록 |
| `amp` | true | CUDA mixed precision |
| `cache` | false | cluster memory·filesystem 차이 최소화 |
| `save_period` | 10 | preemption과 장시간 run 대응 |
| `exist_ok` | false | 결과 덮어쓰기 방지 |

공통 조건 비교에서는 model family 외에 설정을 임의로 변경하지 않는다. 어떤 공통 optimizer가 두 model에 공정한지는 별도 검토가 필요하므로, 실제 비교 전에 config와 Ultralytics version을 함께 확정하고 manifest에 기록한다.

### 6.3 모델별 최적화

공통 조건 비교와 별도로 model-specific recipe를 적용한 최적화 run을 허용한다. YOLO26의 MuSGD·Progressive Loss·STAL 등 architecture-specific recipe와 YOLO11의 권장 recipe를 이용할 경우 다음 원칙을 적용한다.

- run type을 `comparison`이 아니라 `optimized`로 기록한다.
- 변경한 optimizer·scheduler·augmentation을 profile override에 명시한다.
- 공통 조건 비교 결과와 같은 표에서 직접 우열을 확정하지 않는다.
- 동일 model의 baseline 대비 개선 여부를 먼저 평가한다.

## 7. Dataset 입력 계약

### 7.1 입력 형식

이번 작업은 dataset을 확보하지 않고 외부에서 전달된 Ultralytics instance segmentation `data.yaml`을 입력으로 받는다. 최소 계약은 다음과 같다.

- `path`, `train`, `val`, `names` 존재
- relative path는 `data.yaml`의 `path` 기준으로 해석
- train과 validation split이 비어 있지 않음
- image와 label이 대응함
- label의 class ID가 `names` 범위 안에 있음
- segmentation polygon이 class ID 뒤에 정규화한 x·y 쌍을 최소 3점 포함
- 좌표가 0~1 범위에 있음
- train·validation 사이에 같은 image가 중복되지 않음

다음 항목은 명확히 범위 밖이다.

- 어떤 공개 dataset을 실제로 내려받을지 결정
- 끌리니 클래스 목록 확정
- annotation 도구와 작업자 선정
- data split 비율과 모델 품질 목표값 확정
- 실제 촬영 데이터의 개인정보·보안 처리

### 7.2 사전검사 실패

다음 사례는 distinct diagnostic과 non-zero exit code로 거부한다.

- train 또는 validation split 누락
- image만 있고 label이 없는 orphan sample
- label만 있고 image가 없는 orphan annotation
- 범위를 벗어난 class ID
- 홀수 개 좌표, 3점 미만 또는 범위 밖 polygon
- 손상되거나 읽을 수 없는 image·label
- train·validation 중복
- 저장소 내부로 지정된 output 경로

## 8. 실행 인프라

### 8.1 MacBook M5 Pro

현재 개발 노트북은 Apple Silicon arm64, 메모리 48GB 환경이다. Docker 안에서는 Apple MPS를 사용할 수 없으므로 Mac은 native `uv`와 PyTorch MPS를 사용한다.

```bash
uv python install 3.12
cd training
uv sync --frozen
uv run cleany-yolo preflight --device mps ...
uv run cleany-yolo dry-run ...
```

Mac의 역할은 다음으로 제한한다.

- config·dataset contract 단위검사
- CLI dry-run
- MPS availability와 실제 device 확인
- 임시 synthetic segmentation fixture를 이용한 1-epoch smoke

MPS smoke는 기능 검증용이며 모델 정확도 비교 자료로 사용하지 않는다. 계획값은 `epochs: 1`, `imgsz: 320`, `batch: 2`, `workers: 0`이다. 실행 manifest에 실제 device가 `mps`로 기록돼야 하며 CPU fallback은 실패로 처리한다.

synthetic fixture는 test 실행 중 임시 directory에 생성하고 저장소에 dataset asset으로 커밋하지 않는다.

### 8.2 RTX 3080 GPU 클러스터

정식 baseline 학습은 대학 GPU 클러스터의 RTX 3080 한 장에서 시작한다. 클러스터가 4장 또는 8장을 제공하더라도 첫 단계에서 DDP를 사용하지 않는다.

CUDA 환경은 versioned container와 lockfile로 재현한다.

- Python 3.12
- `ultralytics==8.4.104` 기준 lock
- 고정 PyTorch·torchvision·CUDA dependency
- immutable OCI image digest
- NVIDIA driver와 container CUDA 호환성 preflight

클러스터 정책이 아직 확인되지 않았으므로 두 실행 경로를 준비한다.

1. Slurm+Apptainer: `--nv`와 명시적 bind mount 사용
2. 직접 `uv`: cluster module·CUDA 환경 위에서 `uv sync --frozen`

cluster config는 다음 값을 코드 밖에서 받는다.

- partition
- account와 QoS
- walltime
- CPU·memory
- GPU GRES
- module command
- Apptainer executable과 image path
- dataset·weights read-only bind
- artifact·cache·scratch read-write bind

미해결 placeholder가 있으면 job 제출 전 실패한다. `sbatch`가 job ID를 반환한 사실만으로 학습 성공을 판단하지 않고, 종료 코드·terminal manifest·checkpoint와 metrics를 확인한다.

## 9. Artifact와 재현성

### 9.1 저장 위치

dataset, weights와 모든 run output은 Git 저장소 밖에 둔다.

```text
external-artifact-root/
└── <run-name>/
    ├── run-manifest.json
    ├── resolved-config.yaml
    ├── weights/
    │   ├── best.pt
    │   └── last.pt
    ├── metrics/
    │   └── validation.json
    └── ultralytics/
```

root `.gitignore`에는 dataset, weights, `runs/`, checkpoint, Slurm output, cache와 Apptainer SIF에 대한 방어적 ignore rule을 추가한다. 정상 실행 뒤 구현 저장소의 `git status --short`가 실행 전과 같아야 한다.

### 9.2 Run manifest

manifest는 run 시작 전에 `running`, 종료 시 `succeeded`, `failed` 또는 `interrupted` 상태로 원자적으로 갱신한다.

필수 기록 항목은 다음과 같다.

- run ID, run type, 시작·종료 시각과 상태
- 구현 저장소 Git commit과 dirty 여부
- Python, Ultralytics, PyTorch version
- OS, architecture, CUDA·cuDNN 또는 MPS 정보
- GPU 이름, visible device와 memory
- model family, profile hash와 input weights hash
- common config hash와 resolved arguments
- dataset YAML hash와 split fingerprint
- seed와 deterministic 설정
- input checkpoint와 output artifact path·hash
- validation mask·box metrics path

manifest에는 access token, cluster credential과 dataset의 개인정보를 기록하지 않는다.

### 9.3 중단과 재개

- 주기적으로 `last.pt`를 저장한다.
- Slurm preemption 또는 SIGTERM은 `interrupted` 상태로 기록한다.
- disk full, CUDA OOM과 dependency 오류는 성공으로 변환하지 않는다.
- 재제출 시 기존 `last.pt`와 manifest를 명시한다.
- data, profile, config와 weights identity drift가 있으면 새 run으로 시작한다.

## 10. 평가와 완료 기준

### 10.1 학습 완료와 품질 승인 분리

dataset과 정량 성공 기준이 확정되지 않았으므로 이번 환경 구축에는 mAP 합격선을 두지 않는다.

| 상태 | 의미 |
|---|---|
| 환경 검증 완료 | dependency, CLI, preflight, dry-run과 device smoke 통과 |
| 학습 완료 | 지정 epoch 종료, checkpoint·metrics·terminal manifest 생성 |
| 비교 가능 | 같은 comparison config와 dataset fingerprint로 두 model run 완료 |
| 품질 승인 | 별도 Technical 기준에 따른 사람 검토 필요 |

validation 결과는 최소 다음 값을 machine-readable JSON으로 남긴다.

- mask mAP50-95, mAP50과 mAP75
- mask precision과 recall
- box mAP50-95, mAP50과 mAP75
- class별 mask·box 지표
- 평가 dataset fingerprint와 checkpoint hash

### 10.2 공정 비교 결과

YOLO11n-seg와 YOLO26n-seg 비교 시 결과 표에는 다음을 함께 기록한다.

- 정확한 weights와 package version
- 공통 config hash
- dataset split fingerprint
- 학습 시간과 최대 GPU memory
- best epoch와 early-stopping 여부
- mask·box metrics
- inference benchmark와 배포 결과는 학습 결과와 분리

공개 COCO 수치는 실험의 참고값이며 끌리니 dataset의 성능을 대신하지 않는다.

## 11. 테스트와 검증 계획

### 11.1 자동검사

- 올바른 config와 synthetic segmentation fixture 통과
- split 누락, orphan label, malformed polygon과 class ID 범위 오류 거부
- train·validation 중복 거부
- dry-run에서 trainer·download·device 초기화·파일 쓰기가 호출되지 않음
- MPS·CUDA가 없을 때 CPU fallback 없이 실패
- 기존 run 덮어쓰기 거부
- 다른 model family checkpoint resume 거부
- config·data·weights drift resume 거부
- manifest 상태 전이와 secret 제외
- Slurm 필수값 누락 거부
- 생성된 shell의 `bash -n` 통과

예상 검증 명령은 다음과 같다.

```bash
cd training
uv sync --frozen
uv run ruff check .
uv run basedpyright
uv run pytest
uv run cleany-yolo dry-run ...
```

### 11.2 실제 사용 검증

Mac에서는 synthetic fixture로 MPS 1-epoch smoke를 실행해 checkpoint, metrics와 `device=mps` manifest를 확인한다.

클러스터에서는 프로젝트 dataset을 받기 전에 다음 preflight만 수행한다.

- Python과 package version
- `torch.cuda.is_available()`
- visible RTX 3080 한 장
- container `--nv` 또는 직접 `uv` CUDA 연결
- dataset read-only와 output read-write mount
- scratch·cache·output의 disk 여유

실제 dataset이 제공된 뒤 YOLO11n-seg와 YOLO26n-seg comparison run을 같은 조건으로 실행한다. 클러스터 접근과 dataset이 없는 상태에서는 Slurm template을 `정적 검증 완료`로만 표시하고 실제 학습 완료로 보고하지 않는다.

## 12. 상황 특화 데이터 직접 촬영·라벨링 작업 계획

### 12.1 배경과 이 절의 위치

[[260723 - 클래스별 공개 데이터셋 매핑 및 데이터 확보 방안|공개 데이터셋 매핑 및 데이터 확보 방안]]에 따르면 23개 클래스 중 `carrier`(캐리어)·`earphone_case`(이어폰 케이스)·`power_bank`(보조배터리) 3종은 공개 세그멘테이션 데이터가 사실상 없고, `receipt`·`cable`·`key` 3종은 소량만 존재한다. 여기에 `cup`·`mask`·`tissue`·`wrapper`·`slippers`·`glasses` 등은 공개 데이터가 있어도 무인 스터디카페 실물과 도메인 갭이 커 재촬영·재라벨링이 필요하다고 명시돼 있다. 이 절은 이 도메인 특화 촬영·라벨링 작업의 소요기간과 진행 순서를 가늠하기 위한 계획이다.

3.2에서 이 문서의 제외 범위로 "프로젝트 데이터셋의 실제 촬영·수집·다운로드와 라벨링 실행"을 명시했다. 이 절은 그 실행 자체가 아니라, 7장의 dataset 입력 계약(`data.yaml`)을 채우기 위해 별도로 필요한 후속 작업의 기간과 인원 배분을 미리 가늠해 두는 계획 메모이며 3.1의 포함 범위에 해당한다. 실제 촬영·라벨링은 이번 `feat/yolo-seg-training-env` 브랜치와 무관하게 별도로 진행한다.

라벨링 도구는 [[260722 - 객체 탐지·세그멘테이션 클래스 정의 및 라벨링 가이드라인|클래스 정의 및 라벨링 가이드라인]]에 "미정, CVAT·Label Studio·Roboflow 중 팀이 선택"으로 남아 있다. 이 계획에서는 자체 호스팅 CVAT(Docker Compose로 로컬 또는 사내망에 구동)을 잠정 권장 도구로 가정해 아래 기간을 추정한다.

- Polygon·hole annotation과 difficult(보류) 플래그를 기본 지원해 6장 라벨링 기준과 맞는다.
- Ultralytics YOLO segmentation export를 직접 지원해 7장 dataset 계약과 변환 없이 연결된다.
- 자체 호스팅이 가능해 `card`·`receipt`·`wallet` 등 개인정보 포함 가능 이미지를 외부 SaaS에 업로드하지 않아도 된다.
- 다른 도구로 최종 결정되면 12.3·12.4의 기간·역할 추정은 재검토가 필요하다.

### 12.2 전제와 가정

아래 기간·인원 추정은 실측이 아닌 목측 가정이며, 실제 촬영을 시작한 뒤 재산정이 필요하다.

| 가정 항목           |          값 | 근거·비고                                                                                                                                                                                                         |
| --------------- | ---------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 목표 이미지 수        |     약 500장 | 갭 3종(`carrier`·`earphone_case`·`power_bank`)과 도메인 보강 대상(`cup`·`mask`·`tissue`·`wrapper`·`slippers`·`glasses` 등)을 모두 커버하기 위한 1차 목표. 클래스별 최소 인스턴스 수는 미확정([[260723 - 클래스별 공개 데이터셋 매핑 및 데이터 확보 방안#6. 미해결 질문]] 참고) |
| 이미지당 평균 인스턴스 수  |       약 5개 | 책상 위 여러 물체가 동시에 놓이는 장면 특성 반영                                                                                                                                                                                  |
| 인스턴스당 평균 라벨링 시간 |     약 1.5분 | Polygon 작성(6.3 기준) 기준, `cable`·`carrier`처럼 가늘거나 겹친 형태는 더 오래 걸릴 수 있음                                                                                                                                           |
| 작업일 기준          |   1일 = 8시간 | 다른 업무와 병행하면 실제 캘린더 기간은 늘어남                                                                                                                                                                                    |



### 12.3 혼자 진행할 때 작업 순서와 소요기간

|  순서 | 작업                 | 내용                                                                                               |    예상 소요 |
| --: | ------------------ | ------------------------------------------------------------------------------------------------ | -------: |
|   1 | 촬영 계획 수립           | 클래스별 배치 조합, 가림·잘림·조명 변화를 포함한 촬영 시나리오, negative image 비율, 체크리스트 작성                                |     0.5일 |
|   2 | 촬영 실행              | 여러 세션에 걸쳐 스터디카페 책상 환경을 재현해 촬영(약 500장)                                                            |       2일 |
|   3 | 선별·전처리             | 초점 나감·중복 이미지 제거, 파일명·폴더 구조 정리, 개인정보 포함 이미지 격리 또는 비식별 처리                                          |       1일 |
|   4 | 라벨링 도구 셋업          | CVAT 자체 호스팅 설치(Docker Compose), 프로젝트 생성, 23개 클래스 등록, YOLO segmentation export 포맷 확인              |     0.5일 |
|   5 | Calibration 표본 라벨링 | 20~30장 시범 라벨링으로 [[260722 - 객체 탐지·세그멘테이션 클래스 정의 및 라벨링 가이드라인#6.4 모호한 경계 처리 절차6.4 모호한 경계 처리 절차]] 점검 |     0.5일 |
|   6 | 1차 라벨링             | 전체 이미지 Polygon 라벨링(500장 × 평균 5인스턴스)                                                              |     7~8일 |
|   7 | 검수                 | 8장 품질 기준에 따른 표본 또는 전수 검수                                                                         |       2일 |
|   8 | 수정·재검수             | 오류 수정, 보류(difficult) 사례 해소                                                                       |       1일 |
|     | **합계**             |                                                                                                  | **약 2주** |

### 12.4 여러 명이 나눠서 진행할 때 분담

인원 추가의 이득은 주로 물량이 가장 큰 1차 라벨링(6번)과 검수(7번)를 병렬화하는 데서 나온다.

| 담당               | 역할                              | 담당 작업(12.3 기준 순서) |     예상 소요 |
| ---------------- | ------------------------------- | ----------------- | --------: |
| A (촬영·데이터 준비)    | 촬영 계획, 촬영 실행, 선별·전처리 전담         | 1, 2, 3           |      3.5일 |
| B (라벨링 파이프라인·품질) | 도구 셋업, calibration 준비, 검수 총괄    | 4, 5(공동)          |      1.5일 |
| A + B 공동         | 1차 라벨링을 절반씩 나눠 병렬 진행, 서로 상대방 결과 교차검수 | 6, 7, 8           | 각자 약 4~5일 |

## 13. 단계별 후속 작업

1. 구현 저장소 `main`에서 `feat/yolo-seg-training-env` 생성
2. Python 3.12·`uv` 기반 독립 `training/` scaffold와 lockfile 생성
3. typed config, profile, dataset preflight와 dry-run 구현
4. train·resume·validate와 run manifest 구현
5. YOLO11n-seg·YOLO26n-seg weights checksum 등록
6. Mac MPS synthetic smoke 통과
7. CUDA container와 Slurm+Apptainer template 정적 검증
8. 대학 cluster 정책 확인 후 RTX 3080 단일 GPU preflight
9. 외부 dataset 준비(12장 직접 촬영·라벨링 포함) 후 동일 조건 comparison run 실행
10. 결과를 Data and Evaluation 및 모델 선정 Decision 후보에 연결
11. 선정 모델만 ROS inference·Jetson 배포 후속 작업으로 전달

## 14. 참고자료

### 14.1 공식 문서

- [Ultralytics YOLO11](https://docs.ultralytics.com/models/yolo11/)
- [Ultralytics YOLO26](https://docs.ultralytics.com/models/yolo26/)
- [Ultralytics Instance Segmentation](https://docs.ultralytics.com/tasks/segment/)
- [Ultralytics Train Mode](https://docs.ultralytics.com/modes/train/)
- [Ultralytics Segmentation Dataset Format](https://docs.ultralytics.com/datasets/segment/)
- [Ultralytics Docker Quickstart](https://docs.ultralytics.com/guides/docker-quickstart/)
- [Ultralytics 8.4.104 PyPI Release](https://pypi.org/project/ultralytics/8.4.104/)
- [PyTorch MPS Backend](https://docs.pytorch.org/docs/stable/notes/mps.html)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

### 14.2 내부 문서

- [[260720 - 객체 탐지·세그멘테이션 모델 비교 조사]]
- [[260722 - YOLO 방법론 정리 - 탐지·세그·NMS·버전 변천]]
- [[260722 - 객체 탐지·세그멘테이션 클래스 정의 및 라벨링 가이드라인]]
- [[260723 - 클래스별 공개 데이터셋 매핑 및 데이터 확보 방안]]
- [[20_TECHNICAL/07 - Data and Evaluation]]
- [[20_TECHNICAL/99 - Questions]]
