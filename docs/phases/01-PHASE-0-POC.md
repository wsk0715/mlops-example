# Phase 0 — PoC

> 기간: 1-2주
> 목표: 데이터셋 업로드 -> 실험 생성 -> 수동 메트릭 입력 -> CLI 데이터셋 다운로드.
> Web UI + CLI 기본 연동 완료.

---

## 구현해야 할 기능

| 순서 | 기능 | 설명 |
|------|------|------|
| 1 | User + Team ORM | 회원가입/로그인, 팀 생성, 멤버 관리 |
| 2 | Schema 정의 | Pydantic request/response |
| 3 | Auth API | register, login, refresh, me |
| 4 | Project CRUD | 생성/조회/수정/삭제 |
| 5 | Storage Service | R2(S3) upload/download/signed URL |
| 6 | Dataset Upload | zip 압축해제 -> 검증 -> split -> R2 저장 -> data.yaml 생성 |
| 7 | Dataset Version | 버전 관리, download signed URL |
| 8 | Experiment CRUD | 생성, params 저장, 수동 status 변경 |
| 9 | DB Migration | Alembic autogenerate |
| 10 | Frontend 로그인/회원가입 | LoginView, RegisterView |
| 11 | Frontend 프로젝트 목록/상세 | DashboardView, ProjectDetailView |
| 12 | Frontend 데이터셋 업로드/조회 | DatasetListView, DatasetDetailView |
| 13 | Frontend 실험 생성/조회 | ExperimentListView, ExperimentDetailView |
| 14 | CLI auth login | 서버 URL 입력 -> JWT 저장 -> config.json |
| 15 | CLI dataset pull | dataset_id -> signed URL -> zip -> 로컬 extract |
| 16 | Docker Compose | postgres + api + frontend |

## 구현할 API 목록

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /auth/register | No | 회원가입 |
| POST | /auth/login | No | 로그인 |
| POST | /auth/refresh | No | 토큰 갱신 |
| GET | /users/me | Yes | 내 정보 |
| POST | /teams | Yes | 팀 생성 |
| GET | /teams | Yes | 팀 목록 |
| POST | /projects | Yes | 프로젝트 생성 |
| GET | /projects | Yes | 프로젝트 목록 (pagination) |
| GET | /projects/{id} | Yes | 프로젝트 상세 |
| PUT | /projects/{id} | Yes | 프로젝트 수정 |
| DELETE | /projects/{id} | Yes | 프로젝트 삭제 |
| POST | /datasets | Yes | 데이터셋 업로드 (multipart) |
| GET | /datasets?project_id= | Yes | 데이터셋 목록 |
| GET | /datasets/{id} | Yes | 데이터셋 상세 |
| POST | /datasets/{id}/versions | Yes | 새 버전 업로드 |
| GET | /datasets/{id}/versions | Yes | 버전 목록 |
| GET | /datasets/{id}/versions/{vId}/download | Yes | download signed URL |
| POST | /experiments | Yes | 실험 생성 |
| GET | /experiments?project_id= | Yes | 실험 목록 (status filter) |
| GET | /experiments/{id} | Yes | 실험 상세 (params 포함) |
| PUT | /experiments/{id} | Yes | 상태/메트릭 업데이트 |

## DB 마이그레이션 (Alembic)

- `alembic init alembic` 후 async 환경에 맞게 env.py 수정
- target_metadata = Base.metadata (from app.models import Base)
- `alembic revision --autogenerate -m "init"` 실행
- 생성된 migration에 모든 PoC 테이블 포함 확인: users, teams, team_members, projects, datasets, dataset_versions, experiments, experiment_params
- API 컨테이너 시작 시 `alembic upgrade head` 자동 실행
- PostgreSQL 확장: `CREATE EXTENSION IF NOT EXISTS "pgcrypto"` (gen_random_uuid)

## 데이터 모델

### users
- id(UUID PK), username(VARCHAR 50 UNIQUE NOT NULL), hashed_password(VARCHAR 255 NOT NULL), is_active(BOOL DEFAULT true)

### teams
- id(UUID PK), name(VARCHAR 100 NOT NULL), description(TEXT nullable), owner_id(FK users)

### team_members
- UNIQUE(team_id, user_id). id(UUID PK), team_id(FK), user_id(FK), role(VARCHAR 20) CHECK IN('owner','admin','member')

