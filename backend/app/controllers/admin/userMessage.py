from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...services import userMessage as message_service
from ...schemas.userMessage import MessageResponse, MessageUpdate
from ...models import users as models
from ...utils import jwt
from typing import List

router = APIRouter()

@router.get("/admin/messages", response_model=List[MessageResponse])
async def get_all_messages(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    """Get all messages - Admin only endpoint"""
    try:
        messages = await message_service.get_all_messages(db, skip, limit)
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/admin/messages/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    """Get specific message by ID - Admin only endpoint"""
    try:
        message = await message_service.get_message_by_id(db, message_id)
        return message
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/admin/messages/{message_id}")
async def delete_message(
    message_id: str = Path(..., description="Message ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    """Delete a message - Admin only endpoint"""
    try:
        result = await message_service.delete_message(db, message_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/admin/messages/user/{user_id}", response_model=List[MessageResponse])
async def get_user_messages(
    user_id: str = Path(..., description="User ID to retrieve messages for"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    """Get all messages for a specific user - Admin only endpoint"""
    try:
        sent = await message_service.get_sent_messages(db, user_id)
        received = await message_service.get_received_messages(db, user_id)
        return [*sent, *received]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
