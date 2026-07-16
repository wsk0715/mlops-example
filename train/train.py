import json, os, zipfile
from pathlib import Path
from dotenv import load_dotenv
import boto3
from botocore.config import Config
from ultralytics import YOLO

HERE = Path(__file__).parent
load_dotenv(HERE / ".env")

S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "mlops-platform")

project_path = HERE / "yolo" / "runs"
dataset_path = HERE / "dataset"
config_file = HERE / "config.json"


def _s3():
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=S3_ACCESS_KEY_ID,
        aws_secret_access_key=S3_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
    )


def load_config():
    """config.json 파일이 있으면 읽어오고, 없으면 기본값으로 생성하는 함수"""
    if not config_file.exists():
        default = {
            "dataset_name": "chess-pieces",
            "dataset_version": "v1",
            "imgsz": 416,
            "batch": 32,
            "epochs": 50,
            "lr0": 0.01,
            "optimizer": "auto",
        }

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4, ensure_ascii=False)

        print(f"💡 {config_file.name} 없음 → 기본값 생성")

    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


def download_dataset(config):
    """필요한 데이터셋을 중앙 저장소로부터 다운로드하는 함수"""
    dataset_dir = dataset_path
    if dataset_dir.exists() and any(dataset_dir.iterdir()):
        print("📊 데이터셋 이미 존재 → 스킵")
        return

    name = config.get("dataset_name")
    ver = config.get("dataset_version")
    if not name or not ver:
        return

    key = f"datasets/{name}/{name}_{ver}.zip"

    print(f"📥 S3에서 데이터셋 다운로드... ({key})")

    dataset_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dataset_dir.with_suffix(".zip")
    _s3().download_file(S3_BUCKET_NAME, key, str(zip_path))

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(dataset_dir)
    zip_path.unlink()

    print("✅ 데이터셋 다운로드 완료!")


def upload_result(config):
    """학습 결과물을 중앙 저장소에 업로드하는 함수"""
    runs_dir = project_path
    best = runs_dir / "train" / "weights" / "best.pt"
    if not best.exists():
        print(f"⚠️  best.pt 없음: {best}")
        return

    exp_id = config.get("experiment_id", "unknown")
    key = f"models/{exp_id}/best.pt"

    print("🚀 가중치 업로드 중...")

    _s3().upload_file(Filename=str(best), Bucket=S3_BUCKET_NAME, Key=key)

    print(f"✅ 업로드 완료! ({os.path.getsize(best) / 1024**2:.2f} MB)")


def main():
    """설정 파일을 읽어서 YOLO 학습을 실행하는 메인 함수"""
    # config 로드
    config = load_config()

    # 데이터셋 다운로드
    download_dataset(config)

    # 모델 설정 & 학습 시작
    model = YOLO("yolov8n.pt")
    model.train(
        project=str(project_path),
        data=str(dataset_path / "data.yaml"),
        imgsz=config["imgsz"],
        batch=config["batch"],
        epochs=config["epochs"],
        optimizer=config["optimizer"],
        lr0=config["lr0"],
        device=0,
        workers=0,
        amp=True,
    )

    # 학습 결과 업로드
    upload_result(config)


# 시작점 선언 (Windows 환경 필요)
if __name__ == "__main__":
    main()
