from fastapi import APIRouter, Depends, HTTPException, status, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...services import userMessage as message_service
from ...schemas.userMessage import MessageResponse, MessageUpdate
from ...models import users as models
from ...utils import jwt
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.get("/admin/messages", response_model=List[MessageResponse])
@limiter.limit("10/minute")
async def get_all_messages(
    request: Request,
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
@limiter.limit("10/minute")
async def get_message(
    request: Request,
    message_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
   message = await message_service.get_message_by_id(db, message_id)
   return message

@router.delete("/admin/messages/{message_id}")
@limiter.limit("3/minute")
async def delete_message(
    request: Request,
    message_id: str = Path(..., description="Message ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    result = await message_service.delete_message(db, message_id)
    return result

@router.get("/admin/messages/user/{user_id}", response_model=List[MessageResponse])
@limiter.limit("10/minute")
async def get_user_messages(
    request: Request,
    user_id: str = Path(..., description="User ID to retrieve messages for"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    sent = await message_service.get_sent_messages(db, user_id)
    received = await message_service.get_received_messages(db, user_id)
    return [*sent, *received]
