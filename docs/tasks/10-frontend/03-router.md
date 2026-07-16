## Spec

| Path | View | Guard |
|------|------|-------|
| /login | LoginView | public |
| /register | RegisterView | public |
| / | DashboardView | auth |
| /projects/:id | ProjectDetailView | auth |
| /projects/:id/datasets | DatasetListView | auth |
| /projects/:id/datasets/:did | DatasetDetailView | auth |
| /projects/:id/experiments | ExperimentListView | auth |
| /projects/:id/experiments/:eid | ExperimentDetailView | auth |

beforeEach guard: token 없으면 /login redirect.

## Completion

- [ ] 로그인 안 함 -> /login 리다이렉트
- [ ] 로그인 상태 -> 모든 라우트 접근 가능
- [ ] 존재하지 않는 경로 -> 404 or /redirect
