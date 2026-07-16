import os

import boto3
from botocore.config import Config

from app.config import settings


class R2StorageService:
    def __init__(self):
        endpoint = f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
        )
        self.bucket = settings.R2_BUCKET_NAME

    def upload_file(self, local_path: str, r2_key: str):
        self.client.upload_file(local_path, self.bucket, r2_key)

    def upload_bytes(self, data: bytes, r2_key: str, content_type: str | None = None):
        kwargs = {"ContentType": content_type} if content_type else {}
        self.client.put_object(Bucket=self.bucket, Key=r2_key, Body=data, **kwargs)

    def download_file(self, r2_key: str, local_path: str):
        self.client.download_file(self.bucket, r2_key, local_path)

    def get_signed_url(self, r2_key: str, expires: int = 3600) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": r2_key},
            ExpiresIn=expires,
        )

    def download_prefix(self, prefix: str, local_dir: str):
        paginator = self.client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                rel = os.path.relpath(obj["Key"], prefix)
                dest = os.path.join(local_dir, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                self.client.download_file(self.bucket, obj["Key"], dest)


storage = R2StorageService()
