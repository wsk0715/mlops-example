## Story

팀 리더가 프로젝트를 생성하고 팀원들이 조회/수정한다.

## Spec

| Method | Path | Description |
|--------|------|-------------|
| POST | /projects | {name, description, team_id} -> 201 |
| GET | /projects | ?page=1&size=20 -> PaginatedResponse |
| GET | /projects/{id} | detail |
| PUT | /projects/{id} | partial update |
| DELETE | /projects/{id} | 204 |

## Completion

- [ ] POST -> 201 + project 반환
- [ ] GET /projects -> 페이지네이션 정상
- [ ] GET /projects/{id} -> 404
- [ ] DELETE -> 204
