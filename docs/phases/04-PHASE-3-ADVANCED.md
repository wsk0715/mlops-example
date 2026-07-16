# Phase 3 — 고도화

> 기간: 8-12주
> Phase 2 완료 후 시작.
> 자동화, 확장, 프로덕션 안정성.

---

## 구현 항목

| 우선순위 | 기능 | 설명 |
|----------|------|------|
| 선택 | 서버 GPU 학습 | GPU 서버 추가 시 Celery + GPU 학습 지원 |
| High | Hyperparameter Sweep | 여러 파라미터 조합 자동 실행/비교 |
| Medium | 데이터 증강 | 학습 전 augmentation 적용 (YOLO 내장) |
| Medium | CI/CD 통합 | GitHub Actions -> 자동 학습 -> PR comment |
| Low | Slack 알림 | 학습 완료 시 Slack webhook |
| Low | Data Drift 감시 | Production 이미지 분포 변화 감지 |
| Low | Auto-labeling | 기학습 모델로 pseudo-label 생성 |
| Low | Helm Chart | Kubernetes 배포 |

## 상세: 서버 GPU 학습 (선택)

GPU 서버가 추가되면 backend/tasks/train_task.py 복원:
- R2 -> temp dir download -> YOLO model.train(device=0) -> epoch마다 metric 기록 -> 완료 시 artifact upload
- CLI experiment run과 동일한 API 사용
- docker-compose celery_worker에 nvidia GPU 예약 추가

## 상세: Hyperparameter Sweep

### API
- POST /sweeps: {project_id, name, base_config, grid:{key:[values]}} -> N개 experiment 자동 생성
- GET /sweeps?project_id=: sweep 목록 + 각 experiment 결과 요약

### 처리
- grid의 Cartesian product 계산 -> 개별 experiment 생성
- 각 experiment는 CLI experiment run으로 개별 실행 가능
- 서버는 메타관리만, 실제 학습은 CLI

## 상세: 데이터 증강

data.yaml에 augmentation config 추가:
```yaml
augmentation:
  mosaic: 1.0; mixup: 0.1; hsv_h: 0.015; hsv_s: 0.7; hsv_v: 0.4
  degrees: 0.0; translate: 0.1; scale: 0.5; fliplr: 0.5
```
- CLI가 config 읽어 YOLO model.train()에 전달
- YOLO 내장 augmentation 사용

## 상세: CI/CD 통합

### GitHub Actions
- trigger: PR 생성 시 dataset/ 또는 config/ 경로 변경 감지
- self-hosted GPU runner에서 mlops-cli로 학습 실행
- 결과를 PR comment로 자동 등록 (mAP50, mAP50-95)

## 상세: Slack 알림

- 학습 완료 시 Slack webhook 호출
- opt-in (user.notify_slack 설정)
- 완료 시점에만 발송 (epoch마다 X)

## 상세: Data Drift 감시

- Production model 입력 이미지 class 분포 vs 학습 데이터 class 분포
- KL divergence 계산 -> threshold 초과 시 alert
- model_stages에 drift note 기록

## 상세: Auto-labeling

- Model registry의 best.pt로 unlabeled images inference
- confidence > threshold(0.7)인 bbox만 YOLO txt 생성
- 새 dataset_version으로 저장
- Web UI에서 'auto-labeled' badge 표시, 수동 검수

## 상세: Helm Chart

- Docker Compose 구성을 Kubernetes manifest로 변환
- postgres, api, frontend, serving deployment + service
- PVC for postgres/rabbitmq
- GPU nodeSelector for celery_worker (optional)

## 검증 기준

- [ ] (선택) GPU 서버 학습: CLI와 동일한 결과
- [ ] Sweep: experiment 6개 자동 생성 + 비교
- [ ] 데이터 증강: augmentation 적용된 training 결과 확인
- [ ] CI/CD: PR 생성 -> 자동 학습 -> PR comment
- [ ] Slack: 학습 완료 시 채널 메시지
- [ ] Drift: class 분포 변화 감지
- [ ] Auto-label: pseudo-label dataset version 생성
