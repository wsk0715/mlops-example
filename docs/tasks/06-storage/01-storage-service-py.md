## Spec

R2(S3 호환) 스토리지 서비스. 로컬 파일/바이트를 R2에 업로드하고 signed URL 발급.

| 메서드 | 인자 | 설명 |
|--------|------|------|
| upload_file | local_path, r2_key | 로컬 파일 업로드 |
| upload_bytes | data, r2_key, content_type | 메모리 데이터 직접 업로드 |
| download_file | r2_key, local_path | R2 -> 로컬 파일 |
| get_signed_url | r2_key, expires(초) | presigned GET URL 발급 |
| download_prefix | prefix, local_dir | prefix 하위 전체 다운로드 |

연결 설정:
- endpoint: https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com
- signature_version: s3v4
- bucket: R2_BUCKET_NAME

## Completion

- [ ] upload_file -> R2 객체 생성 확인
- [ ] get_signed_url -> HTTP 200 응답 URL
- [ ] download_prefix -> 로컬 디렉토리에 구조 보존 다운로드
