from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.dataset import Dataset, DatasetVersion
from app.models.user import User
from app.services.dataset_service import handle_upload
from app.services.storage_service import storage

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("", status_code=201)
async def create(
    name: str = Form(...),
    project_id: str = Form(...),
    class_names: str = Form(""),
    annotation_format: str = Form("yolo_txt"),
    files: list[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    cls_list = [c.strip() for c in class_names.split(",") if c.strip()]
    ds = Dataset(
        name=name,
        project_id=project_id,
        class_names=cls_list,
        created_by=user.id,
    )
    db.add(ds)
    await db.flush()
    await db.refresh(ds)

    image_count = handle_upload(files, ds.id, cls_list, annotation_format)

    version = DatasetVersion(
        dataset_id=ds.id,
        version=1,
        image_count=image_count,
        annotation_format=annotation_format,
        r2_prefix=f"datasets/{ds.id}/v1/",
        created_by=user.id,
    )
    db.add(version)
    await db.commit()
    await db.refresh(ds)
    return ds


@router.get("")
async def list(
    project_id: str,
    page: int = 1,
    size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    items = (
        await db.execute(
            select(Dataset)
            .where(Dataset.project_id == project_id)
            .offset((page - 1) * size)
            .limit(size)
        )
    ).scalars().all()
    return {"items": items, "total": len(items), "page": page, "page_size": size}


@router.get("/{id}")
async def get(id: str, db: AsyncSession = Depends(get_db)):
    ds = await db.get(Dataset, id)
    if not ds:
        raise HTTPException(status_code=404)
    return ds


@router.get("/{id}/versions")
async def list_versions(id: str, db: AsyncSession = Depends(get_db)):
    items = (
        await db.execute(
            select(DatasetVersion)
            .where(DatasetVersion.dataset_id == id)
            .order_by(DatasetVersion.version.desc())
        )
    ).scalars().all()
    return {"items": items, "total": len(items)}


@router.get("/{id}/versions/{vId}/download")
async def download(id: str, vId: str, db: AsyncSession = Depends(get_db)):
    ver = await db.get(DatasetVersion, vId)
    if not ver:
        raise HTTPException(status_code=404)
    url = storage.get_signed_url(f"{ver.r2_prefix}data.yaml")
    return {"signed_url": url, "filename": f"dataset_v{ver.version}.zip"}
