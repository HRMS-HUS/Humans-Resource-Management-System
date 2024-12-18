from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import job as schemas
from ..controllers.manager import job as controllers
from ..models import users as models
from ..services import users
from ..database import get_db
from typing import List

router = APIRouter(prefix="/api", tags=["job"])

@router.post(
    "/job",
    response_model=schemas.JobCreate,
    status_code=status.HTTP_201_CREATED,
)
async def create_job(
    job: schemas.JobCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):
    return await controllers.create_job(db, job)

@router.get("/job/{job_id}", response_model=schemas.Job)
async def get_job_by_id(
    job_id: str = Path(..., description="Job ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):
    return await controllers.get_job_by_id_controller(db, job_id)

@router.get("/job/user/{user_id}", response_model=List[schemas.Job])
async def get_jobs_by_user_id(
    user_id: str = Path(..., description="User ID to retrieve jobs"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):
    return await controllers.get_jobs_by_user_id_controller(db, user_id)

@router.put("/job/{job_id}", response_model=schemas.Job)
async def update_job(
    job: schemas.JobCreate = Query(...),
    job_id: str = Path(..., description="Job ID to update"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):
    return await controllers.update_job_controller(db, job_id, job)

@router.delete("/job/{job_id}")
async def delete_job(
    job_id: str = Path(..., description="Job ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):
    return await controllers.delete_job_controller(db, job_id)

@router.get("/job", response_model=List[schemas.Job])
async def get_all_jobs(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(users.get_current_admin),
):
    return await controllers.get_all_jobs_controller(db, skip=skip, limit=limit)
