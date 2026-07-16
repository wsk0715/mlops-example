## Story

팀 아래 프로젝트를 생성한다. 모든 데이터셋/실험/모델은 프로젝트에 속한다.

## Spec

| 컬럼 | 타입 | 제약 |
|------|------|------|
| id | UUID | PK |
| name | VARCHAR(200) | NOT NULL |
| description | TEXT | nullable |
| team_id | UUID | FK teams.id |
| created_by | UUID | FK users.id |

TimestampMixin 상속.

## Completion

- [ ] CREATE TABLE projects migration
- [ ] FK 제약 teams, users 연결 확인
