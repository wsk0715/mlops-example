## Story

사용자가 로그인하면 JWT를 localStorage에 저장하고 user 정보를 불러온다.

## Spec

- state: user, accessToken
- getters: isLoggedIn
- actions: login(username, pw) -> POST /auth/login -> token 저장
- actions: register(username, pw) -> POST /auth/register
- actions: fetchUser() -> GET /users/me -> user 할당
- actions: logout() -> localStorage clear + state 초기화

## Completion

- [ ] login 후 access_token localStorage 저장 확인
- [ ] fetchUser 후 user state 채워짐
- [ ] logout 후 isLoggedIn == false
