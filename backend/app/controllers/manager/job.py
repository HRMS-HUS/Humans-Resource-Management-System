# controllers/manager/job.py
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import job as schemas
from ...services import job as services

async def create_job(db: AsyncSession, job: schemas.JobCreate):
    return await services.create_job(db, job)

async def get_job_by_id_controller(db: AsyncSession, job_id: str):
    return await services.get_job_by_id(db, job_id)

async def get_jobs_by_user_id_controller(db: AsyncSession, user_id: str):
    return await services.get_jobs_by_user_id(db, user_id)

async def update_job_controller(db: AsyncSession, job_id: str, job: schemas.JobCreate):
    return await services.update_job(db, job_id, job)

async def delete_job_controller(db: AsyncSession, job_id: str):
    return await services.delete_job(db, job_id)

async def get_all_jobs_controller(db: AsyncSession, skip: int = 0, limit: int = 100):
    return await services.get_all_jobs(db, skip, limit)