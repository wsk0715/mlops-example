## Story

데이터셋을 업로드하고 목록을 조회한다. 상세 화면에서 버전 정보를 확인한다.

## Spec

**DatasetListView.vue**: v-data-table + upload dialog (name, classes, zip file)

**DatasetDetailView.vue**: metadata 표시 + version history table + download 버튼

## Completion

- [ ] 업로드 다이얼로그 -> POST /datasets (multipart)
- [ ] 데이터셋 목록 v-data-table
- [ ] 상세 화면 버전 리스트
- [ ] Download 버튼 -> signed URL -> 새 탭 열기
