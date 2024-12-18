from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ...services import users as users_service
from ...schemas import job as schemas
from ...services import job as services
from ...database import get_db
from ...models import users as model_user

async def create_job(
    job: schemas.JobCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current: model_user.Users = Depends(users_service.get_current_admin),
):
    try:
        return await services.create_job(db, job)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating job: {str(e)}",
        )

async def get_job_by_id_controller(
    db: AsyncSession, job_id: str
):
    try:
        return await services.get_job_by_id(db, job_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving job: {str(e)}",
        )

async def get_jobs_by_user_id_controller(db: AsyncSession, user_id: str):
    try:
        return await services.get_jobs_by_user_id(db, user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving jobs: {str(e)}",
        )

async def update_job_controller(
    db: AsyncSession, job_id: str, job: schemas.JobCreate
):
    try:
        return await services.update_job(db, job_id, job)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating job: {str(e)}",
        )

async def delete_job_controller(db: AsyncSession, job_id: str):
    try:
        return await services.delete_job(db, job_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting job: {str(e)}",
        )

async def get_all_jobs_controller(
    db: AsyncSession, skip: int = 0, limit: int = 100
):
    try:
        return await services.get_all_jobs(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving jobs: {str(e)}",
        )
