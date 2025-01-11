from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import daysHoliday as schemas
from ...services import daysHoliday as services
from ...utils import jwt
from typing import List

router = APIRouter()

@router.post(
    "/admin/holiday",
    response_model=schemas.DaysHolidayResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_holiday(
    holiday: schemas.DaysHolidayCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.create_holiday(holiday, db)

@router.put(
    "/admin/holiday/{holiday_id}",
    response_model=schemas.DaysHolidayResponse
)
async def update_holiday(
    holiday_id: str,
    holiday: schemas.DaysHolidayUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.update_holiday(
        db, holiday_id, holiday
    )

@router.delete("/admin/holiday/{holiday_id}")
async def delete_holiday(
    holiday_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.delete_holiday(db, holiday_id)
