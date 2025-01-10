from sqlalchemy.ext.asyncio import AsyncSession
from ..models import userPersonalEvent as models
from ..schemas import userPersonalEvent as schemas
from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from typing import List
from ..utils.redis_lock import DistributedLock

class DatabaseOperationError(Exception):
    pass

async def create_user_event(db: AsyncSession, event: schemas.UserPersonalEventCreate):
    async with DistributedLock(f"event:user:{event.user_id}"):
        try:
            db_event = models.UserPersonalEvent(
                user_id=event.user_id,
                event_title=event.event_title,
                event_description=event.event_description,
                event_start_date=event.event_start_date,
                event_end_date=event.event_end_date,
            )
            db.add(db_event)
            await db.commit()
            await db.refresh(db_event)
            return db_event
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

async def get_user_event_by_id(db: AsyncSession, event_id: str):
    try:
        async with db.begin():
            result = await db.execute(
                select(models.UserPersonalEvent).filter(
                    models.UserPersonalEvent.event_id == event_id
                )
            )
            event = result.scalar_one_or_none()

            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
                )
            return event
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

async def get_user_event_by_user_id(db: AsyncSession, user_id: str):
    try:
        async with db.begin():
            result = await db.execute(
                select(models.UserPersonalEvent).filter(
                    models.UserPersonalEvent.user_id == user_id
                )
            )
            events = result.scalars().all()

            if not events:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
                )
            return events
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

async def get_all_events(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.UserPersonalEvent]:
    try:
        async with db.begin():
            result = await db.execute(
                select(models.UserPersonalEvent).offset(skip).limit(limit)
            )
            return result.scalars().all()
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

async def update_user_event(
    db: AsyncSession, event_id: str, event: schemas.UserPersonalEventUpdate
):
    async with DistributedLock(f"event:{event_id}"):
        try:
            query = (
                update(models.UserPersonalEvent)
                .where(models.UserPersonalEvent.event_id == event_id)
                .values(event.dict(exclude_unset=True))
            )

            result = await db.execute(query)
            await db.commit()

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
                )

            return await get_user_event_by_id(db, event_id)
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

async def delete_user_event(db: AsyncSession, event_id: str):
    async with DistributedLock(f"event:{event_id}"):
        try:
            result = await db.execute(
                delete(models.UserPersonalEvent).where(
                    models.UserPersonalEvent.event_id == event_id
                )
            )
            await db.commit()

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
                )

            return {"message": "Event deleted successfully"}
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
