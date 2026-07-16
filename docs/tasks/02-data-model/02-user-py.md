## Spec

| 컬럼 | 타입 | 제약 |
|------|------|------|
| id | UUID | PK, default uuid4 |
| username | VARCHAR(50) | UNIQUE NOT NULL |
| hashed_password | VARCHAR(255) | NOT NULL |
| is_active | BOOLEAN | DEFAULT true |

TimestampMixin 상속.

## Completion

- [ ] alembic autogenerate -> CREATE TABLE users
- [ ] username UNIQUE 제약 확인
