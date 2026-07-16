## Spec

- SQLAlchemy DeclarativeBase 선언
- TimestampMixin: created_at(TIMESTAMPTZ, server_default=now()), updated_at(TIMESTAMPTZ, server_default=now(), onupdate=now())
- 모든 모델이 TimestampMixin 상속

## Completion

- [ ] Base.metadata.create_all 정상 실행
