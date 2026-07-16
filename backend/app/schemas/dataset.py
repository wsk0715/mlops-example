from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class DatasetCreate(BaseModel):
    name: str
    description: str | None = None
    project_id: str
    class_names: list[str] = Field(default_factory=list)
    annotation_format: str = "yolo_txt"


class DatasetResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    project_id: UUID
    class_names: list[str]
    created_at: datetime


class DatasetVersionResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    version: int
    image_count: int
    annotation_format: str
    r2_prefix: str
    created_at: datetime


class DownloadResponse(BaseModel):
    signed_url: str
    filename: str
