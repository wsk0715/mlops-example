# Phase 1 — MVP

> 기간: 2-4주
> PoC 완료 후 시작.
> 목표: CLI로 로컬 GPU 학습 -> 자동 메트릭 Push -> Web 차트 비교 -> Model Registry -> CPU Serving.

---

## PoC 대비 변경/추가 사항

| 항목 | PoC | MVP |
|------|-----|-----|
| 실험 메트릭 | 수동 입력 | CLI가 epoch마다 API push |
| 아티팩트 | 없음 | best.pt, results.png 자동 push |
| 모델 관리 | 없음 | Model Registry + Stage + Serving |
| Frontend 차트 | 텍스트 | Chart.js 선 그래프 (epoch별 mAP) |
| Docker | 3 containers | +rabbitmq +celery +serving |
| CLI | login, dataset pull | +experiment run, model register |

## 추가 데이터 모델

### experiment_metrics
- UNIQUE(experiment_id, epoch, metric_key)
- id(UUID PK), experiment_id(FK), epoch(INT), metric_key(VARCHAR 100), metric_value(FLOAT), logged_at(TIMESTAMPTZ)
- INDEX on (experiment_id, epoch)

### experiment_artifacts
- id(UUID PK), experiment_id(FK), artifact_type(VARCHAR 50) CHECK('weight','chart','log','other'), file_name(VARCHAR 255), r2_key(VARCHAR 500), file_size(BIGINT), created_at

### model_registry
- UNIQUE(project_id, name)
- id(UUID PK), project_id(FK), name(VARCHAR 200), description(TEXT), task(VARCHAR 50) DEFAULT 'detect', class_names(TEXT[]), created_by(FK), created_at, updated_at

### model_versions
- UNIQUE(model_id, version)
- id(UUID PK), model_id(FK), version(INT), experiment_id(FK nullable), r2_weight_key(VARCHAR 500), r2_onnx_key(VARCHAR 500 nullable), metrics(JSONB), file_size(BIGINT), created_by(FK), created_at

### model_stages
- id(UUID PK), model_version_id(FK), stage(VARCHAR 20) CHECK('none','staging','production','archived'), previous_stage(VARCHAR 20 nullable), promoted_by(FK), note(TEXT), created_at

## 추가 API

| Method | Path | Description |
|--------|------|-------------|
| POST | /experiments/{id}/metrics/batch | CLI epoch push: {epoch, metrics:{key:val}} |
| POST | /experiments/{id}/artifacts | multipart file upload (CLI 호출) |
| GET | /experiments/{id}/artifacts/{aId}/download | signed URL |
| POST | /experiments/compare | {experiment_ids} -> metrics 비교 |
| POST | /models | 실험 -> 모델 등록 |
| GET | /models?project_id= | 모델 목록 |
| GET | /models/{id} | 모델 + 버전 목록 |
| PUT | /models/{id}/versions/{vId}/stage | stage 변경 |
| GET | /models/{id}/versions/{vId}/stage-history | stage 이력 |
| POST | /serving/deploy | model_version_id -> serving 배포 |
| GET | /serving/status | 서빙 상태 조회 |
| POST | /serving/rollback | 이전 version으로 롤백 |

### metrics/batch 상세
- POST /experiments/{id}/metrics/batch
- Request: {epoch: int, metrics: {metric_key: float_value, ...}}
- key 예시: train/box_loss, val/mAP50, val/mAP50-95, metrics/precision(B), metrics/recall(B), lr/pg0

### compare 상세
- POST /experiments/compare
- Request: {experiment_ids: [uuid, uuid, ...]}
- Response: 각 실험별 params + metrics_summary + best 비교

### model register 상세
- POST /models: {experiment_id, name, description}
- 처리: experiment_artifacts에서 best.pt 조회 -> model registry 생성 -> model_versions 생성 (version=1) -> model_stages (stage='none')

## Serving Module (별도 프로세스 :9000)

- 독립 FastAPI 앱, port 9000, CPU 전용
- 시작 시 PostgreSQL에서 production stage 최신 version 조회
- R2에서 best.pt 다운로드 -> YOLO model 로드
- POST /predict (X-API-Key 인증): image bytes -> YOLO inference -> detections JSON
- GET /health: {status, model_loaded, device, uptime, total_predictions}

### predict 응답 형식
```json
{
  "success": true,
  "detections": [
    {"bbox": {"x1":100,"y1":200,"x2":300,"y2":400}, "class_id": 0, "class_name": "person", "confidence": 0.952}
  ],
  "image_width": 1280, "image_height": 720, "inference_time_ms": 45.2
}
```

## CLI 추가 명령어

### experiment run
- `mlops-cli experiment run --project <id> --name <name> --dataset <path> --params <json> --device cuda:0`
- 내부 처리: POST /experiments 생성 -> 실험 등록 -> Ultralytics callback 등록 -> model.train() 로컬 실행 -> epoch마다 POST /metrics/batch -> 완료 후 POST /artifacts (best.pt, results.png) -> PUT /experiments (status=completed, metrics)

### model register
- `mlops-cli model register <experiment_id> --name <name>`
- POST /models로 등록. 응답에 model_id, version, mAP50 표시

## Stage Lifecycle

```
none -> staging -> production -> archived
           ^            |
           +------------+ (rollback)
```

- 같은 stage에 여러 version 가능
- Serving은 production stage 중 최신 version 사용

## Docker Compose 추가 (PoC +)

- **rabbitmq**: rabbitmq:3.13-management-alpine, 볼륨 rabbitmq_data
- **celery_worker**: backend/ Dockerfile, command celery -A tasks.celery_app worker, CPU-only, depends on rabbitmq
- **serving**: serving/app/ Dockerfile, port 9000, SERVING_DEVICE=cpu, volumes serving_cache

## Frontend 추가

### MetricChart.vue
- Chart.js line chart: epoch vs val/mAP50-95
- 다중 실험 overlay (다른 색상)
- zoom, pan 가능

### ExperimentCompareView.vue
- 2~4개 experiment 선택 -> MetricChart overlay + 파라미터/메트릭 테이블

### ModelRegistryView.vue
- Card grid: model name, latest version, stage badge (color-coded)
- StageBadge 색상: none=gray, staging=blue, production=green, archived=red

### ModelDetailView.vue
- Version timeline, metrics 테이블
- Promote to staging / production / archive 버튼
- Deploy to serving 버튼

### ServingView.vue
- 현재 serving 중인 model 표시
- Deploy / Rollback 버튼
- Health status (live/stopped/error)

## 구현 순서

1. DB migration: experiment_metrics, experiment_artifacts, model_registry 테이블 추가
2. Backend: metrics batch API, artifact upload API
3. Backend: model_registry CRUD + stage API
4. Backend: serving deploy API, compare API
5. Frontend: MetricChart, ExperimentCompareView
6. Frontend: ModelRegistryView, ModelDetailView, ServingView
7. CLI: experiment run (with epoch callback -> metric push)
8. CLI: model register
9. Serving: predictor + predict/health endpoints
10. Docker: rabbitmq, celery_worker, serving 추가

## 검증 기준

- [ ] CLI experiment run -> 로컬 GPU 학습 -> epoch마다 Web UI에 메트릭 표시
- [ ] 2개 실험 선택 -> 비교 차트 정상 동작
- [ ] Model Registry 등록 -> stage=production -> serving /predict 응답
- [ ] 팀원 2명이 각자 노트북 학습 후 결과 공유/비교
- [ ] CPU serving: image 1장 predict 1초 이내 (YOLOv8n 기준)
