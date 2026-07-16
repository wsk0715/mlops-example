## Spec

- create_access_token(user_id: str) -> str: JWT, sub=user_id, exp=24h
- create_refresh_token(user_id: str) -> str: JWT, sub=user_id, type=refresh, exp=30d
- decode_token(token: str) -> dict: raise ExpiredSignatureError / InvalidTokenError

## Completion

- [ ] create_access_token("uuid") -> 유효한 JWT 문자열
- [ ] decode_token(token)["sub"] == "uuid"
- [ ] 만료 토큰 decode -> jwt.ExpiredSignatureError
