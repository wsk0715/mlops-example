## Spec

- APIClient(base_url, access_token, refresh_token)
- _request(method, path, **kwargs) -> 자동 401 refresh 후 재시도
- GET/POST/PUT/DELETE 지원

## Completion

- [ ] POST /auth/login 성공
- [ ] 401 -> refresh -> 재시도 성공
