import os
from pathlib import Path
from ultralytics import YOLO

project_path = Path("./").resolve()
dataset_path = Path("./dataset").resolve()

model = YOLO("yolov8n.pt")
model.train(
    project=str(project_path),
    data=str(dataset_path / "data.yaml"),
    imgsz=416,
    batch=32,
    epochs=50,
    device=0,
    workers=0,
)
