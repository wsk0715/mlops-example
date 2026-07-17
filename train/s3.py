import os
import zipfile
import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

_client = None


def _get_client():
    """환경변수로부터 boto3 S3 클라이언트를 생성하고 재사용합니다."""
    global _client
    if _client is None:
        _client = boto3.client(
            "s3",
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),
            config=Config(signature_version="s3v4"),
        )
    return _client


def get_bucket() -> str:
    """설정된 S3 버킷 이름을 반환합니다."""
    return os.getenv("S3_BUCKET_NAME", "mlops-platform")


def _dataset_key(cfg: dict) -> str:
    """config로부터 데이터셋 S3 키를 생성합니다."""
    pid = cfg["project_id"]
    name = cfg["dataset_name"]
    ver = cfg["dataset_version"]
    return f"{pid}/datasets/{name}/{name}_{ver}.zip"


def _model_key(cfg: dict) -> str:
    """config로부터 모델 업로드 S3 키를 생성합니다."""
    pid = cfg["project_id"]
    eid = cfg.get("experiment_id", "")
    return f"{pid}/models/{eid}/best.pt" if eid else f"{pid}/models/best.pt"


def download_dataset(cfg: dict, dest_dir: str, *, force: bool = False) -> None:
    """config로부터 S3 키를 구성하여 데이터셋을 다운로드하고 압축을 해제합니다.

    dest_dir에 이미 파일이 있으면 다운로드를 생략합니다.
    """
    if not force and os.path.exists(dest_dir) and any(os.scandir(dest_dir)):
        print(f"[SKIP] 데이터셋이 이미 존재합니다: {dest_dir}")
        return

    s3_key = _dataset_key(cfg)
    os.makedirs(dest_dir, exist_ok=True)
    zip_path = dest_dir.rstrip("/\\") + ".zip"

    print(f"[DOWNLOAD] S3에서 다운로드 중... {s3_key}")
    _get_client().download_file(get_bucket(), s3_key, zip_path)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(dest_dir)
    os.remove(zip_path)

    print(f"[OK] 압축 해제 완료: {dest_dir}")


def upload_model(cfg: dict, local_path: str) -> None:
    """config로부터 S3 키를 구성하여 로컬 파일을 업로드합니다."""
    if not os.path.exists(local_path):
        print(f"[WARN] 파일이 없어 업로드를 생략합니다: {local_path}")
        return

    s3_key = _model_key(cfg)
    size_mb = os.path.getsize(local_path) / 1_048_576
    print(f"[UPLOAD] 업로드 중... {local_path} ({size_mb:.2f} MB) -> {s3_key}")
    _get_client().upload_file(Filename=local_path, Bucket=get_bucket(), Key=s3_key)
    print("[OK] 업로드 완료")
