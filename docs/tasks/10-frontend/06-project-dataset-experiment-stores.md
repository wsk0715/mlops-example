## Spec

**projectsStore**: state(projects[], current), actions(fetch, create, getById)

**datasetsStore**: state(datasets[], current, versions[]), actions(fetch, upload, getById, fetchVersions)

**experimentsStore**: state(experiments[], current), actions(fetch, create, getById, updateStatus)

## Completion

- [ ] 각 store action 호출 -> API 응답 state에 저장
- [ ] create 후 목록에 추가 확인
