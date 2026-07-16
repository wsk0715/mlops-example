## Story

사용자가 실험을 생성하고 하이퍼파라미터(YOLO model/epochs/batch/lr0 등)를 설정한다. 실험 상태를 수동으로 변경한다.

## Spec

**experiments**: id(UUID PK), project_id(FK), name(VARCHAR 200), description(TEXT), status(VARCHAR 20) DEFAULT 'created' CHECK('created','running','completed','failed'), dataset_version_id(FK nullable), created_by(FK), started_at(TIMESTAMPTZ nullable), completed_at(TIMESTAMPTZ nullable)

**experiment_params**: UNIQUE(experiment_id, param_key). id(UUID PK), experiment_id(FK), param_key(VARCHAR 100), param_value(TEXT)

## Completion

- [ ] CREATE TABLE experiments + experiment_params
- [ ] status CHECK 제약
- [ ] UNIQUE(experiment_id, param_key)