### projects
- id(UUID PK), name(VARCHAR 200 NOT NULL), description(TEXT nullable), team_id(FK), created_by(FK users)

### datasets
- id(UUID PK), name(VARCHAR 200 NOT NULL), description(TEXT nullable), project_id(FK), created_by(FK), class_names(TEXT[])

### dataset_versions
- UNIQUE(dataset_id, version). id(UUID PK), dataset_id(FK), version(INT), image_count(INT DEFAULT 0), annotation_format(VARCHAR 20) CHECK IN('yolo_txt','coco_json','voc_xml'), r2_prefix(VARCHAR 500), created_by(FK)

### experiments
- id(UUID PK), project_id(FK), name(VARCHAR 200 NOT NULL), description(TEXT nullable), status(VARCHAR 20) DEFAULT 'created' CHECK('created','running','completed','failed'), dataset_version_id(FK nullable), created_by(FK), started_at(TIMESTAMPTZ nullable), completed_at(TIMESTAMPTZ nullable)

### experiment_params
- UNIQUE(experiment_id, param_key). id(UUID PK), experiment_id(FK), param_key(VARCHAR 100), param_value(TEXT)

## Storage Service (R2)

### R2 연결 설정
- endpoint: https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com
- signature version: s3v4
- bucket: R2_BUCKET_NAME

### R2 Key 구조
```
datasets/{dataset_id}/v{version}/data.yaml
datasets/{dataset_id}/v{version}/images/train/{filename}
datasets/{dataset_id}/v{version}/images/val/{filename}
datasets/{dataset_id}/v{version}/labels/train/{filename}
datasets/{dataset_id}/v{version}/labels/val/{filename}
```

### 구현할 메서드
- upload_file(local_path, r2_key): 파일 업로드
- upload_bytes(data, r2_key, content_type): 바이트 직접 업로드
- download_file(r2_key, local_path): 파일 다운로드
- get_signed_url(r2_key, expires): presigned URL 생성
- download_prefix(prefix, local_dir): prefix 하위 전체 다운로드

## Dataset Upload 처리 흐름

1. zip 파일 업로드 수신 (multipart/form-data)
2. zip 압축 해제
3. 디렉토리 구조 검증: images/ + labels/ (yolo_txt) 또는 _annotations.coco.json
4. 확장자 필터: .jpg, .jpeg, .png
5. annotation class_id가 class_names 범위 내인지 검증
6. 80/20 random split (train/val)
7. R2에 업로드 (images/train/, images/val/, labels/train/, labels/val/)
8. data.yaml 생성: train/val path, nc, names
9. data.yaml R2 업로드
10. image_count 산출
11. dataset_versions row 생성

## CLI 구현 명세

### auth login
- `mlops-cli auth login --server <url>`
- server URL 입력 -> POST {server}/api/v1/auth/login
- username/password prompt
- 성공 시 ~/.mlops/config.json 저장: {server_url, access_token, refresh_token}
- 실패 시 에러 메시지 출력

### dataset pull
- `mlops-cli dataset pull <dataset_id> [--version N] [--output DIR]`
- GET /api/v1/datasets/{id}/versions -> 최신 or 지정 버전
- GET /datasets/{id}/versions/{vId}/download -> signed URL
- requests.streaming으로 zip 다운로드
- 압축 해제 -> output 디렉토리 (기본: ./dataset_{id})
- images/, labels/, data.yaml 로컬에 저장

## Docker Compose

### 서비스
- **postgres**: postgres:16-alpine, 볼륨 pg_data, healthcheck pg_isready
- **api**: backend/ Dockerfile, 포트 8000, command에 alembic upgrade head 포함
- **frontend**: frontend/ Dockerfile, 포트 3000

### 환경변수
- SECRET_KEY, POSTGRES_PASSWORD, R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME

## 검증 기준

- [ ] docker compose up -> http://localhost:8000/docs Swagger 정상
- [ ] 회원가입 + 로그인 -> JWT 발급
- [ ] 프로젝트 생성 -> 목록 조회
- [ ] 데이터셋 zip 업로드 -> R2 images/, labels/ 저장 확인
- [ ] dataset version 생성 -> download signed URL
- [ ] 실험 생성 -> params 저장 -> status 변경
- [ ] CLI login -> ~/.mlops/config.json 생성
- [ ] CLI dataset pull -> 로컬 data.yaml 생성 확인
- [ ] Frontend 모든 페이지 라우팅 정상
