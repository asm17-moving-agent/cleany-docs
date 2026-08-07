---
ingest_targets:
  - technical
decision_candidates:
  - "객체 인식·판단 아키텍처 선택"
date: 2026-08-04
source_type: user-direction
source_title: "Gemini Robotics-ER 2 클라우드 API 실측"
related_docs:
  - "../260803 - Gemini Robotics ER 2/01 - ER 2 역할·기능·한계.md"
  - "../260803 - Gemini Robotics ER 2/02 - 클라우드 API·비용·운영 조건.md"
---

# 260804 - Gemini Robotics ER 2 실측

## 1. 검증 범위

`google-genai` SDK로 Gemini Robotics-ER 2 Preview를 호출해 사무실 책상 사진 2장(사람·노트북·모니터·마우스·컵·의자 등이 있는 장면)에서 2D bounding box를 뽑고, 그 결과를 SAM2 세그멘테이션·3D 좌표 계산까지 실제로 연결해 봤다.
정확도 수치·가격·쿼터의 정식 벤치마크가 아니라, 파이프라인이 실제로 돌아가는지와 출력 형식이 안정적인지 확인하는 데 목적을 뒀다.

## 2. 사용 조건

- SDK: `google-genai` (Python), `client.models.generate_content`.
- 인증: `GEMINI_API_KEY` 환경변수.
- `temperature=0.0`로 고정해 호출했다.
- 실행 환경: 시스템 Python 3.9(별도 venv 아님) — 이 스크립트는 torch가 필요 없는 유일한 단계라서 로컬 인식 파이프라인의 나머지(SAM2, 3D 계산)와 다른 인터프리터를 쓴다.

## 3. 응답 속도

이미지 입력부터 추론 결과 수신까지 **6.8~7.2초**로 실측됐다(API 왕복 포함, 여러 차례 호출한 범위).
정식 지연시간 벤치마크는 아니며, 네트워크 상태·이미지 크기·물체 수에 따라 달라질 수 있다.
[[02 - 로컬 VLM(Qwen3-VL) 실측.md|2번 문서]]의 로컬 Qwen3-VL-2B(모델 로드 평균 6.7초 + 추론 14초, 총 20초 이상)과 비교하면 ER 2 쪽이 전체 소요 시간이 짧다.
다만, ER 2는 매 호출마다 이 지연이 반복되는 반면 로컬 VLM은 모델 로드가 프로세스당 1회뿐이라는 차이가 있다.

## 4. 출력 스키마

```json
{
  "detections": [
    {"label": "laptop", "box_2d": [341, 78, 748, 356]}
  ]
}
```

- `box_2d`는 `[y_min, x_min, y_max, x_max]` 순서이며, **원본 이미지 기준** 0-1000 정규화 좌표다.

`box_2d`를 픽셀 좌표로 되돌리는 변환은 두 백엔드가 공유하는 좌표 코드다(`detection_common.py`).
경계를 벗어난 값과 뒤집힌 좌표를 여기서 한 번에 정리해서, SAM2 프롬프트로 넘어가기 전에 항상 유효한 박스가 되게 한다.

```python
def denormalize_box(box_2d, width, height):
    """0-1000 정규화 좌표 [y_min, x_min, y_max, x_max]를 픽셀 xyxy로 변환.

    이미지 경계를 벗어난 좌표는 잘라낸다. SAM2에 박스 프롬프트로 넘길 때
    범위를 벗어난 값이 들어가면 마스크가 엉뚱하게 잡히기 때문이다.
    """
    y_min, x_min, y_max, x_max = box_2d
    x1 = max(0.0, min(x_min / 1000 * width, width))
    y1 = max(0.0, min(y_min / 1000 * height, height))
    x2 = max(0.0, min(x_max / 1000 * width, width))
    y2 = max(0.0, min(y_max / 1000 * height, height))
    # 모델이 좌표를 뒤집어 내놓는 경우가 있어 정렬해 둔다.
    return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
```

## 5. 실측 정확도 관찰

정량 벤치마크는 아니지만, 같은 사진을 SAM2에 넘겼을 때의 `fill_ratio` (마스크 픽셀 수 / 박스 픽셀 수)로 박스 품질을 간접 확인했다.

| 물체 | fill_ratio | 해석 |
| --- | --- | --- |
| card(사각형) | 88.2% | 박스가 실제 형상에 밀착 |
| sticky note(사각형) | 82.4% | 상동 |
| tape measure(곡면) | 65.6% | 박스 모서리에 여백 발생 — 정상 |
| crumpled tissue(불규칙) | 60.3% | 박스로 표현 안 되는 형상 |

낮은 값 자체가 오류는 아니며, 형상이 사각형에서 멀수록 자연히 낮아진다.

> [!WARNING]
> 이 표는 검증 범위(1절)의 desk01·desk02가 아니라, 세션 초반에 쓴 **별도의 소품 근접 촬영 사진**(카드·포스트잇·줄자·구겨진 티슈가 놓인 책상)에서 나온 값이다.
> [[02 - 로컬 VLM(Qwen3-VL) 실측|02번 문서]]의 로컬 VLM fill_ratio(대체로 20~80%, 일부 0%)는 다시 이 사진이 아니라 사무실 데스크 장면(모니터·마우스·케이블 등)에서 나온 값이다.
> 동일 조건(같은 사진, 같은 물체)에서 두 백엔드의 fill_ratio를 나란히 측정한 적은 없다 — 이 자체가 후속 검증 항목이다.
> [[#6. 확인하지 않은 것|2번 문서 6장]]에서 진행한 실제 desk02 동일 사진 비교는 fill_ratio가 아니라 박스 위치의 육안 비교였다.

## 6. 확인하지 않은 것

- 최대 1FPS 영상 입력 제약과의 관계 — 이번 검증은 정지 이미지 호출만 했고 스트리밍/영상 입력 경로는 시험하지 않았다.
- 최초 인벤토리의 누락률·환각률 — 사진 2장에서 육안 확인한 수준이며 통계적으로 유의한 표본이 아니다.
