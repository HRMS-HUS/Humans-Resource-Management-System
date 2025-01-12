# routes/job.py
from fastapi import APIRouter, Depends, Path, Query, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import job as schemas
from ...services import job as services
from ...models import users as models
from ...utils import jwt
from ...configs.database import get_db
from typing import List

router = APIRouter()

@router.post(
    "/me/job",
    response_model=schemas.Job,
    status_code=status.HTTP_201_CREATED,
)
async def create_job_me(
    job: schemas.JobCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    if job.user_id and job.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create jobs for other users"
        )
    job.user_id = current_user.user_id
    return await services.create_job(db, job)

@router.put(
    "/me/job/{job_id}",
    response_model=schemas.Job,
)
async def update_job_me(
    job_id: str = Path(..., description="Job ID to update"),
    job: schemas.JobUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    existing_job = await services.get_job_by_id(db, job_id)
    if not existing_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    if existing_job.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this job"
        )
    return await services.update_job(db, job_id, job)

@router.delete("/me/job/{job_id}")
async def delete_job_me(
    job_id: str = Path(..., description="Job ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    job = await services.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    if job.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this job"
        )
    return await services.delete_job(db, job_id)

@router.get("/me/job", response_model=List[schemas.Job])
async def get_current_user_job(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    return await services.get_jobs_by_user_id(
        db, current_user.user_id
    )