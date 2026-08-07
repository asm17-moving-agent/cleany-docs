# 읽기 가이드(Reading Guide)

루트 [README.md](../README.md)의 기본 읽기 순서를 확인한 뒤, 아래에서 목적에 맞는
경로를 고른다.

## 기획 리뷰

1. [Problem and Users](<../10_PLANNING/01 - Problem and Users.md>)
2. [Target Scenario](<../10_PLANNING/02 - Target Scenario.md>)
3. [Scope and Non-Goals](<../10_PLANNING/04 - Scope and Non-Goals.md>)
4. [Success Criteria](<../10_PLANNING/05 - Success Criteria.md>)
5. [Planning Questions](<../10_PLANNING/99 - Questions.md>)

확인할 점:

- 스터디카페 운영자 문제와 아직 검증되지 않은 가설이 구분되는가?
- Dashboard 요청부터 전후 결과까지 E2E 범위가 이어지는가?
- 분실물 처리처럼 정하지 않은 행동이 확정처럼 쓰이지 않았는가?

## 기술 리뷰

1. [System Context](<../20_TECHNICAL/01 - System Context.md>)
2. [Task Planning and Robot Capabilities](<../20_TECHNICAL/03 - Task Planning and Robot Capabilities.md>)
3. [Perception and Scene Understanding](<../20_TECHNICAL/07 - Perception and Scene Understanding.md>)
4. [Mission Lifecycle](<../20_TECHNICAL/09 - Mission Lifecycle.md>)
5. [Safety and Risk](<../20_TECHNICAL/08 - Safety and Risk.md>)
6. 필요한 subsystem 문서
   - [Navigation and Mapping](<../20_TECHNICAL/05 - Navigation and Mapping.md>)
   - [Robot ROS Contract](<../20_TECHNICAL/10 - Robot ROS Contract.md>)
   - [ROS 2 Software Architecture](<../20_TECHNICAL/11 - ROS 2 Software Architecture.md>)
   - [Hardware Configuration](<../20_TECHNICAL/12 - Hardware Configuration.md>)
   - [Verification and Simulation Strategy](<../20_TECHNICAL/13 - Verification and Simulation Strategy.md>)

확인할 점:

- 후보 Planner의 고수준 제안과 Skill 내부 VLA 실행 가능성 검증이 구분되는가?
- Navigation과 Manipulation의 책임이 섞이지 않고 안전 정지가 일반 skill과 구분되는가?
- 목표 구조, 현재 구현과 실험 후보가 구분되는가?

## 프로젝트 설명

팀원이나 외부 사람에게 프로젝트를 설명할 때는 다음 순서로 본다.

1. [Project Brief](<../10_PLANNING/00 - Project Brief.md>)
2. [Target Scenario](<../10_PLANNING/02 - Target Scenario.md>)
3. [Technical Overview](<../20_TECHNICAL/00 - Technical Overview.md>)
4. [Success Criteria](<../10_PLANNING/05 - Success Criteria.md>)

미결정 사항을 설명해야 할 때만 Planning Questions와 Technical Questions를 추가한다.

## Decision과 Raw

Decision은 [Decision Index](<../30_DECISIONS/00 - Decision Index.md>)에서 시작한다.
Decision의 이유나 실험 근거가 필요할 때만 연결된 Raw를 읽는다. Raw는 초안, 개인
학습, 회의, 조사 공간이며 공식 결론이 아니다.

## Sprint와 구현

Jira는 작업 상태, 담당자, 일정의 Source of Truth다. 구현 사실, ROS interface,
실행 및 검증 명령은 Cleany 구현 레포와 각 package README에서 확인한다. KB 본문을
Jira에 복사하지 않고 관련 문서 링크만 연결한다.

## 외부 공유 전

1. 현재 기준 문서인지 검토 중인 변경안인지 확인한다.
2. Decision 대체 관계와 GitHub PR 승인 이력을 확인한다.
3. `$kb-quality-checks`, `$kb-audit`, 필요 시 `$kb-review-pack`을 실행한다.
