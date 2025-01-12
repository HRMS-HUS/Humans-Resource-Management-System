from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import userMessage as schemas
from ...models import users as models
from ...services import userMessage as services
from ...utils import jwt
from ...configs.database import get_db
from typing import List

router = APIRouter()

@router.post(
    "/me/messages",
    response_model=schemas.MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_message_me(
    message: schemas.MessageCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # # Validate and set sender_id
    # if message.sender_id and message.sender_id != current_user.user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Cannot send messages on behalf of other users"
    #     )
    message.sender_id = current_user.user_id
    return await services.create_message(db, message)

@router.get(
    "/me/messages/sent",
    response_model=List[schemas.MessageResponse]
)
async def get_sent_messages_me(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    return await services.get_sent_messages(db, current_user.user_id)

@router.get(
    "/me/messages/received",
    response_model=List[schemas.MessageResponse]
)
async def get_received_messages_me(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    return await services.get_received_messages(db, current_user.user_id)

@router.get(
    "/me/messages/{message_id}",
    response_model=schemas.MessageResponse
)
async def get_message_me(
    message_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    message = await services.get_message_by_id(db, message_id)
    if message.sender_id != current_user.user_id and message.receiver_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this message"
        )
    return message

@router.put(
    "/me/messages/{message_id}",
    response_model=schemas.MessageResponse
)
async def update_message_me(
    message_id: str = Path(...),
    message: schemas.MessageUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # Check if message exists and belongs to current user
    existing_message = await services.get_message_by_id(db, message_id)
    if existing_message.sender_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this message"
        )
    
    return await services.update_message(db, message_id, message)

@router.delete("/me/messages/{message_id}")
async def delete_message_me(
    message_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # Check if message exists and belongs to current user
    existing_message = await services.get_message_by_id(db, message_id)
    if existing_message.sender_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this message"
        )
    
    return await services.delete_message(db, message_id)
