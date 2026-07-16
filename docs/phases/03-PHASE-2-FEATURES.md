# Phase 2 — 추가기능

> 기간: 4-6주
> MVP 완료 후 시작.
> 운영 편의성 + 데이터셋 고급 시각화.

---

## 구현 항목

| 우선순위 | 기능 | 설명 |
|----------|------|------|
| High | Annotation Viewer | 이미지 위 bbox overlay 시각화 (canvas) |
| High | Dataset Version Diff | 두 버전 간 이미지/annotation 차이 비교 |
| High | COCO/VOC -> YOLO 변환 | 업로드 시 자동 변환 |
| High | Dataset Web Download | Web UI에서 ZIP 다운로드 버튼 |
| Medium | Dashboard | 최근 실험 통계, 요약 카드 |
| Medium | Team Management UI | 멤버 초대, 역할 변경, 추방 |
| Low | ONNX Export | 실험 완료 시 자동 ONNX 변환 |

## 상세: Annotation Viewer

### API
- GET /datasets/{id}/versions/{vId}/images -> {items: [{id, filename, signed_url, width, height}], total}
- GET /datasets/{id}/versions/{vId}/images/{imgId}/annotation -> YOLO txt content

### Frontend
- AnnotationViewer.vue: canvas에 이미지 로드 + bbox overlay (class별 색상)
- Navigation: prev/next image, zoom(wheel), pan(drag)
- 우측 패널: class 분포 doughnut chart (Chart.js)

## 상세: Dataset Version Diff

### API
- GET /datasets/{id}/versions/{a}/diff?version_b={b}
- Response: {version_a, version_b, added_images[], removed_images[], class_distribution_a, class_distribution_b, total_images_a, total_images_b}

### Frontend
- Version selector (A vs B dropdown)
- Added images: green highlight, Removed: red
- Class 분포 bar chart side-by-side

## 상세: COCO/VOC -> YOLO 변환

Dataset upload 시 annotation_format 선택 옵션과 함께 변환 처리:
- coco_json: categories[] -> class_names 매핑, annotations[] -> 각 이미지별 YOLO txt
- voc_xml: bndbox [xmin,ymin,xmax,ymax] -> YOLO [cx,cy,w,h] (정규화)
- 변환 실패 시 422 + 상세 메시지

## 상세: Dashboard

### API
- GET /dashboard?project_id={id}
- Response: {total_datasets, total_experiments, running_experiments, recent_experiments[5], best_model{name, mAP50-95}}

### Frontend
- DashboardView: MetricCard(row) + RecentExperimentsTable + ActiveTrainingProgress

## 상세: Team Management

### API (PoC API 사용 + Frontend만 추가)
- POST /teams/{id}/members: 멤버 초대
- PUT /teams/{id}/members/{userId}: 역할 변경
- DELETE /teams/{id}/members/{userId}: 추방

### Frontend
- TeamSettingsView: 팀 정보 수정, 멤버 테이블(role, joined_at), 초대/역할변경/추방 버튼

## 상세: ONNX Export

CLI에 --export onnx 옵션 추가:
- 학습 완료 후 YOLO model.export(format='onnx')
- 생성된 .onnx 파일을 artifact로 push
- model_versions.r2_onnx_key 업데이트

## 검증 기준

- [ ] Annotation viewer: 이미지 로드 -> bbox 정확히 overlay -> zoom/pan 정상
- [ ] Dataset version diff: 버전 간 차이 표시 (추가/삭제 이미지)
- [ ] COCO JSON 업로드 -> 자동 YOLO 변환 -> data.yaml 정상
- [ ] Dashboard: 통계 수치, 최근 실험 목록 정상 표시
- [ ] Team: 멤버 초대 -> 역할 변경 -> 추방
- [ ] ONNX export -> .onnx 생성 -> artifact 업로드 확인
