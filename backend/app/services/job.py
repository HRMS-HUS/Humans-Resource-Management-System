# services/job.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from fastapi import HTTPException, status
from ..models import job as models
from ..schemas import job as schemas
from typing import List, Optional
from ..utils.redis_lock import DistributedLock

class DatabaseOperationError(Exception):
    pass

async def create_job(db: AsyncSession, job: schemas.JobCreate):
    async with DistributedLock(f"job:user:{job.user_id}"):
        try:
            db_job = models.Job(
                user_id=job.user_id,
                job_tittle=job.job_tittle,  # Note: There's a typo in 'tittle', should be 'title'
                start_date=job.start_date,
                end_date=job.end_date,
            )

            db.add(db_job)
            await db.commit()
            await db.refresh(db_job)
            return db_job
        except HTTPException:
            await db.rollback()
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

async def get_job_by_id(db: AsyncSession, job_id: str):
    try:
        async with db.begin():
            query = select(models.Job).where(models.Job.job_id == job_id)
            result = await db.execute(query)
            job = result.scalar_one_or_none()

            if not job:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
                )
            return job
    except HTTPException:
        await db.rollback()
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

async def get_jobs_by_user_id(db: AsyncSession, user_id: str):
    try:
        async with db.begin():
            query = select(models.Job).where(models.Job.user_id == user_id)
            result = await db.execute(query)
            jobs = result.scalars().all()

            if not jobs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No jobs found for this user",
                )
            return list(jobs)
    except HTTPException:
        await db.rollback()
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

async def update_job(db: AsyncSession, job_id: str, job: schemas.JobUpdate):
    async with DistributedLock(f"job:{job_id}"):
        try:
            # First check if job exists
            await get_job_by_id(db, job_id)

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
            await get_job_by_id(db, job_id)

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

async def get_all_jobs(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.Job]:
    try:
        async with db.begin():
            query = select(models.Job).offset(skip).limit(limit)
            result = await db.execute(query)
            jobs = result.scalars().all()
            return list(jobs)
    except HTTPException:
        await db.rollback()
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
