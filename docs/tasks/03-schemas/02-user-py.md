## Spec

- UserCreate: username(str), password(str)
- UserResponse: id(UUID), username(str), is_active(bool), created_at(datetime)
- LoginRequest: username(str), password(str)
- TokenResponse: access_token(str), refresh_token(str), token_type(str) default "bearer"
- RefreshRequest: refresh_token(str)

## Completion

- [ ] Pydantic validation 정상
- [ ] password 최소 길이 검증 (6자)
