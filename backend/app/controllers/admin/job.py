# routes/job.py
from fastapi import APIRouter, Depends, Path, Query, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import job as schemas
from ...services import job as services
from ...models import users as models
from ...utils import jwt
from ...configs.database import get_db
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/admin/job", response_model=schemas.Job, status_code=201)
@limiter.limit("20/minute")
async def create_job(
    request: Request,
    job: schemas.JobCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_job(db, job)

@router.get("/admin/job/{job_id}", response_model=schemas.Job)
@limiter.limit("20/minute")
async def get_job_by_id(
    request: Request,
    job_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_job_by_id(db, job_id)

@router.get("/admin/job/user/{user_id}", response_model=List[schemas.Job])
@limiter.limit("20/minute")
async def get_jobs_by_user_id(
    request: Request,
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_jobs_by_user_id(db, user_id)

@router.put("/admin/job/{job_id}", response_model=schemas.Job)
@limiter.limit("20/minute")
async def update_job(
    request: Request,
    job: schemas.JobUpdate = Query(...),
    job_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.update_job(db, job_id, job)

@router.delete("/admin/job/{job_id}")
@limiter.limit("20/minute")
async def delete_job(
    request: Request,
    job_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.delete_job(db, job_id)

@router.get("/admin/job", response_model=List[schemas.Job])
@limiter.limit("20/minute")
async def get_all_jobs(
    request: Request,
    skip: int = Query(0),
    limit: int = Query(200),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_all_jobs(db, skip=skip, limit=limit)
