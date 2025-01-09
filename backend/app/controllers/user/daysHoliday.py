from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import daysHoliday as schemas
from ...models import users as models
from ...services import daysHoliday as services
from ...utils import jwt
from typing import List

router = APIRouter()

@router.get(
    "me/holiday/{holiday_id}",
    response_model=schemas.DaysHolidayResponse
)
async def get_holiday(
    holiday_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    return await services.get_holiday_by_id(db, holiday_id)

@router.get(
    "me/holidays",
    response_model=List[schemas.DaysHolidayResponse]
)
async def get_all_holidays(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    return await services.get_all_holidays(db, skip, limit)
