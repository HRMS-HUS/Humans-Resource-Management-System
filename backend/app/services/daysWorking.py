from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException, status
from ..models import daysWorking as models
from ..schemas import daysWorking as schemas
from typing import List
from ..utils.redis_lock import DistributedLock


async def create_working_day(
    working: schemas.DaysWorkingCreate, db: AsyncSession
):
    async with DistributedLock(f"working:{working.day}"):
        # Check if working day already exists on the same date
        existing = await db.execute(
            select(models.DaysWorking).filter(
                models.DaysWorking.day == working.day
            )
        )

        db_working = models.DaysWorking(**working.dict())
        db.add(db_working)
        await db.commit()
        await db.refresh(db_working)
        return db_working


async def update_working_day(
    db: AsyncSession, working_id: str, working: schemas.DaysWorkingUpdate
):
    async with DistributedLock(f"working:{working_id}"):
        db_working = await get_working_day_by_id(db, working_id)

        for key, value in working.dict(exclude_unset=True).items():
            setattr(db_working, key, value)

        await db.commit()
        await db.refresh(db_working)
        return db_working


async def get_working_day_by_id(db: AsyncSession, working_id: str):
    result = await db.execute(
        select(models.DaysWorking).filter(
            models.DaysWorking.working_id == working_id
        )
    )
    working = result.scalar_one_or_none()

    if not working:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Working day not found"
        )

    return working


async def get_all_working_days(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.DaysWorking]:
    result = await db.execute(
        select(models.DaysWorking).offset(skip).limit(limit)
    )
    working_days = result.scalars().all()

    if not working_days:
        return []

    return working_days


async def delete_working_day(db: AsyncSession, working_id: str):
    async with DistributedLock(f"working:{working_id}"):
        await get_working_day_by_id(db, working_id)

        stmt = delete(models.DaysWorking).where(
            models.DaysWorking.working_id == working_id
        )

        await db.execute(stmt)
        await db.commit()

        return {"detail": "Working day deleted successfully"}
