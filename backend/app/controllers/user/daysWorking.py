from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import daysWorking as schemas
from ...models import users as models
from ...services import daysWorking as services
from ...utils import jwt
from typing import List

router = APIRouter()

@router.get(
    "me/working/{working_id}",
    response_model=schemas.DaysWorkingResponse
)
async def get_working_day(
    working_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    return await services.get_working_day_by_id(db, working_id)

@router.get(
    "me/working",
    response_model=List[schemas.DaysWorkingResponse]
)
async def get_all_working_days(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    return await services.get_all_working_days(db, skip, limit)
