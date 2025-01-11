from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException, status
from ..models import daysHoliday as models
from ..schemas import daysHoliday as schemas
from typing import List
from ..utils.redis_lock import DistributedLock
from ..utils.logger import logger

class DatabaseOperationError(Exception):
    pass

async def create_holiday(
    holiday: schemas.DaysHolidayCreate, db: AsyncSession
):
    async with DistributedLock(f"holiday:{holiday.holiday_name}"):
        try:
            db_holiday = models.DaysHoliday(**holiday.dict())
            db.add(db_holiday)
            await db.commit()
            await db.refresh(db_holiday)
            await logger.info("Created holiday", {"holiday_id": db_holiday.holiday_id})
            return db_holiday
        except Exception as e:
            await logger.error("Create holiday failed", error=e)
            await db.rollback()
            raise

async def update_holiday(
    db: AsyncSession, holiday_id: str, holiday: schemas.DaysHolidayUpdate
):
    async with DistributedLock(f"holiday:{holiday_id}"):
        try:
            db_holiday = await get_holiday_by_id(db, holiday_id)
            for key, value in holiday.dict(exclude_unset=True).items():
                setattr(db_holiday, key, value)
            await db.commit()
            await logger.info("Updated holiday", {"holiday_id": holiday_id})
            return db_holiday
        except Exception as e:
            await logger.error("Update holiday failed", error=e)
            await db.rollback()
            raise

async def get_holiday_by_id(db: AsyncSession, holiday_id: str):
    try:
        result = await db.execute(
            select(models.DaysHoliday).filter(
                models.DaysHoliday.holiday_id == holiday_id
            )
        )
        holiday = result.scalar_one_or_none()

        if not holiday:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Holiday not found"
            )
        
        return holiday
    except Exception as e:
        await logger.error("Get holiday by id failed", error=e)
        raise

async def get_all_holidays(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.DaysHoliday]:
    try:
        result = await db.execute(
            select(models.DaysHoliday).offset(skip).limit(limit)
        )
        holidays = result.scalars().all()
        return holidays if holidays else []
    except Exception as e:
        await logger.error("Get all holidays failed", error=e)
        raise

async def delete_holiday(db: AsyncSession, holiday_id: str):
    async with DistributedLock(f"holiday:{holiday_id}"):
        try:
            holiday = await get_holiday_by_id(db, holiday_id)
            stmt = delete(models.DaysHoliday).where(
                models.DaysHoliday.holiday_id == holiday_id
            )
            await db.execute(stmt)
            await db.commit()
            await logger.info("Deleted holiday", {"holiday_id": holiday_id})
            return {"detail": "Holiday deleted successfully"}
        except Exception as e:
            await logger.error("Delete holiday failed", error=e)
            await db.rollback()
            raise
