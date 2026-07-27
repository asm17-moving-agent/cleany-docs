---
type: technical
status: draft
reviewers:
  -
tags:
  - technical
  - hardware
  - robot-platform
  - components
  - cleany
source_refs:
  - "비공개 Raw 원본: 끌리니 하드웨어 구성 및 부품 목록"
related_decisions:
  - "30_DECISIONS/Technical/260708 - XLeRobot 기반 플랫폼.md"
  - "30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스.md"
  - "30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB.md"
related_jira:
  -
updated: 2026-07-27
---

# 하드웨어 구성(Hardware Configuration)

## 1. 요약

끌리니는 XLeRobot 상부 모듈의 듀얼 매니퓰레이터와 RGB-D 카메라를 유지하고, 알루미늄 프로파일 기반 트롤리 프레임 및 4륜 Mecanum 이동 베이스를 결합하는 모바일 매니퓰레이터를 예비 구성으로 둔다.

이 문서는 부품의 역할과 대략적인 배치 개념을 공유하기 위한 `draft` 기술 문서다. 실제 기구 치수, 배선, 전력 정격, 통신 계약 및 실장 위치는 별도 검토가 필요하다.

## 2. 하드웨어 구성 개념도

![끌리니 하드웨어 구성 개념도](<assets/hardware/cleany-hardware-concept-v1.png>)

이미지는 부품 간 관계를 설명하기 위한 AI 생성 개념도다. 실제 조립도, 최종 BOM 또는 안전 검증 결과로 해석하지 않는다.

## 3. 구성 요소와 역할

| 구성부 | 대표 구성 요소 | 역할 |
| --- | --- | --- |
| 컴퓨팅·제어 | Jetson Orin NX 16GB, ESP32 제어 PCB | 온디바이스 추론, ROS 2 런타임, 상위 제어와 저수준 제어 연결 |
| 인지·센서 | Intel RealSense D435, RPLIDAR A1M8, 매니퓰레이터 카메라 | 작업 대상 관측, 깊이 정보 획득, 지도 작성·위치 추정·장애물 인지 |
| 이동 베이스 | 127 mm Mecanum wheel, PG42 DC gear motor, Cytron MDD20A | 전후·좌우 병진과 회전, 모터 구동, 엔코더 기반 odometry 입력 |
| 작업 매니퓰레이터 | 듀얼 매니퓰레이터, Feetech STS3215·STS3250 | 물체 접근, 파지, 운반과 투입 |
| 전원 | 3S battery pack, DC-DC converter, 보호 회로 | 이동 환경의 전원 공급과 각 장치 전압 변환 |
| 배선·기구 | 알루미늄 프로파일, 커넥터·하네스, 3D printed mount | 상부 모듈·베이스 결합, 전원·신호 연결과 센서·컴퓨팅 장치 고정 |

## 4. 배치 개념

- **상단:** 듀얼 매니퓰레이터와 Intel RealSense D435를 배치해 작업 공간과 그리퍼 주변을 관측한다.
- **중간층:** RPLIDAR A1M8을 수평 스캔이 가능한 높이에 배치한다.
- **하부 전자 장비 구역:** Jetson Orin NX 16GB, 3S battery pack, ESP32 제어 PCB와 Cytron MDD20A를 배치하는 후보 영역이다.
- **이동 베이스:** 4륜 Mecanum wheel과 독립 DC gear motor로 holonomic 이동을 구현하는 후보 구조다.

## 5. 제약과 검토 필요 항목

- 프레임의 실제 치수·강성·무게중심은 매니퓰레이터 도달 범위와 이동 안정성을 기준으로 검증해야 한다.
- Jetson, 배터리, 모터 드라이버의 방열·방진·보호 회로와 최종 전력 예산은 추가 정의가 필요하다.
- wheel geometry, encoder parameter, ESP32 통신 방식, 속도·가속도 제한과 emergency stop 경로는 아직 확정되지 않았다.
- RGB-D, LiDAR, IMU, 매니퓰레이터의 frame·calibration·QoS 계약은 [[20_TECHNICAL/10 - Robot ROS Contract|Robot ROS Contract]]에서 별도로 정의한다.

## 6. 관련 결정

- [[30_DECISIONS/Technical/260708 - XLeRobot 기반 플랫폼|XLeRobot 기반 플랫폼]]: 듀얼 매니퓰레이터와 깊이 카메라를 유지하는 `selected` Decision이다.
- [[30_DECISIONS/Technical/260714 - 4륜 메카넘 베이스|4륜 메카넘 베이스]]: 4륜 Mecanum custom base를 사용하는 `selected` Decision이다.
- [[30_DECISIONS/Technical/260714 - Jetson Orin NX 16GB|Jetson Orin NX 16GB]]: 메인 엣지 컴퓨팅 장치를 정한 `selected` Decision이다.
