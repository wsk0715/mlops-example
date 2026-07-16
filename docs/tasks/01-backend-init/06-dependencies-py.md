## Story

인증된 사용자만 API를 호출할 수 있어야 한다. 토큰이 없거나 만료되면 401을 반환한다.

## Spec

- HTTPBearer security에서 token 추출
- jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
- payload["sub"]로 user_id 추출 -> db.get(User, user_id)
- user 없거나 is_active=False -> 401
- ExpiredSignatureError -> 401
- InvalidTokenError -> 401

## Completion

- [ ] 유효 토큰 -> User 반환
- [ ] 만료 토큰 -> 401
- [ ] 토큰 없음 -> 401
- [ ] 잘못된 토큰 -> 401
