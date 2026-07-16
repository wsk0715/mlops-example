# MLOps Platform (YOLO 기반 객체탐지)

소규모 팀이 로컬 GPU로 YOLO 모델을 학습하고, 공유 서버에서 데이터셋/실험/모델을 중앙 관리/협업하기 위한 MLOps 플랫폼.

---

## 기술스택

| 계층 | 기술 |
|------|------|
| Backend | Python 3.11+ / FastAPI 0.115+ / SQLAlchemy 2.0+ |
| Database | PostgreSQL 16 |
| Storage | Cloudflare R2 (S3 API) |
| Frontend | Vue 3 + Vuetify 3 + Vite |
| Auth | PyJWT + bcrypt (id/pw only) |
| CLI | Click + requests + Ultralytics (로컬 학습 연동) |
| Container | Docker + Compose V2 |

---

## 프로젝트 구조

```
mlops-example/
├── docker-compose.yml          # 서버 orchestration
├── backend/                     # FastAPI 서버
│   └── app/
│       ├── models/             # SQLAlchemy ORM
│       ├── schemas/            # Pydantic request/response
│       ├── routers/            # API endpoints
│       └── services/           # 비즈니스 로직 (R2, dataset, auth)
├── cli/                        # mlops-cli (로컬 학습 연동)
│   └── mlops_cli/
│       ├── commands/           # auth, dataset, experiment, model
│       └── services/           # api_client, trainer
├── serving/                    # CPU inference server
└── frontend/                   # Vue 3 + Vuetify 대시보드
```

---

## 시작하기

### 사전 요구사항

- Docker + Compose V2
- Cloudflare R2 버킷 (또는 S3 호환 스토리지)

### 설치 및 실행

```bash
# 1. 환경변수 설정
cp .env.example .env
# .env 파일 수정 (R2 계정 정보, SECRET_KEY)

# 2. 서버 실행
docker compose up -d

# 3. 접속
# Frontend: http://localhost:3000
# API Swagger: http://localhost:8000/docs
```

### CLI 설치

```bash
pip install cli/
mlops-cli auth login --server http://localhost:8000
```

---

## Phase별 구현 로드맵

| Phase | 목표 |
|-------|------|
| PoC | 데이터셋 업로드 -> 실험 생성 -> CLI 다운로드 |
| MVP | 로컬 GPU 학습 -> 메트릭 Push -> Model Registry -> CPU Serving |
| 추가기능 | Annotation Viewer, Dashboard, Team 관리 |
| 고도화 | GPU 서버 학습(선택), Sweep, CI/CD, Drift 감지 |

---

## 라이선스

Internal project.
