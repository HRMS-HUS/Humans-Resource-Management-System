from sqlalchemy.ext.asyncio import AsyncSession
from ..models import job as models
from ..schemas import job as schemas
from fastapi import HTTPException, status
from sqlalchemy import select, delete, update

async def create_job(db: AsyncSession, job: schemas.JobCreate):
    db_job = models.Job(
        job_id=job.job_id,
        user_id=job.user_id,
        job_tittle=job.job_tittle,
        start_date=job.start_date,
        end_date=job.end_date
    )
    
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job

async def get_job_by_id(db: AsyncSession, job_id: str):
    result = await db.execute(
        select(models.Job).filter(
            models.Job.job_id == job_id
        )
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Job not found"
        )
    
    return job

async def get_jobs_by_user_id(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(models.Job).filter(
            models.Job.user_id == user_id
        )
    )
    jobs = result.scalars().all()
    
    if not jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Jobs not found for this user"
        )
    
    return jobs

async def update_job(db: AsyncSession, job_id: str, job: schemas.JobCreate):
    await get_job_by_id(db, job_id)
    
    update_data = {
        "user_id": job.user_id,
        "job_tittle": job.job_tittle,
        "start_date": job.start_date,
        "end_date": job.end_date
    }
    
    stmt = update(models.Job).where(
        models.Job.job_id == job_id
    ).values(**update_data)
    
    await db.execute(stmt)
    await db.commit()
    
    updated_job = await get_job_by_id(db, job_id)
    return updated_job

async def delete_job(db: AsyncSession, job_id: str):
    await get_job_by_id(db, job_id)
    
    stmt = delete(models.Job).where(
        models.Job.job_id == job_id
    )
    
    await db.execute(stmt)
    await db.commit()
    
    return {"detail": "Job deleted successfully"}

async def get_all_jobs(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Job)
        .offset(skip)
        .limit(limit)
    )
    
    jobs = result.scalars().all()
    
    if not jobs:
        return []
    
    return jobs
