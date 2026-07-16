## Story

팀원이 서버에 업로드된 데이터셋을 로컬 노트북으로 다운로드한다. 이후 로컬 GPU로 학습할 때 사용한다.

## Spec

**dataset pull**: `mlops-cli dataset pull <dataset_id> [--version N] [--output DIR]`
1. API로 버전 목록 조회 -> 최신 or 지정 버전 선택
2. download signed URL 획득
3. requests.streaming으로 zip 다운로드 -> 압축 해제 -> output 디렉토리
4. images/(train,val) + labels/(train,val) + data.yaml 구조 보존

## Completion

- [ ] mlops-cli dataset pull <id> -> 로컬에 images/ labels/ data.yaml 생성
- [ ] --version N -> 지정 버전 다운로드
- [ ] --output DIR -> 지정 경로에 저장
