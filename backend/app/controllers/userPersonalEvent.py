from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import userPersonalEvent as schemas
from ..models import users as models
from ..services import userPersonalEvent as services
from ..services import users
from ..utils import jwt
from ..database import get_db
from typing import List

router = APIRouter()

@router.post(
    "/personal_event",
    response_model=schemas.UserPersonalEventCreate,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_event(
    event: schemas.UserPersonalEventCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_user_event(db, event)

@router.get("/personal_event/{event_id}", response_model=schemas.UserPersonalEventCreate)
async def get_event_by_id(
    event_id: str = Path(..., description="Event ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_user_event_by_id(db, event_id)

# @router.get("/personal_event/user/{user_id}", response_model=List[schemas.UserPersonalEventCreate])
# async def get_events_by_user_id(
#     user_id: str = Path(..., description="User ID to retrieve events"),
#     db: AsyncSession = Depends(get_db),
#     current_user: models.Users = Depends(users.get_current_admin),
# ):
#     return await services.get_user_events_by_user_id_controller(db, user_id)

@router.put("/personal_event/{event_id}", response_model=schemas.UserPersonalEventCreate)
async def update_event(
    event: schemas.UserPersonalEventCreate = Query(...),
    event_id: str = Path(..., description="Event ID to update"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.update_user_event(db, event_id, event)

@router.delete("/personal_event/{event_id}")
async def delete_event(
    event_id: str = Path(..., description="Event ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.delete_user_event(db, event_id)

@router.get("/personal_event", response_model=List[schemas.UserPersonalEventCreate])
async def get_all_events(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_all_events(db, skip=skip, limit=limit)

@router.get("/me/personal_event", response_model=List[schemas.UserPersonalEventResponse])
async def get_current_user_personal_info(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):

    return await services.get_user_event_by_user_id(
        db, current_user.user_id
    )

@router.get("/personal_event/user/{user_id}", response_model=List[schemas.UserPersonalEventResponse])
async def get_personal_info_by_user_id(
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_user_event_by_user_id(db, user_id)

