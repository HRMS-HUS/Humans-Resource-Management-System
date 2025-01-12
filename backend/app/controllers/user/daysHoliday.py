from fastapi import APIRouter, Depends, HTTPException, status, Path, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import daysHoliday as schemas
from ...models import users as models
from ...services import daysHoliday as services
from ...utils import jwt
from typing import List

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.get(
    "/me/holiday/{holiday_id}",
    response_model=schemas.DaysHolidayResponse
)
@limiter.limit("10/minute")
async def get_holiday(
    request: Request,
    holiday_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    return await services.get_holiday_by_id(db, holiday_id)

@router.get(
    "/me/holidays",
    response_model=List[schemas.DaysHolidayResponse]
)
@limiter.limit("10/minute")
async def get_all_holidays(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    return await services.get_all_holidays(db, skip, limit)
