## Spec

- FastAPI 앱 생성 (title="MLOps Platform")
- CORS 미들웨어: allow_origins=["*"]
- 라우터 등록: auth, projects, datasets, experiments prefix=/api/v1
- Exception handler 등록 (500, 422)
- .env 파일 로드

## Completion

- [ ] GET /docs -> Swagger UI 정상 렌더링
- [ ] 모든 라우터 응답 확인
