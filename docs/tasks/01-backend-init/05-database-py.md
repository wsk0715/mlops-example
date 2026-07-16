## Spec

- create_async_engine(settings.DATABASE_URL)
- async_session = async_sessionmaker(AsyncSession)
- get_db() async generator -> Depends에서 사용 가능하도록

## Completion

- [ ] route에서 Depends(get_db) 호출 -> 세션 정상 반환
- [ ] PostgreSQL 연결 성공
