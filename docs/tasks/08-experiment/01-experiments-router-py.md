## Story

사용자가 실험을 생성하고 YOLO 하이퍼파라미터를 설정한다. 학습 진행 상태를 수동으로 업데이트한다.

## Spec

| Method | Path | Request | Description |
|--------|------|---------|-------------|
| POST | /experiments | {project_id, name, description, params:{}} | 201 생성 |
| GET | /experiments | ?project_id=&status= | paginated + status filter |
| GET | /experiments/{id} | - | params 포함 상세 |
| PUT | /experiments/{id} | {status, name} | 수정 |

POST 처리:
1. experiment 생성 (status=created)
2. experiment_params에 key-value 저장
3. response에 experiment + params 포함

## Completion

- [ ] POST -> 201 + experiment + params 반환
- [ ] GET /experiments?project_id= -> 목록
- [ ] GET /experiments?project_id=&status=running -> 필터
- [ ] GET /experiments/{id} -> params 포함
- [ ] PUT /experiments/{id} -> status 변경 확인
