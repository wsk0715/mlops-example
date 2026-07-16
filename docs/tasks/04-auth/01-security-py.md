## Spec

- hash_password(password: str) -> str: bcrypt.gensalt(rounds=12)로 해싱
- verify_password(password: str, hashed: str) -> bool

## Completion

- [ ] hash_password("test123") != plain text
- [ ] verify_password("test123", hash) == True
- [ ] verify_password("wrong", hash) == False
