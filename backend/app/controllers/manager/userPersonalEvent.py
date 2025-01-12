from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import userPersonalEvent as schemas
from ...services import userPersonalEvent as services
from ...services import userPersonalInfo as user_info_services
from ...services import department as dept_services
from ...models import users as models
from ...configs.database import get_db
from ...utils import jwt
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

async def validate_user_department(db: AsyncSession, user_id: str, manager_id: str):
    # Get manager's department
    dept = await dept_services.get_department_by_manager_id(db, manager_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager has no associated department"
        )
    
    # Get user's department
    user_info = await user_info_services.get_user_personal_info_by_user_id(db, user_id)
    if user_info.department_id != dept.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User not in manager's department"
        )
    return dept

@router.post("/manager/events", response_model=schemas.UserPersonalEventResponse)
@limiter.limit("5/minute")
async def create_event(
    request: Request,
    event: schemas.UserPersonalEventCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    await validate_user_department(db, event.user_id, current_user.user_id)
    return await services.create_user_event(db, event)

@router.get("/manager/events/{event_id}", response_model=schemas.UserPersonalEventResponse)
@limiter.limit("10/minute")
async def get_event(
    request: Request,
    event_id: str = Path(..., description="Event ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    event = await services.get_user_event_by_id(db, event_id)
    await validate_user_department(db, event.user_id, current_user.user_id)
    return event

@router.get("/manager/users/{user_id}/events", response_model=List[schemas.UserPersonalEventResponse])
@limiter.limit("10/minute")
async def get_user_events(
    request: Request,
    user_id: str = Path(..., description="User ID to retrieve events"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    await validate_user_department(db, user_id, current_user.user_id)
    return await services.get_user_event_by_user_id(db, user_id)

@router.put("/manager/events/{event_id}", response_model=schemas.UserPersonalEventResponse)
@limiter.limit("5/minute")
async def update_event(
    request: Request,
    event_id: str = Path(..., description="Event ID to update"),
    event_update: schemas.UserPersonalEventUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    event = await services.get_user_event_by_id(db, event_id)
    await validate_user_department(db, event.user_id, current_user.user_id)
    return await services.update_user_event(db, event_id, event_update)

@router.delete("/manager/events/{event_id}")
@limiter.limit("3/minute")
async def delete_event(
    request: Request,
    event_id: str = Path(..., description="Event ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    event = await services.get_user_event_by_id(db, event_id)
    await validate_user_department(db, event.user_id, current_user.user_id)
    return await services.delete_user_event(db, event_id)
