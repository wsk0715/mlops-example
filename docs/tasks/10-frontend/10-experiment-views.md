## Story

실험을 생성하고 하이퍼파라미터를 확인한다. 실험 상태를 수동으로 변경한다.

## Spec

**ExperimentListView.vue**: v-data-table + status chip(color) + create dialog + status filter

**ExperimentDetailView.vue**: params v-table + status badge + 상태 변경 버튼(Start/Complete/Fail)

Status colors: created=grey, running=blue, completed=green, failed=red

## Completion

- [ ] 실험 생성 -> 목록에 추가
- [ ] status 필터 동작
- [ ] 상세 화면 params 테이블
- [ ] Start 버튼 -> status=running
- [ ] Complete 버튼 -> status=completed
