# services/job.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from fastapi import HTTPException, status
from ..models import job as models
from ..schemas import job as schemas
from typing import List, Optional
from ..utils.redis_lock import DistributedLock
from ..utils.logger import logger
from ..services import users as user_service

class DatabaseOperationError(Exception):
    pass

async def _validate_user_exists(db: AsyncSession, user_id: str):
    try:
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while validating user"
        )

async def create_job(db: AsyncSession, job: schemas.JobCreate):
    async with DistributedLock(f"job:user:{job.user_id}"):
        try:
            await _validate_user_exists(db, job.user_id)
            db_job = models.Job(**job.dict())
            db.add(db_job)
            await db.commit()
            await db.refresh(db_job)
            await logger.info("Created job", {
                "job_id": db_job.job_id,
                "user_id": job.user_id,
                "job_title": job.job_tittle
            })
            return db_job
        except Exception as e:
            await logger.error("Create job failed", error=e)
            await db.rollback()
            raise

async def get_job_by_id(db: AsyncSession, job_id: str):
    try:
        query = select(models.Job).where(models.Job.job_id == job_id)
        result = await db.execute(query)
        job = result.scalar_one_or_none()

        if not job:
            await logger.warning("Job not found", {"job_id": job_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        await logger.info("Retrieved job", {"job_id": job_id})
        return job
    except Exception as e:
        await logger.error("Get job by id failed", error=e)
        raise

async def get_jobs_by_user_id(db: AsyncSession, user_id: str):
    try:
        await _validate_user_exists(db, user_id)
        query = select(models.Job).where(models.Job.user_id == user_id)
        result = await db.execute(query)
        jobs = result.scalars().all()

        if not jobs:
            await logger.warning("No jobs found", {"user_id": user_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No jobs found for this user",
            )
        await logger.info("Retrieved jobs for user", {"user_id": user_id, "count": len(jobs)})
        return list(jobs)
    except Exception as e:
        await logger.error("Get jobs by user failed", error=e)
        raise

async def update_job(db: AsyncSession, job_id: str, job: schemas.JobUpdate):
    async with DistributedLock(f"job:{job_id}"):
        try:
            # First check if job exists
            existing_job = await get_job_by_id(db, job_id)
            await _validate_user_exists(db, existing_job.user_id)

            # Prepare update data
            update_data = job.dict(exclude_unset=True)

            # Execute update
            query = (
                update(models.Job)
                .where(models.Job.job_id == job_id)
                .values(**update_data)
                .execution_options(synchronize_session="fetch")
            )
            await db.execute(query)
            await db.commit()

            # Get and return updated job
            return await get_job_by_id(db, job_id)
        except HTTPException:
            raise
        except DatabaseOperationError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

async def delete_job(db: AsyncSession, job_id: str):
    async with DistributedLock(f"job:{job_id}"):
        try:
            # First check if job exists
            existing_job = await get_job_by_id(db, job_id)
            await _validate_user_exists(db, existing_job.user_id)

            # Execute delete
            query = (
                delete(models.Job)
                .where(models.Job.job_id == job_id)
                .execution_options(synchronize_session="fetch")
            )
            await db.execute(query)
            await db.commit()

            return {"detail": "Job deleted successfully"}
        except HTTPException:
            raise
        except DatabaseOperationError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

async def get_all_jobs(db: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        query = select(models.Job).offset(skip).limit(limit)
        result = await db.execute(query)
        jobs = result.scalars().all()
        await logger.info("Retrieved all jobs", {"count": len(jobs), "skip": skip, "limit": limit})
        return list(jobs)
    except Exception as e:
        await logger.error("Get all jobs failed", error=e)
        raise
