from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import daysWorking as schemas
from ...services import daysWorking as services
from ...utils import jwt
from typing import List

router = APIRouter()

@router.post(
    "/admin/working",
    response_model=schemas.DaysWorkingResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_working_day(
    working: schemas.DaysWorkingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.create_working_day(working, db)

@router.put(
    "/admin/working/{working_id}",
    response_model=schemas.DaysWorkingResponse
)
async def update_working_day(
    working_id: str,
    working: schemas.DaysWorkingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.update_working_day(
        db, working_id, working
    )

@router.delete("/admin/working/{working_id}")
async def delete_working_day(
    working_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.delete_working_day(db, working_id)

@router.get(
    "/admin/working",
    response_model=List[schemas.DaysWorkingResponse]
)
async def get_all_working_days(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_all_working_days(db, skip, limit)

@router.get(
    "/admin/working/{working_id}",
    response_model=schemas.DaysWorkingResponse
)
async def get_working_day(
    working_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_working_day_by_id(db, working_id)
