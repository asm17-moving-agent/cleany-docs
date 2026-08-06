---
ingest_targets:
  - technical
  - decision
decision_candidates:
  - "Gemini Robotics ER 2와 Robot Capability의 책임 경계"
date: 2026-08-03
source_type: official-docs-and-project-analysis
source_title: "Gemini Robotics ER 2 공식 발표·API 문서·모델 카드"
---

# 260803 - Gemini Robotics ER 2

## 공식 출처

- [Google DeepMind: Gemini Robotics 2 발표](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)
- [Google: Introducing Gemini Robotics ER 2](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/)
- [Gemini API Robotics 문서](https://ai.google.dev/gemini-api/docs/robotics-overview)
- [Gemini Robotics ER 2 Model Card](https://deepmind.google/models/model-cards/gemini-robotics-er-2/)

공식 발표일은 미국 기준 2026년 7월 30일이며 한국 시간으로는 7월 31일이다.
이 묶음은 위 공식 자료와 Cleany 적용 검토를 분리해 기록한다.

## 확인된 사실

- ER 2는 Gemini 3.5 Flash 기반의 embodied reasoning VLM이다.
- 텍스트·이미지·비디오·오디오를 입력으로 받고 텍스트·함수 호출을 출력한다.
- 공간 추론, 비디오 진행도·성공 탐지, 다단계 tool orchestration을 지원한다.
- `gemini-robotics-er-2-preview`와 Live API용
  `gemini-robotics-er-2-streaming-preview`가 제공된다.
- ER 2는 motor action을 직접 내는 VLA가 아니라, 하위 VLA나 Navigation API 같은
  개발자 제공 도구를 호출하는 고수준 에이전트다.
- Gemini Robotics 2와 On-Device 2 VLA는 공개 API가 아니라 early-access 대상이다.
- 모델 판단은 물리적 안전장치와 로컬 제어 검증을 대체하지 않는다.

## Cleany 적용 가설

```text
작업 목표 + 책상 관찰
        ↓
ER 2: 장면 해석·대상 선택·처리 순서·진행 판단
        ↓ 검증된 tool request
Robot Capabilities
├─ Navigation
├─ Manipulation Skills (VLA-backed 포함 가능)
└─ Safety Controls (계획 경로와 독립)
        ↓
실행 결과 + 최신 관찰 → ER 2 재계획
```

ER 2가 Navigation까지 직접 호출할지, 책상 도착 후 작업에만 관여할지는 아직
결정하지 않았다. 현재 Mission Manager 구현은 Navigation과 책상 작업 실행을
분리한다.

## 문서 지도

| 문서 | 내용 |
|---|---|
| [역할·기능·한계](01%20-%20ER%202%20역할·기능·한계.md) | 공식 모델 구분과 Cleany 적용 경계 |
| [클라우드 API·운영 조건](02%20-%20클라우드%20API·비용·운영%20조건.md) | 엔드포인트, 네트워크와 도입 판단 |
| [시스템 아키텍처와 책임 경계](03%20-%20시스템%20아키텍처와%20책임%20경계.md) | ER 2, Capability, 안전 계층 관계 |
| [다중 객체 폐루프 시나리오](05%20-%20다중%20객체%20폐루프%20정리%20시나리오%20예시.md) | 여러 물체의 관찰·실행·재관찰 예시 |

## 검증 상태

공식 모델 설명과 실제 Cleany 적합성은 구분한다. 정지 이미지 기반 ER 2→SAM2→Depth
실측은 [[40_RAW/260804 - 인식 파이프라인 로컬 실측 검증/00 - README|별도 Raw 묶음]]에
기록되어 있다. Streaming, 실제 VLA tool orchestration과 실제 로봇 폐루프는 아직
검증하지 않았다.
