## Story

사용자가 데이터셋을 업로드하면 여러 버전으로 관리된다. 각 버전마다 R2에 images + labels 디렉토리가 저장된다.

## Spec

**datasets**: id(UUID PK), name(VARCHAR 200), description(TEXT), project_id(FK), created_by(FK), class_names(TEXT[])

**dataset_versions**: UNIQUE(dataset_id, version). id(UUID PK), dataset_id(FK), version(INT), image_count(INT), annotation_format(VARCHAR 20) CHECK('yolo_txt','coco_json','voc_xml'), r2_prefix(VARCHAR 500), created_by(FK)

## Completion

- [ ] CREATE TABLE datasets + dataset_versions
- [ ] UNIQUE(dataset_id, version)
- [ ] annotation_format CHECK 제약
