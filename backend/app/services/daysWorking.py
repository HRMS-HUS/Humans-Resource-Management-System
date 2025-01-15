from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException, status
from ..models import daysWorking as models
from ..schemas import daysWorking as schemas
from typing import List
from ..utils.redis_lock import DistributedLock
from ..utils.logger import logger
from datetime import datetime, date, timezone, time, timedelta
import pytz

class DatabaseOperationError(Exception):
    pass

# async def create_working_day(
#     working: schemas.DaysWorkingCreate, db: AsyncSession
# ):
#     async with DistributedLock(f"working:{working.day}"):
#         try:
#             # Check if working day already exists on the same date
#             existing = await db.execute(
#                 select(models.DaysWorking).filter(
#                     models.DaysWorking.day == working.day
#                 )
#             )

#             db_working = models.DaysWorking(**working.dict())
#             db.add(db_working)
#             await db.commit()
#             await logger.info("Created working day", {
#                 "working_id": db_working.working_id,
#                 "day": str(working.day)
#             })
#             await db.refresh(db_working)
#             return db_working
#         except HTTPException:
#             await db.rollback()
#             raise
#         except DatabaseOperationError:
#             await db.rollback()
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Database operation failed"
#             )
#         except Exception as e:
#             await logger.error("Create working day failed", error=e)
#             await db.rollback()
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Internal server error"
#             )


# async def update_working_day(
#     db: AsyncSession, working_id: str, working: schemas.DaysWorkingUpdate
# ):
#     async with DistributedLock(f"working:{working_id}"):
#         try:
#             db_working = await get_working_day_by_id(db, working_id)

#             for key, value in working.dict(exclude_unset=True).items():
#                 setattr(db_working, key, value)

#             await db.commit()
#             await db.refresh(db_working)
#             await logger.info("Updated working day", {
#                 "working_id": db_working.working_id,
#                 "day": str(db_working.day)
#             })
#             return db_working
#         except HTTPException:
#             await db.rollback()
#             raise
#         except DatabaseOperationError:
#             await db.rollback()
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Database operation failed"
#             )
#         except Exception as e:
#             await logger.error("Update working day failed", error=e)
#             await db.rollback()
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Internal server error"
#             )


async def get_working_day_by_id(db: AsyncSession, working_id: str):
    try:
        result = await db.execute(
            select(models.DaysWorking).filter(
                models.DaysWorking.working_id == working_id
            )
        )
        working = result.scalar_one_or_none()

        if not working:
            await logger.warning("Working day not found", {"working_id": working_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Working day not found"
            )
        await logger.info("Retrieved working day", {"working_id": working_id})
        return working
    except HTTPException:
        raise
    except Exception as e:
        await logger.error("Get working day failed", error=e)
        raise


async def get_all_working_days(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.DaysWorking]:
    try:
        result = await db.execute(
            select(models.DaysWorking).offset(skip).limit(limit)
        )
        working_days = result.scalars().all()
        await logger.info("Retrieved all working days", {
            "count": len(working_days),
            "skip": skip,
            "limit": limit
        })
        return working_days if working_days else []
    except Exception as e:
        await logger.error("Get all working days failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def delete_working_day(db: AsyncSession, working_id: str):
    async with DistributedLock(f"working:{working_id}"):
        try:
            await get_working_day_by_id(db, working_id)

            stmt = delete(models.DaysWorking).where(
                models.DaysWorking.working_id == working_id
            )

            await db.execute(stmt)
            await db.commit()
            await logger.info("Deleted working day", {"working_id": working_id})
            return {"detail": "Working day deleted successfully"}
        except HTTPException:
            await db.rollback()
            raise
        except DatabaseOperationError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except Exception as e:
            await logger.error("Delete working day failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

async def create_attendance_record(
    user_id: str,
    db: AsyncSession
):
    async with DistributedLock(f"working:{user_id}:{date.today()}"):
        try:
            # Check if attendance record already exists for today
            existing = await db.execute(
                select(models.DaysWorking).filter(
                    models.DaysWorking.user_id == user_id,
                    models.DaysWorking.day == date.today()
                )
            )
            # if existing.scalar_one_or_none():
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail="Attendance already recorded for today"
            #     )

            # Get current time with timezone
            current_datetime = datetime.now(timezone.utc)
            current_time = current_datetime.time().replace(tzinfo=timezone.utc)
            
            working_data = {
                "user_id": user_id,
                "day": date.today(),
                "login_time": current_time,
                "total_hours": 0.0  # Explicitly set as float
            }
            
            db_working = models.DaysWorking(**working_data)
            db.add(db_working)
            await db.commit()
            await logger.info("Created attendance record", {
                "user_id": user_id,
                "login_time": str(current_time)
            })
            await db.refresh(db_working)
            return db_working
        except Exception as e:
            await logger.error("Create attendance record failed", error=e)
            await db.rollback()
            raise

async def update_attendance_logout(
    user_id: str,
    db: AsyncSession
):
    async with DistributedLock(f"working:{user_id}"):
        try:
            result = await db.execute(
                select(models.DaysWorking).filter(
                    models.DaysWorking.user_id == user_id,
                    models.DaysWorking.day == date.today()
                )
            )
            record = result.scalar_one_or_none()
            
            if not record:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No attendance record found for today"
                )

            # Get current time with timezone
            current_datetime = datetime.now(timezone.utc)
            current_time = current_datetime.time().replace(tzinfo=timezone.utc)
            
            # Calculate total hours using timezone-aware times
            login_datetime = datetime.combine(date.today(), record.login_time)
            logout_datetime = datetime.combine(date.today(), current_time)
            
            # Ensure both times are timezone-aware
            if login_datetime.tzinfo is None:
                login_datetime = login_datetime.replace(tzinfo=timezone.utc)
            if logout_datetime.tzinfo is None:
                logout_datetime = logout_datetime.replace(tzinfo=timezone.utc)
                
            total_hours = (logout_datetime - login_datetime).total_seconds() / 3600

            record.logout_time = current_time
            record.total_hours = round(total_hours, 2)

            await db.commit()
            await db.refresh(record)
            await logger.info("Updated attendance logout", {
                "user_id": user_id,
                "logout_time": str(current_time),
                "total_hours": total_hours
            })
            return record
        except Exception as e:
            await logger.error("Update attendance logout failed", error=e)
            await db.rollback()
            raise

async def get_working_day_by_user_id(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100):
    try:
        # Add query to check if user has any working days
        count_query = select(models.DaysWorking).filter(
            models.DaysWorking.user_id == user_id
        )
        count_result = await db.execute(count_query)
        if not count_result.scalars().first():
            await logger.warning("No working days found for user", {"user_id": user_id})
            return []

        # Get working days with pagination
        query = select(models.DaysWorking).filter(
            models.DaysWorking.user_id == user_id
        ).offset(skip).limit(limit).order_by(models.DaysWorking.day.desc())
        
        result = await db.execute(query)
        working_days = result.scalars().all()
        
        if working_days:
            await logger.info("Retrieved working days for user", {
                "user_id": user_id,
                "count": len(working_days)
            })
            return list(working_days)  # Convert to list explicitly
        return []
        
    except Exception as e:
        await logger.error("Get working days by user failed", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get working days: {str(e)}"
        )