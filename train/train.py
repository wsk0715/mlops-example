from pathlib import Path
from ultralytics import YOLO


def run_training(cfg: dict, data_yaml: str, project_dir: str) -> None:
    """config에서 하이퍼파라미터와 모델명을 꺼내 YOLO 학습을 실행합니다.

    결과는 project_dir/train/weights/ 아래에 저장됩니다.
    """
    weights = cfg.get("weights", "yolov8n.pt")
    print(f"[LOAD] YOLO 모델 로딩: {weights}")
    model = YOLO(weights)

    print(
        f"[TRAIN] 학습 시작 "
        f"(imgsz={cfg['imgsz']}, batch={cfg['batch']}, epochs={cfg['epochs']})"
    )
    model.train(
        project=project_dir,
        data=data_yaml,
        imgsz=cfg["imgsz"],
        batch=cfg["batch"],
        epochs=cfg["epochs"],
        optimizer=cfg.get("optimizer", "auto"),
        lr0=cfg.get("lr0", 0.01),
        device=0,
        workers=0,
        amp=True,
    )
    print(f"[OK] 학습 완료 — 결과 저장 위치: {project_dir}")


def best_weight_path(project_dir: str) -> str:
    """학습 완료 후 최고 성능 가중치 파일(best.pt)의 절대 경로를 반환합니다."""
    path = Path(project_dir) / "train" / "weights" / "best.pt"
    if not path.exists():
        raise FileNotFoundError(f"best.pt를 찾을 수 없습니다: {path}")
    return str(path.resolve())
