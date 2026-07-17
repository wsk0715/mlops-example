import json
from pathlib import Path

HERE = Path(__file__).parent
CONFIG_FILE = HERE / "config.json"

DEFAULT_CONFIG = {
    "project_id": "",
    "experiment_id": "",
    "dataset_name": "chess-pieces",
    "dataset_version": "v1",
    "weights": "yolov8n.pt",
    "imgsz": 416,
    "batch": 32,
    "epochs": 5,
    "lr0": 0.01,
    "optimizer": "auto",
}


def load() -> dict:
    """config.json을 읽어 반환합니다. 없으면 기본값을 그대로 반환합니다."""
    if not CONFIG_FILE.exists():
        return dict(DEFAULT_CONFIG)

    with open(CONFIG_FILE, encoding="utf-8") as f:
        cfg = json.load(f)

    for k, v in DEFAULT_CONFIG.items():
        cfg.setdefault(k, v)

    return cfg
