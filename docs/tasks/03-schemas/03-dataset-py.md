## Spec

- DatasetCreate: name(str), description(str optional), project_id(str), class_names(list[str] optional), annotation_format(str) default "yolo_txt"
- DatasetResponse: id(UUID), name(str), description(str optional), project_id(UUID), class_names(list[str]), created_at(datetime)
- DatasetVersionResponse: id(UUID), dataset_id(UUID), version(int), image_count(int), annotation_format(str), r2_prefix(str), created_at(datetime)
- DownloadResponse: signed_url(str), filename(str)

## Completion

- [ ] DatasetCreate annotation_format validation (yolo_txt/coco_json/voc_xml 중 하나)
