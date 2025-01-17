# routers/userFinancialInfo.py
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ...configs.database import get_db
from ...schemas import userFinancialInfo as schemas
from ...models import users as models
from ...services import userFinancialInfo as services
from ...utils import jwt
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post(
    "/admin/financial_info",
    response_model=schemas.UserFinancialInfoResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("20/minute")
async def create_financial_info(
    request: Request,
    financial: schemas.UserFinancialInfoCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.create_financial_info(financial, db)

@router.get(
    "/admin/financial_info/{financial_info_id}",
    response_model=schemas.UserFinancialInfoResponse
)
@limiter.limit("20/minute")
async def get_financial_info(
    request: Request,
    financial_info_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_financial_info_by_id(db, financial_info_id)

@router.get(
    "/admin/financial_info",
    response_model=List[schemas.UserFinancialInfoResponse]
)
@limiter.limit("20/minute")
async def get_all_financial_info(
    request: Request,
    skip: int = 0,
    limit: int = 200,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.get_all_financial_info(db, skip, limit)

@router.put(
    "/admin/financial_info/{financial_info_id}",
    response_model=schemas.UserFinancialInfoResponse
)
@limiter.limit("20/minute")
async def update_financial_info(
    request: Request,
    financial_info_id: str = Path(...),
    financial: schemas.UserFinancialInfoUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.update_financial_info(
        db, financial_info_id, financial
    )

@router.delete("/financial_info/{financial_info_id}")
@limiter.limit("3/minute")
async def delete_financial_info(
    request: Request,
    financial_info_id: str  = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await services.delete_financial_info(db, financial_info_id)

@router.get("/admin/financial_info/user/{user_id}", response_model=schemas.UserFinancialInfoResponse)
@limiter.limit("20/minute")
async def get_financial_info_by_user_id(
    request: Request,
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await services.get_user_financial_info_by_user_id(db, user_id)
