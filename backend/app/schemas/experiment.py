from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class ExperimentCreate(BaseModel):
    project_id: str
    name: str
    description: str | None = None
    params: dict[str, str] = {}


class ExperimentUpdate(BaseModel):
    status: str | None = None
    name: str | None = None


class ExperimentResponse(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    description: str | None
    status: str
    params: dict = {}
    created_at: datetime
