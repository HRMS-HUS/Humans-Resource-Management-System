from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException, status
from ..models import daysHoliday as models
from ..schemas import daysHoliday as schemas
from typing import List
from ..utils.redis_lock import DistributedLock

class DatabaseOperationError(Exception):
    pass

async def create_holiday(
    holiday: schemas.DaysHolidayCreate, db: AsyncSession
):
    async with DistributedLock(f"holiday:{holiday.holiday_name}"):
        try:
            # Check if holiday already exists on the same date
            existing = await db.execute(
                select(models.DaysHoliday).filter(
                    models.DaysHoliday.holiday_date == holiday.holiday_date
                )
            )

            db_holiday = models.DaysHoliday(**holiday.dict())
            db.add(db_holiday)
            await db.commit()
            await db.refresh(db_holiday)
            return db_holiday
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


async def update_holiday(
    db: AsyncSession, holiday_id: str, holiday: schemas.DaysHolidayUpdate
):
    async with DistributedLock(f"holiday:{holiday_id}"):
        try:
            db_holiday = await get_holiday_by_id(db, holiday_id)

            for key, value in holiday.dict(exclude_unset=True).items():
                setattr(db_holiday, key, value)

            await db.commit()
            await db.refresh(db_holiday)
            return db_holiday
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


async def get_holiday_by_id(db: AsyncSession, holiday_id: str):
    try:
        async with db.begin():
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
    except HTTPException:
        await db.rollback()
        raise
    except DatabaseOperationError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database operation failed: {str(e)}"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


async def get_all_holidays(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.DaysHoliday]:
    try:
        result = await db.execute(
            select(models.DaysHoliday).offset(skip).limit(limit)
        )
        holidays = result.scalars().all()

        if not holidays:
            return []

        return holidays
    except HTTPException:
        await db.rollback()
        raise
    except DatabaseOperationError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def delete_holiday(db: AsyncSession, holiday_id: str):
    async with DistributedLock(f"holiday:{holiday_id}"):
        try:
            await get_holiday_by_id(db, holiday_id)

            stmt = delete(models.DaysHoliday).where(
                models.DaysHoliday.holiday_id == holiday_id
            )

            await db.execute(stmt)
            await db.commit()

            return {"detail": "Holiday deleted successfully"}
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
