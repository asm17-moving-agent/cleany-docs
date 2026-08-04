---
ingest_status: raw
ingest_targets:
  - technical
  - decision
decision_candidates:
  - "YOLOE+VLM, 로컬 VLM+Segmentation model, Gemini Robotics ER 2+Segmentation model 중 객체 인식·판단 구성 선정"
date: 2026-08-03
source_type: user-direction
source_title: "YOLOE 전환 및 파인튜닝 취소"
---

# 객체 탐지·세그멘테이션 모델 선정 자료 안내

## 1. 현재 방향

기존 일반 YOLO 후보를 YOLOE로 바꾼다. 객체 인식과 그 이후 판단 구성은 아직 다음
세 후보 중에서 선택하지 않았다. YOLOE는 첫 번째 후보의 detector이며, 두 번째와
세 번째 후보에 공통으로 적용되는 확정 모델이 아니다.

```text
1. YOLOE + VLM
2. 로컬 VLM + segmentation model
3. Gemini Robotics ER 2 + segmentation model
```

파인튜닝은 진행하지 않는다. YOLOE 후보는 공개된 사전 학습 가중치 또는 제공 API를
사용하는 전제로 검토한다. 이 변경은 Raw 단계의 사용자 방향이며 `selected` Decision은
아니다.

## 2. 문서 상태

| 문서 | 상태 | 사용 범위 |
| --- | --- | --- |
| [객체 탐지·세그멘테이션 모델 비교 조사](260720%20-%20객체%20탐지·세그멘테이션%20모델%20비교%20조사.md) | 참고 유지 | 기존 모델 비교의 역사적 근거 |
| [YOLO 방법론 정리](260722%20-%20YOLO%20방법론%20정리%20-%20탐지·세그·NMS·버전%20변천.md) | 참고 유지 | 기존 YOLO 계열 방법론 참고 |
| [클래스 정의 및 라벨링 가이드라인](260722%20-%20객체%20탐지·세그멘테이션%20클래스%20정의%20및%20라벨링%20가이드라인.md) | 취소 | 파인튜닝용 라벨링을 진행하지 않음 |
| [파인튜닝 환경 구축 계획](260723%20-%20YOLO11n-seg·YOLO26n-seg%20파인튜닝%20환경%20구축%20계획.md) | 취소 | 학습 환경을 구축하지 않음 |
| [공개 데이터셋 매핑 및 데이터 확보 방안](260723%20-%20클래스별%20공개%20데이터셋%20매핑%20및%20데이터%20확보%20방안.md) | 취소 | 학습 데이터 수집·가공을 진행하지 않음 |

취소 문서는 삭제하지 않고 `status: dropped`, `ingest_status: blocked`로 보존한다.
본문은 당시 조사·계획의 이력을 확인하는 용도로만 사용한다.

## 3. 이어서 볼 문서

- [Gemini Robotics ER 2 README](../260803%20-%20Gemini%20Robotics%20ER%202/00%20-%20README.md)

## 4. 사람 검토 필요

- 사용할 YOLOE 구현, checkpoint, task와 라이선스
- 사전 학습 가중치의 대상 객체 포괄 범위
- YOLOE 출력만으로 필요한 mask를 확보할 수 있는지
- 세 후보의 동일 장면 평가 기준과 우선 실험 순서
- 최종 선택 전에는 어느 후보도 현재 모델 선정안 또는 확정 구성으로 표기하지 않음
