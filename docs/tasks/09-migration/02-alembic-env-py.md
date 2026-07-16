## Spec

- async SQLAlchemy migration 지원
- target_metadata = Base.metadata (from app.models import Base)
- run_migrations_online: create_async_engine(settings.DATABASE_URL) -> connection.run_sync(do_run_migrations)
- offline mode 지원

## Completion

- [ ] `alembic revision --autogenerate -m "init"` -> migration 파일 생성
- [ ] 생성된 SQL에 모든 PoC 테이블 포함
- [ ] `alembic upgrade head` -> 테이블 생성
