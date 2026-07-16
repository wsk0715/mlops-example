## Story

사용자가 웹 UI에서 데이터셋을 업로드하고 버전을 관리한다. CLI에서 다운로드한다.

## Spec

| Method | Path | Description |
|--------|------|-------------|
| POST | /datasets | multipart: name, project_id, class_names, annotation_format, files |
| GET | /datasets?project_id= | 목록 (pagination) |
| GET | /datasets/{id} | 상세 |
| GET | /datasets/{id}/versions | 버전 목록 |
| POST | /datasets/{id}/versions | 새 버전 업로드 |
| GET | /datasets/{id}/versions/{vId}/download | signed download URL |

POST /datasets:
- request: multipart/form-data
- 내부에서 dataset row 생성 -> dataset_service.handle_upload() 호출 -> DatasetVersion row 생성
- response: 201 DatasetResponse

## Completion

- [ ] POST /datasets (multipart) -> 201
- [ ] GET /datasets?project_id= -> 목록
- [ ] GET /datasets/{id}/versions -> 버전 리스트
- [ ] GET /datasets/{id}/versions/{vId}/download -> signed URL
