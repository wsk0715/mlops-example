## Spec

- ExperimentCreate: project_id(str), name(str), description(str optional), params(dict[str,str]) optional
- ExperimentUpdate: status(str optional), name(str optional)
- ExperimentResponse: id(UUID), project_id(UUID), name(str), description(str optional), status(str), params(dict), created_at(datetime)

## Completion

- [ ] POST /experiments 에서 params 가 dict[str,str]로 정상 수신
