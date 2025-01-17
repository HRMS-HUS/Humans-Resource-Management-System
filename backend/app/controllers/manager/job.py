from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import job as schemas
from ...services import job as services
from ...services import userPersonalInfo as personal_info_services
from ...services import department as dept_services
from ...models import users as models
from ...configs.database import get_db
from ...utils import jwt
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

async def validate_user_in_department(db: AsyncSession, user_id: str, manager_id: str):
    # Get manager's department
    dept = await dept_services.get_department_by_manager_id(db, manager_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager has no associated department"
        )
    
    # Get user's department
    user_info = await personal_info_services.get_user_personal_info_by_user_id(db, user_id)
    if user_info.department_id != dept.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User not in manager's department"
        )
    return dept

@router.post("/manager/job", response_model=schemas.Job)
@limiter.limit("5/minute")
async def create_job(
    request: Request,
    job: schemas.JobCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    await validate_user_in_department(db, job.user_id, current_user.user_id)
    return await services.create_job(db, job)

@router.get("/manager/job/{job_id}", response_model=schemas.Job)
@limiter.limit("10/minute")
async def get_job(
    request: Request,
    job_id: str = Path(..., description="Job ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    job = await services.get_job_by_id(db, job_id)
    await validate_user_in_department(db, job.user_id, current_user.user_id)
    return job

@router.get("/manager/job/user/{user_id}", response_model=List[schemas.Job])
@limiter.limit("10/minute")
async def get_user_jobs(
    request: Request,
    user_id: str = Path(..., description="User ID to retrieve jobs"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    await validate_user_in_department(db, user_id, current_user.user_id)
    return await services.get_jobs_by_user_id(db, user_id)

@router.put("/manager/job/{job_id}", response_model=schemas.Job)
@limiter.limit("5/minute")
async def update_job(
    request: Request,
    job_id: str = Path(..., description="Job ID to update"),
    job: schemas.JobUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    existing_job = await services.get_job_by_id(db, job_id)
    await validate_user_in_department(db, existing_job.user_id, current_user.user_id)
    return await services.update_job(db, job_id, job)

@router.delete("/manager/job/{job_id}")
@limiter.limit("3/minute")
async def delete_job(
    request: Request,
    job_id: str = Path(..., description="Job ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    existing_job = await services.get_job_by_id(db, job_id)
    await validate_user_in_department(db, existing_job.user_id, current_user.user_id)
    return await services.delete_job(db, job_id)
