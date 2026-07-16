## Story

사용자가 zip 파일로 데이터셋을 업로드하면 압축을 풀고 구조를 검증한 뒤 R2에 저장한다. train/val로 분할하고 data.yaml을 생성한다.

## Spec

입력: files(UploadFile[]), dataset_id(UUID), class_names(list[str]), annotation_format(str)

처리 흐름:
1. zip 압축 해제
2. 디렉토리 구조 검증: images/ + labels/ (yolo_txt) 또는 _annotations.coco.json (coco_json)
3. 확장자 필터 (jpg, jpeg, png)
4. class_id가 class_names 범위 내인지 검증
5. 80/20 random split
6. R2 업로드: images/train/, images/val/, labels/train/, labels/val/
7. data.yaml 생성: train/val 경로, nc, names
8. data.yaml R2 업로드
9. image_count 반환

R2 Key 패턴:
```
datasets/{dataset_id}/v{version}/data.yaml
datasets/{dataset_id}/v{version}/images/train/{filename}
datasets/{dataset_id}/v{version}/images/val/{filename}
datasets/{dataset_id}/v{version}/labels/train/{filename}
datasets/{dataset_id}/v{version}/labels/val/{filename}
```

## Completion

- [ ] zip 업로드 -> R2 images/train/, images/val/, labels/train/, labels/val/ 저장 확인
- [ ] data.yaml nc=class_names 개수 일치
- [ ] annotation_format=yolo_txt -> class_id 검증 동작
- [ ] annotation_format=coco_json -> 변환 후 YOLO txt로 저장
