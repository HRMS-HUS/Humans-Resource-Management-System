# routers/userFinancialInfo.py
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import userFinancialInfo as schemas
from ..models import users as models
from ..controllers.manager import userFinancialInfo as controller
from ..utils import jwt
from typing import List

router = APIRouter(prefix="/api", tags=["financial_info"])

@router.post(
    "/financial_info",
    response_model=schemas.UserFinancialInfoResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_financial_info(
    financial: schemas.UserFinancialInfoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await controller.create_financial_info_controller(db, financial)

@router.get(
    "/financial_info/{financial_info_id}",
    response_model=schemas.UserFinancialInfoResponse
)
async def get_financial_info(
    financial_info_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await controller.get_financial_info_by_id_controller(db, financial_info_id)

@router.get(
    "/financial_info",
    response_model=List[schemas.UserFinancialInfoResponse]
)
async def get_all_financial_info(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await controller.get_all_financial_info_controller(db, skip, limit)

@router.put(
    "/financial_info/{financial_info_id}",
    response_model=schemas.UserFinancialInfoResponse
)
async def update_financial_info(
    financial_info_id: str,
    financial: schemas.UserFinancialInfoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await controller.update_financial_info_controller(
        db, financial_info_id, financial
    )

@router.delete("/financial_info/{financial_info_id}")
async def delete_financial_info(
    financial_info_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(jwt.get_current_admin)
):
    return await controller.delete_financial_info_controller(db, financial_info_id)

@router.get("/me/financial_info", response_model=schemas.UserFinancialInfoResponse)
async def get_current_user_personal_info(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):

    return await controller.get_user_personal_info_by_user_id_controller(
        db, current_user.user_id
    )

@router.get("/financial_info/user/{user_id}", response_model=schemas.UserFinancialInfoResponse)
async def get_financial_info_by_user_id(
    user_id: str = Path(..., description="User ID to retrieve personal info"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):

    return await controller.get_user_personal_info_by_user_id_controller(db, user_id)
