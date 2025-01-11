from sqlalchemy.ext.asyncio import AsyncSession
from ..models import userMessage as models
from ..schemas import userMessage as schemas
from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from typing import List
from ..utils.redis_lock import DistributedLock
from ..services import users as user_service
from ..utils.logger import logger

async def _validate_users_exist(db: AsyncSession, sender_id: str, receiver_id: str):
    """Validate if both sender and receiver exist in the database"""
    try:
        sender = await user_service.get_user_by_id(db, sender_id)
        receiver = await user_service.get_user_by_id(db, receiver_id)
        if not sender or not receiver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sender or receiver not found"
            )
        return True
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error validating users"
        )

async def create_message(db: AsyncSession, message: schemas.MessageCreate):
    try:
        await _validate_users_exist(db, message.sender_id, message.receiver_id)
        db_message = models.UserMessage(**message.dict())
        db.add(db_message)
        await db.commit()
        await db.refresh(db_message)
        await logger.info("Created message", {
            "message_id": db_message.message_id,
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id
        })
        return db_message
    except Exception as e:
        await logger.error("Create message failed", error=e)
        await db.rollback()
        raise

async def get_message_by_id(db: AsyncSession, message_id: str):
    try:
        result = await db.execute(
            select(models.UserMessage).filter(
                models.UserMessage.message_id == message_id
            )
        )
        message = result.scalar_one_or_none()

        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        return message
    except HTTPException:
        raise

async def get_sent_messages(db: AsyncSession, user_id: str):
    try:
        result = await db.execute(
            select(models.UserMessage).filter(
                models.UserMessage.sender_id == user_id
            )
        )
        messages = result.scalars().all()
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def get_received_messages(db: AsyncSession, user_id: str):
    try:
        result = await db.execute(
            select(models.UserMessage).filter(
                models.UserMessage.receiver_id == user_id
            )
        )
        messages = result.scalars().all()
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def update_message(
    db: AsyncSession, message_id: str, message: schemas.MessageUpdate
):
    async with DistributedLock(f"message:{message_id}"):
        try:
            query = (
                update(models.UserMessage)
                .where(models.UserMessage.message_id == message_id)
                .values(message.dict(exclude_unset=True))
            )

            result = await db.execute(query)
            await db.commit()

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Message not found"
                )

            return await get_message_by_id(db, message_id)
        except HTTPException:
            await db.rollback()
            raise
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

async def delete_message(db: AsyncSession, message_id: str):
    async with DistributedLock(f"message:{message_id}"):
        try:
            result = await db.execute(
                delete(models.UserMessage).where(
                    models.UserMessage.message_id == message_id
                )
            )
            await db.commit()

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Message not found"
                )

            return {"message": "Message deleted successfully"}
        except HTTPException:
            await db.rollback()
            raise
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

async def get_all_messages(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.UserMessage]:
    try:
        result = await db.execute(
            select(models.UserMessage).offset(skip).limit(limit)
        )
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
