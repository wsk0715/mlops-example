from pathlib import Path

import config
import s3
import train

HERE = Path(__file__).resolve().parent
PROJECT_DIR = str(HERE / "yolo" / "runs")
DATASET_DIR = HERE / "dataset"


def main():
    """학습 파이프라인을 실행합니다:
    설정 로드 -> 데이터셋 다운로드 -> 학습 -> 결과 업로드
    """
    cfg = config.load()

    s3.download_dataset(cfg, str(DATASET_DIR))
    train.run_training(cfg, str(DATASET_DIR / "data.yaml"), PROJECT_DIR)
    s3.upload_model(cfg, train.best_weight_path(PROJECT_DIR))


if __name__ == "__main__":
    main()
