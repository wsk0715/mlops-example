## Spec

- cli.py: Click group "mlops-cli" -> subcommands: auth, dataset
- __main__.py: python -m mlops_cli 지원
- config.py: ~/.mlops/config.json 읽기/쓰기 (server_url, access_token, refresh_token)

## Completion

- [ ] mlops-cli --help -> auth, dataset 표시
- [ ] python -m mlops_cli --help -> 동일
