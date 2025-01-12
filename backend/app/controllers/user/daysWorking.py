from fastapi import APIRouter, Depends, HTTPException, status, Path, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from ...configs.database import get_db
from ...schemas import daysWorking as schemas
from ...models import users as models
from ...services import daysWorking as services
from ...utils import jwt
from typing import List
from datetime import date

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.get(
    "/me/working/{working_id}",
    response_model=schemas.DaysWorkingResponse
)
@limiter.limit("10/minute")
async def get_working_day(
    request: Request,
    working_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    return await services.get_working_day_by_id(db, working_id)


@router.get(
    "/me/working/history",
    response_model=List[schemas.DaysWorkingResponse]
)
@limiter.limit("10/minute")
async def get_my_working_days(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user)
):
    return await services.get_working_day_by_user_id(db, current_user.user_id, skip, limit)

# @router.get(
#     "/me/attendance",
#     response_model=List[schemas.DaysWorkingResponse]
# )
# @limiter.limit("10/minute")
# async def get_my_attendance_records(
#     request: Request,
#     skip: int = 0,
#     limit: int = 100,
#     start_date: date = None,
#     end_date: date = None,
#     db: AsyncSession = Depends(get_db),
#     current_user: dict = Depends(jwt.get_active_user)
# ):
#     return await services.get_all_working_days(
#         db, skip, limit, start_date, end_date, current_user.user_id
#     )

# @router.get(
#     "/me/attendance/{working_id}",
#     response_model=schemas.DaysWorkingResponse
# )
# @limiter.limit("10/minute")
# async def get_my_attendance_record(
#     request: Request,
#     working_id: str,
#     db: AsyncSession = Depends(get_db),
#     current_user: dict = Depends(jwt.get_active_user)
# ):
#     return await services.get_working_day_by_id(db, working_id)
