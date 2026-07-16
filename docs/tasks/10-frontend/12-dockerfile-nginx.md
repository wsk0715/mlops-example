## Spec

**Dockerfile**: node:20-alpine build -> npm ci -> npm run build -> nginx:alpine serve

**nginx.conf**: SPA fallback (try_files $uri /index.html), /api proxy -> http://api:8000

## Completion

- [ ] docker build -> 정상 빌드
- [ ] 컨테이너 실행 -> 80 포트, /api 프록시
