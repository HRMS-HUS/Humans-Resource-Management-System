from sqlalchemy.ext.asyncio import AsyncSession
from ..models import userPersonalEvent as models
from ..schemas import userPersonalEvent as schemas
from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from typing import List
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

async def create_user_event(db: AsyncSession, event: schemas.UserPersonalEventCreate):
    async with DistributedLock(f"event:user:{event.user_id}"):
        try:
            await _validate_user_exists(db, event.user_id)
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
            await logger.info("Created user event", {
                "event_id": db_event.event_id,
                "user_id": event.user_id
            })
            return db_event
        except Exception as e:
            await logger.error("Create user event failed", error=e)
            await db.rollback()
            raise

async def get_user_event_by_id(db: AsyncSession, event_id: str):
    try:
        result = await db.execute(
            select(models.UserPersonalEvent).filter(
                models.UserPersonalEvent.event_id == event_id
            )
        )
        event = result.scalar_one_or_none()

        if not event:
            await logger.warning("Event not found", {"event_id": event_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        await logger.info("Retrieved event by id", {"event_id": event_id})
        return event
    except Exception as e:
        await logger.error("Get event by id failed", error=e)
        raise

async def get_user_event_by_user_id(db: AsyncSession, user_id: str):
    try:
        result = await db.execute(
            select(models.UserPersonalEvent).filter(
                models.UserPersonalEvent.user_id == user_id
            )
        )
        events = result.scalars().all()

        if not events:
            await logger.warning("No events found for user", {"user_id": user_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        await logger.info("Retrieved events for user", {"user_id": user_id, "count": len(events)})
        return events
    except Exception as e:
        await logger.error("Get events by user failed", error=e)
        raise

async def get_all_events(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.UserPersonalEvent]:
    try:
        result = await db.execute(
            select(models.UserPersonalEvent).offset(skip).limit(limit)
        )
        events = result.scalars().all()
        await logger.info("Retrieved all events", {"count": len(events), "skip": skip, "limit": limit})
        return events
    except Exception as e:
        await logger.error("Get all events failed", error=e)
        raise

async def update_user_event(
    db: AsyncSession, event_id: str, event: schemas.UserPersonalEventUpdate
):
    async with DistributedLock(f"event:{event_id}"):
        try:
            query = (
                update(models.UserPersonalEvent)
                .where(models.UserPersonalEvent.event_id == event_id)
                .values(**event.dict(exclude_unset=True))  # Added exclude_unset=True
            )

            result = await db.execute(query)
            await db.commit()

            if result.rowcount == 0:
                await logger.warning("Event not found for update", {"event_id": event_id})
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
                )

            await logger.info("Updated user event", {"event_id": event_id})
            return await get_user_event_by_id(db, event_id)
        except Exception as e:
            await logger.error("Update user event failed", error=e)
            await db.rollback()
            raise

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
                await logger.warning("Event not found for deletion", {"event_id": event_id})
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
                )

            await logger.info("Deleted user event", {"event_id": event_id})
            return {"message": "Event deleted successfully"}
        except Exception as e:
            await logger.error("Delete user event failed", error=e)
            await db.rollback()
            raise
