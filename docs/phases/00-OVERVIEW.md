# MLOps Platform Overview

YOLO 기반 객체탐지 MLOps 플랫폼. 소규모 팀(2~5명)이 각자 로컬 GPU로 학습하고, 공유 서버에서 데이터셋/실험/모델을 중앙 관리하며 협업.

> 서버 GPU 불필요. 학습은 팀원 노트북 GPU. 서버는 저장/관리/비교/CPU 서빙.

---

## 기술스택

| 계층 | 기술 | Phase |
|------|------|-------|
| Backend | Python 3.11+ / FastAPI 0.115+ / SQLAlchemy 2.0+ | PoC+ |
| Database | PostgreSQL 16 | PoC+ |
| Storage | Cloudflare R2 (S3 API) | PoC+ |
| Queue | RabbitMQ 3.13 | MVP+ |
| Task Queue | Celery 5.4+ | MVP+ |
| CLI | Click + requests + Ultralytics 8.3+ | PoC+ |
| Frontend | Vue 3 + Vuetify 3 + Vite | PoC+ |
| Auth | PyJWT + bcrypt (id/pw only) | PoC+ |
| Chart | Chart.js + vue-chartjs | MVP+ |
| Container | Docker + Compose V2 | PoC+ |

## 디렉토리 구조

```
mlops-example/
├── docker-compose.yml          # 서버 orchestration
├── .env.example                # 환경변수 템플릿
├── backend/                    # FastAPI 서버
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── alembic.ini + alembic/  # DB migration
│   └── app/
│       ├── main.py             # 앱 생성, 라우터 등록
│       ├── config.py           # Pydantic Settings
│       ├── database.py         # async engine + session
│       ├── dependencies.py     # get_db, get_current_user
│       ├── models/             # SQLAlchemy ORM
│       ├── schemas/            # Pydantic request/response
│       ├── routers/            # API endpoints
│       ├── services/           # 비즈니스 로직
│       └── utils/              # security helpers
├── cli/                        # mlops-cli (로컬 학습 연동)
├── serving/                    # CPU inference server (MVP+)
├── frontend/                   # Vue 3 + Vuetify
└── ref/                        # 명세 문서
    └── phases/
        ├── 00-OVERVIEW.md
        ├── 01-PHASE-0-POC.md
        ├── 02-PHASE-1-MVP.md
        ├── 03-PHASE-2-FEATURES.md
        └── 04-PHASE-3-ADVANCED.md
```

## 공통 API 규칙

| 항목 | 규칙 |
|------|------|
| Base URL | `/api/v1` |
| Content-Type | `application/json` (파일: `multipart/form-data`) |
| 인증 | `Authorization: Bearer <access_token>` |
| Pagination | `?page=1&page_size=20` → `{"items":[],"total":N,"page":1,"page_size":20}` |
| Error | `{"detail":"message"}` with 4xx/5xx |

## 공통 인증

내부 팀 플랫폼. username + password만. 이메일 인증 없음. OAuth 없음.

- `POST /auth/register` → {username, password}
- `POST /auth/login` → {username, password} → {access_token, refresh_token}
- `POST /auth/refresh` → {refresh_token} → {access_token, refresh_token}
- JWT access token: 24h expiry
- JWT refresh token: 30d expiry
- 비밀번호: bcrypt rounds=12, 최소 6자

## 구현 순서

```
Phase 0 ──→ Phase 1 ──→ Phase 2 ──→ Phase 3
  PoC        MVP        추가기능      고도화
```

각 Phase는 이전 Phase 완료 후 시작. Phase 0부터 구현.
