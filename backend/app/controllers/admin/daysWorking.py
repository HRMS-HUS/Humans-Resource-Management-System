from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from ...configs.database import get_db
from ...schemas import daysWorking as schemas
from ...services import daysWorking as services
from ...utils import jwt
from typing import List
from datetime import date

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

# @router.post(
#     "/admin/working",
#     response_model=schemas.DaysWorkingResponse,
#     status_code=status.HTTP_201_CREATED
# )
# @limiter.limit("5/minute")
# async def create_working_day(
#     request: Request,
#     working: schemas.DaysWorkingCreate = Query(...),
#     db: AsyncSession = Depends(get_db),
#     current_user: dict = Depends(jwt.get_current_admin)
# ):
#     return await services.create_working_day(working, db)

@router.put(
    "/admin/working/{working_id}",
    response_model=schemas.DaysWorkingResponse
)
@limiter.limit("20/minute")
async def update_working_day(
    request: Request,
    working_id: str = Path(..., description="Working ID to update"),
    working: schemas.DaysWorkingUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.update_working_day(
        db, working_id, working
    )

@router.delete("/admin/working/{working_id}")
@limiter.limit("20/minute")
async def delete_working_day(
    request: Request,
    working_id: str = Path(..., description="Working ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.delete_working_day(db, working_id)

@router.get(
    "/admin/working",
    response_model=List[schemas.DaysWorkingResponse]
)
@limiter.limit("20/minute")
async def get_all_working_days(
    request: Request,
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
@limiter.limit("20/minute")
async def get_working_day(
    request: Request,
    working_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_working_day_by_id(db, working_id)

@router.get(
    "/admin/working/user/{user_id}",
    response_model=List[schemas.DaysWorkingResponse]
)
@limiter.limit("20/minute")
async def get_user_working_days(
    request: Request,
    user_id: str = Path(..., description="User ID to retrieve working days"),
    skip: int = 0,
    limit: int = 200,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_working_day_by_user_id(db, user_id, skip, limit)
