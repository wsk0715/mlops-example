## Story

사용자가 CLI로 플랫폼에 로그인한다. 입력한 JWT를 로컬에 저장하여 이후 모든 CLI 명령어에서 재사용한다.

## Spec

**auth login**: `--server <url>` 옵션 -> username/password prompt -> POST /auth/login -> ~/.mlops/config.json 저장
**auth logout**: config.json 삭제

## Completion

- [ ] mlops-cli auth login --server http://localhost:8000 -> ~/.mlops/config.json 생성
- [ ] config.json에 access_token, refresh_token 포함
- [ ] mlops-cli auth logout -> config.json 삭제
