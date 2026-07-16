## Story

사용자가 회원가입하고 로그인한다. JWT를 받아 이후 모든 API 요청에 사용한다.

## Spec

| Method | Path | Request | Response | Error |
|--------|------|---------|----------|-------|
| POST | /auth/register | {username, password} | 201 UserResponse | 409 중복 |
| POST | /auth/login | {username, password} | 200 TokenResponse | 401 |
| POST | /auth/refresh | {refresh_token} | 200 TokenResponse | 401 |
| GET | /users/me | - | 200 UserResponse | 401 |

## Completion

- [ ] POST /auth/register -> 201
- [ ] 중복 username -> 409
- [ ] POST /auth/login -> access_token + refresh_token
- [ ] 잘못된 비밀번호 -> 401
- [ ] POST /auth/refresh -> 새 토큰
- [ ] GET /users/me -> 사용자 정보
