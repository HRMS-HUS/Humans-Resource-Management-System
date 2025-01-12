from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import userPersonalEvent as schemas
from ...models import users as models
from ...services import userPersonalEvent as services
from ...services import users
from ...utils import jwt
from ...configs.database import get_db
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post(
    "/admin/personal_event",
    response_model=schemas.UserPersonalEventResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
async def create_user_event(
    request: Request,
    event: schemas.UserPersonalEventCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_user_event(db, event)

@router.get("/admin/personal_event/{event_id}", response_model=schemas.UserPersonalEventResponse)
@limiter.limit("10/minute")
async def get_event_by_id(
    request: Request,
    event_id: str = Path(..., description="Event ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_user_event_by_id(db, event_id)

@router.put("/admin/personal_event/{event_id}", response_model=schemas.UserPersonalEventResponse)
@limiter.limit("5/minute")
async def update_event(
    request: Request,
    event: schemas.UserPersonalEventUpdate,
    event_id: str = Path(..., description="Event ID to update"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.update_user_event(db, event_id, event)

@router.delete("/admin/personal_event/{event_id}")
@limiter.limit("3/minute")
async def delete_event(
    request: Request,
    event_id: str = Path(..., description="Event ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.delete_user_event(db, event_id)

@router.get("/admin/personal_event", response_model=List[schemas.UserPersonalEventResponse])
@limiter.limit("10/minute")
async def get_all_events(
    request: Request,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_all_events(db, skip=skip, limit=limit)

@router.get("/admin/personal_event/user/{user_id}", response_model=List[schemas.UserPersonalEventResponse])
@limiter.limit("10/minute")
async def get_personal_info_by_user_id(
    request: Request,
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_user_event_by_user_id(db, user_id)

