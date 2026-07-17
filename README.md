# MLOps Platform (YOLO 기반 객체탐지)

소규모 팀이 로컬 GPU로 YOLO 모델을 학습하고, 공유 서버에서 데이터셋/실험/모델을 중앙 관리/협업하는 MLOps 플랫폼.

> 서버 GPU 불필요. 학습은 팀원 노트북 GPU. 서버는 저장/관리/비교/CPU 서빙.

---

## 기술스택

| 계층 | 기술 |
|------|------|
| Backend | Python 3.11+ / FastAPI 0.115+ / SQLAlchemy 2.0+ |
| Database | PostgreSQL 16 |
| Storage | Cloudflare R2 (S3 API) / MinIO (개발대체) |
| Frontend | Vue 3 + Vuetify 3 + Vite |
| CLI | Python Click (로컬 학습 연동) |
| Container | Docker + Compose V2 |

---

## 시작하기 (로컬 개발)

### 사전 준비

- Docker Desktop
- PowerShell or bash

### Step 1: .env 파일 설정

```bash
cp .env.example .env
```

`.env` 파일을 열어 SECRET_KEY 변경 (아무 32자 문자열). R2 정보는 빈칸으로 둬도 됨.

### Step 2: 전체 서비스 실행

```bash
docker compose up -d
```

postgres + api + frontend 3개 컨테이너가 자동 빌드 및 실행된다.

### Step 3: 정상 동작 확인

브라우저에서 http://localhost:8000/docs 열면 Swagger UI가 보여야 함.

curl로 API 테스트:

```bash
# 회원가입
curl -X POST http://localhost:8000/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"alice\",\"password\":\"test123\"}"

# 로그인 (토큰 발급)
curl -X POST http://localhost:8000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"alice\",\"password\":\"test123\"}"

# 프로젝트 생성
curl -X POST http://localhost:8000/api/v1/projects ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer [access_token]" ^
  -d "{\"name\":\"test-project\",\"team_id\":\"00000000-0000-0000-0000-000000000000\"}"
```

### Step 4: 프론트엔드 접속

```bash
cd frontend
npm install
npm run dev
```

http://localhost:3000 접속.

### 전체 중단

```bash
docker compose down
```

---

## Phase별 로드맵

| Phase | 목표 |
|-------|------|
| PoC | 데이터셋 업로드 -> 실험 생성 -> CLI 다운로드 |
| MVP | 로컬 GPU 학습 -> 메트릭 Push -> Model Registry -> CPU Serving |
| 추가기능 | Annotation Viewer, Dashboard, Team 관리 |
| 고도화 | GPU 서버 학습(선택), Sweep, CI/CD |

상세 명세: [ref/phases/](ref/phases/)
