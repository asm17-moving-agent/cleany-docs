---
status: draft
---

# 읽기 가이드(Reading Guide)

## 15분 안에 이해하기

1. [[10_PLANNING/00 - Project Brief|Project Brief]]
2. [[10_PLANNING/02 - Target Scenario|Target Scenario]]
3. [[10_PLANNING/05 - Success Criteria|Success Criteria]]
4. [[20_TECHNICAL/00 - Technical Overview|Technical Overview]]
5. [[10_PLANNING/99 - Questions|Planning Questions]]과
   [[20_TECHNICAL/99 - Questions|Technical Questions]]
6. [[30_DECISIONS/00 - Decision Index|Decision Index]]

이 순서로 읽으면 제품 목표, 데모 흐름, 기술 경계와 실제 열린 질문을 구분할 수 있다.

## 기획 리뷰

1. [[10_PLANNING/01 - Problem and Users|Problem and Users]]
2. [[10_PLANNING/02 - Target Scenario|Target Scenario]]
3. [[10_PLANNING/04 - Scope and Non-Goals|Scope and Non-Goals]]
4. [[10_PLANNING/05 - Success Criteria|Success Criteria]]
5. [[10_PLANNING/99 - Questions|Planning Questions]]

확인할 점:

- 스터디카페 운영자 문제와 아직 검증되지 않은 가설이 구분되는가?
- Dashboard 요청부터 전후 결과까지 E2E 범위가 이어지는가?
- 분실물 처리처럼 정하지 않은 행동이 확정처럼 쓰이지 않았는가?

## 기술 리뷰

1. [[20_TECHNICAL/01 - System Context|System Context]]
2. [[20_TECHNICAL/03 - Task Planning and Robot Capabilities|Task Planning and Robot Capabilities]]
3. [[20_TECHNICAL/07 - Perception and Scene Understanding|Perception and Scene Understanding]]
4. [[20_TECHNICAL/09 - Mission Lifecycle|Mission Lifecycle]]
5. [[20_TECHNICAL/08 - Safety and Risk|Safety and Risk]]
6. 필요한 subsystem 문서
   - [[20_TECHNICAL/05 - Navigation and Mapping|Navigation and Mapping]]
   - [[20_TECHNICAL/10 - Robot ROS Contract|Robot ROS Contract]]
   - [[20_TECHNICAL/11 - ROS 2 Software Architecture|ROS 2 Software Architecture]]
   - [[20_TECHNICAL/12 - Hardware Configuration|Hardware Configuration]]
   - [[20_TECHNICAL/13 - Verification and Simulation Strategy|Verification and Simulation Strategy]]

확인할 점:

- ER 2의 고수준 판단과 Skill 내부 VLA 실행이 구분되는가?
- Navigation, Manipulation과 Safety Control의 책임이 섞이지 않는가?
- 목표 구조, 현재 구현과 실험 후보가 구분되는가?

## Decision과 Raw

Decision은 [[30_DECISIONS/00 - Decision Index|Decision Index]]에서 시작한다.
Decision의 이유나 실험 근거가 필요할 때만 연결된 Raw를 읽는다. Raw는 초안·개인
학습·회의·조사 공간이며 공식 결론이 아니다.

## Sprint와 구현

Jira는 작업 상태·담당자·일정의 Source of Truth다. 구현 사실, ROS interface,
실행·검증 명령은 Cleany 구현 레포와 각 package README에서 확인한다. KB 본문을
Jira에 복사하지 않고 관련 문서 링크만 연결한다.

## 외부 공유 전

1. `draft`를 확정 사실처럼 공유하지 않는다.
2. Decision status와 GitHub PR 승인 이력을 확인한다.
3. `$kb-quality-checks`, `$kb-audit`, 필요 시 `$kb-review-pack`을 실행한다.
