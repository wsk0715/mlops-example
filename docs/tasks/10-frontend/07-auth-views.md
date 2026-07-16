## Story

사용자가 플랫폼에 로그인하거나 회원가입한다.

## Spec

**LoginView.vue**: username + password 폼 -> login store -> / redirect

**RegisterView.vue**: username + password 폼 -> register store -> /login redirect

둘 다 Vuetify v-text-field + v-btn. 에러 메시지 표시.

## Completion

- [ ] 로그인 성공 -> / 이동
- [ ] 로그인 실패 -> 에러 메시지
- [ ] 회원가입 성공 -> /login 이동
