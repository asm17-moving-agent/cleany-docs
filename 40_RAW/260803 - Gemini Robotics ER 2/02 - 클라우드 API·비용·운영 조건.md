---
ingest_targets:
  - technical
  - decision
decision_candidates:
  - "Gemini Robotics ER 2 일반 API와 Streaming API 사용 범위"
date: 2026-08-03
source_type: official-docs-and-project-analysis
source_title: "Gemini Robotics ER 2 API 공식 문서"
---

# 260803 - Gemini Robotics ER 2 클라우드 API·비용·운영 조건

## 출처

- [Gemini API Robotics 문서](https://ai.google.dev/gemini-api/docs/robotics-overview)
- [Google ER 2 소개](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/)
- [Gemini API 가격](https://ai.google.dev/gemini-api/docs/pricing)
- [Gemini API 추가 약관](https://ai.google.dev/gemini-api/terms)

## 실행 위치

ER 2는 Gemini API를 통해 사용하는 클라우드 모델이다. Jetson은 카메라·ROS 상태를
정리해 API에 전달하고 응답을 검증해 로컬 Capability를 호출한다. 고주기 제어와
안전 정지는 네트워크 연결과 독립적으로 동작해야 한다.

```text
RGB-D·Mission Context
        ↓
Jetson Edge Orchestrator
        ↓ HTTPS / Live API
Gemini Robotics ER 2
        ↓ structured result / function call
Local Guard → Robot Capability → Robot
```

## Endpoint 선택

| Endpoint | 적합한 용도 | Cleany 검증 순서 |
|---|---|---|
| `gemini-robotics-er-2-preview` | 정지 이미지·짧은 영상, 구조화 결과, 이벤트 기반 계획 | 먼저 검증 |
| `gemini-robotics-er-2-streaming-preview` | 연속 영상·음성, 저지연 function calling, 진행 관찰 | 기본 계약 검증 후 |

초기 실험은 정지 이미지에서 장면·분류·순서를 구조화해 받는 방식으로 시작한다.
이후 검증된 Capability를 tool로 노출하고, 마지막에 Streaming 기반 진행 추적과
재계획을 평가한다.

## 비용과 운영 조건

가격, 무료·유료 tier, 지역, quota와 데이터 처리 조건은 변동 가능하므로 숫자를 KB의
고정 사실로 복사하지 않는다. 실험 시점의 공식 가격표와 계정 console을 근거로
호출량·영상 길이·실제 청구 비용을 기록한다.

확인할 운영 조건:

- 요청당 이미지·영상 크기와 end-to-end 지연
- API 오류·rate limit·network loss 시 로컬 동작
- 요청·응답 로그와 영상 보존 범위
- 식별 가능한 사람이 포함될 때 고지·동의·최소 수집 조건
- API key 제한과 로봇 장치 내 secret 관리

## 채택 판단

ER 2는 현재 목표 AI 실험 경로이지 무조건적인 운영 의존성이 아니다. 정확도, 지연,
실패 형태, 비용과 개인정보 조건을 실제 Cleany 입력으로 측정한 뒤 역할을 확정한다.
API가 실패해도 safe stop, e-stop과 현재 동작의 안전한 종료는 로컬에서 가능해야 한다.
