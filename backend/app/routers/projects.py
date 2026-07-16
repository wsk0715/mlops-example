from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.project import Project
from app.models.user import User
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    team_id: str


@router.post("", status_code=201)
async def create(
    body: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    proj = Project(
        name=body.name,
        description=body.description,
        team_id=body.team_id,
        created_by=user.id,
    )
    db.add(proj)
    await db.commit()
    await db.refresh(proj)
    return proj


@router.get("")
async def list(
    page: int = 1,
    size: int = 20,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    total = await db.scalar(select(func.count(Project.id)))
    items = (
        await db.execute(select(Project).offset((page - 1) * size).limit(size))
    ).scalars().all()
    return PaginatedResponse(items=items, total=total or 0, page=page, page_size=size)


@router.get("/{id}")
async def get(id: str, db: AsyncSession = Depends(get_db)):
    proj = await db.get(Project, id)
    if not proj:
        raise HTTPException(status_code=404)
    return proj


@router.put("/{id}")
async def update(
    id: str,
    body: ProjectCreate,
    db: AsyncSession = Depends(get_db),
):
    proj = await db.get(Project, id)
    if not proj:
        raise HTTPException(status_code=404)
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(proj, k, v)
    await db.commit()
    await db.refresh(proj)
    return proj


@router.delete("/{id}", status_code=204)
async def delete(id: str, db: AsyncSession = Depends(get_db)):
    proj = await db.get(Project, id)
    if not proj:
        raise HTTPException(status_code=404)
    await db.delete(proj)
    await db.commit()
