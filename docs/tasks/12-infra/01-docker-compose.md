## Spec

postgres + api + frontend 3개 서비스.

| 서비스 | 이미지 | 포트 | 비고 |
|--------|--------|------|------|
| postgres | postgres:16-alpine | | 볼륨 pg_data, healthcheck pg_isready |
| api | backend/ Dockerfile | 8000 | 명령어: alembic upgrade head && uvicorn, 환경변수 연결 |
| frontend | frontend/ Dockerfile | 3000 | depends_on api |

환경변수: SECRET_KEY, POSTGRES_PASSWORD, R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME

## Completion

- [ ] docker compose up -d -> postgres + api + frontend 정상 기동
- [ ] http://localhost:3000 접속
- [ ] http://localhost:8000/docs 접속
