from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.dependencies import get_current_user
from app.models.experiment import Experiment, ExperimentParam
from app.models.user import User

router = APIRouter(prefix="/experiments", tags=["experiments"])


class ExperimentCreate(BaseModel):
    project_id: UUID
    name: str
    description: str | None = None
    params: dict[str, str] = {}


class ExperimentUpdate(BaseModel):
    status: str | None = None
    name: str | None = None


@router.post("", status_code=201)
async def create(
    body: ExperimentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    exp = Experiment(
        project_id=body.project_id,
        name=body.name,
        description=body.description,
        created_by=user.id,
    )
    db.add(exp)
    await db.flush()
    await db.refresh(exp)

    for k, v in body.params.items():
        db.add(ExperimentParam(experiment_id=exp.id, param_key=k, param_value=str(v)))
    await db.commit()
    await db.refresh(exp)

    return {
        "id": exp.id,
        "project_id": exp.project_id,
        "name": exp.name,
        "description": exp.description,
        "status": exp.status,
        "params": body.params,
        "created_at": exp.created_at,
    }


@router.get("")
async def list(
    project_id: str,
    status: str | None = None,
    page: int = 1,
    size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    q = select(Experiment).where(Experiment.project_id == project_id)
    if status:
        q = q.where(Experiment.status == status)
    q = q.offset((page - 1) * size).limit(size).order_by(Experiment.created_at.desc())
    items = (await db.execute(q)).scalars().all()
    return {"items": items, "total": len(items), "page": page, "page_size": size}


@router.get("/{id}")
async def get(id: str, db: AsyncSession = Depends(get_db)):
    exp = await db.get(Experiment, id)
    if not exp:
        raise HTTPException(status_code=404)

    params_rows = (
        await db.execute(
            select(ExperimentParam).where(ExperimentParam.experiment_id == id)
        )
    ).scalars().all()

    return {
        "id": exp.id,
        "name": exp.name,
        "description": exp.description,
        "status": exp.status,
        "params": {p.param_key: p.param_value for p in params_rows},
        "created_at": exp.created_at,
    }


@router.put("/{id}")
async def update(
    id: str,
    body: ExperimentUpdate,
    db: AsyncSession = Depends(get_db),
):
    exp = await db.get(Experiment, id)
    if not exp:
        raise HTTPException(status_code=404)
    if body.status is not None:
        exp.status = body.status
    if body.name is not None:
        exp.name = body.name
    await db.commit()
    await db.refresh(exp)
    return exp
