## Story

개발자가 프로젝트를 클론받고 pip install로 의존성을 한 번에 설치할 수 있어야 한다.

## Spec

- FastAPI + SQLAlchemy(async) + asyncpg + Alembic + boto3 + PyJWT + bcrypt + python-multipart + pydantic-settings
- pip install . 로 설치 가능
- 의존성 버전 고정

## Completion

- [ ] pip install . -> uvicorn app.main:app 기동
