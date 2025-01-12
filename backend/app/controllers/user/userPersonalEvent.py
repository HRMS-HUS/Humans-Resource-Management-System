from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import userPersonalEvent as schemas
from ...models import users as models
from ...services import userPersonalEvent as services
from ...services import users
from ...utils import jwt
from ...configs.database import get_db
from typing import List

router = APIRouter()

@router.post(
    "/me/personal_event",
    response_model=schemas.UserPersonalEventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_event_me(
    event: schemas.UserPersonalEventCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # # Validate and set user_id
    # if event.user_id and event.user_id != current_user.user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Cannot create events for other users"
    #     )
    event.user_id = current_user.user_id
    return await services.create_user_event(db, event)

@router.put(
    "/me/personal_event/{event_id}",
    response_model=schemas.UserPersonalEventResponse,
)
async def update_user_event_me(
    event_id: str = Path(..., description="Event ID to update"),
    event_update: schemas.UserPersonalEventUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # Check if event exists and belongs to current user
    existing_event = await services.get_user_event_by_id(db, event_id)
    if not existing_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    if existing_event.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this event"
        )
    
    return await services.update_user_event(db, event_id, event_update)

@router.get("/me/personal_event", response_model=List[schemas.UserPersonalEventResponse])
async def get_current_user_personal_event(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):

    return await services.get_user_event_by_user_id(
        db, current_user.user_id
    )

@router.delete("/me/personal_event/{event_id}")
async def delete_event(
    event_id: str = Path(..., description="Event ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    # Check if event exists and belongs to current user
    event = await services.get_user_event_by_id(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    if event.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this event"
        )
    
    return await services.delete_user_event(db, event_id)