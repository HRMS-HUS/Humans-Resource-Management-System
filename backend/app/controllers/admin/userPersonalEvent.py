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
    "/admin/personal_event",
    response_model=schemas.UserPersonalEventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_event(
    event: schemas.UserPersonalEventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_user_event(db, event)

@router.get("/admin/personal_event/{event_id}", response_model=schemas.UserPersonalEventResponse)
async def get_event_by_id(
    event_id: str = Path(..., description="Event ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_user_event_by_id(db, event_id)

@router.put("/admin/personal_event/{event_id}", response_model=schemas.UserPersonalEventResponse)
async def update_event(
    event: schemas.UserPersonalEventUpdate,
    event_id: str = Path(..., description="Event ID to update"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.update_user_event(db, event_id, event)

@router.delete("/admin/personal_event/{event_id}")
async def delete_event(
    event_id: str = Path(..., description="Event ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.delete_user_event(db, event_id)

@router.get("/admin/personal_event", response_model=List[schemas.UserPersonalEventResponse])
async def get_all_events(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_all_events(db, skip=skip, limit=limit)

@router.get("/admin/personal_event/user/{user_id}", response_model=List[schemas.UserPersonalEventResponse])
async def get_personal_info_by_user_id(
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_user_event_by_user_id(db, user_id)

