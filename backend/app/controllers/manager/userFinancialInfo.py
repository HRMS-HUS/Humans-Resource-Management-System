from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import userFinancialInfo as schemas
from ...services import userFinancialInfo as services
from ...services import userPersonalInfo as personal_info_services
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

async def validate_user_in_department(db: AsyncSession, user_id: str, manager_id: str):
    # Get manager's department
    dept = await dept_services.get_department_by_manager_id(db, manager_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager has no associated department"
        )
    
    # Get user's department
    user_info = await personal_info_services.get_user_personal_info_by_user_id(db, user_id)
    if user_info.department_id != dept.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User not in manager's department"
        )
    return dept

@router.post("/manager/financial", response_model=schemas.UserFinancialInfoResponse)
@limiter.limit("5/minute")
async def create_financial_info(
    request: Request,
    financial: schemas.UserFinancialInfoCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    await validate_user_in_department(db, financial.user_id, current_user.user_id)
    return await services.create_financial_info(financial, db)

@router.get("/manager/financial/{financial_info_id}", response_model=schemas.UserFinancialInfoResponse)
@limiter.limit("10/minute")
async def get_financial_info(
    request: Request,
    financial_info_id: str = Path(..., description="Financial Info ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    financial_info = await services.get_financial_info_by_id(db, financial_info_id)
    await validate_user_in_department(db, financial_info.user_id, current_user.user_id)
    return financial_info

@router.get("/manager/financial/user/{user_id}", response_model=schemas.UserFinancialInfoResponse)
@limiter.limit("10/minute")
async def get_user_financial_info(
    request: Request,
    user_id: str = Path(..., description="User ID to retrieve financial info"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    await validate_user_in_department(db, user_id, current_user.user_id)
    return await services.get_user_financial_info_by_user_id(db, user_id)

@router.put("/manager/financial/{financial_info_id}", response_model=schemas.UserFinancialInfoResponse)
@limiter.limit("5/minute")
async def update_financial_info(
    request: Request,
    financial_info_id: str = Path(..., description="Financial Info ID to update"),
    financial: schemas.UserFinancialInfoUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Validate user belongs to manager's department
    existing_info = await services.get_financial_info_by_id(db, financial_info_id)
    await validate_user_in_department(db, existing_info.user_id, current_user.user_id)
    
    return await services.update_financial_info(db, financial_info_id, financial)

@router.delete("/manager/financial/{financial_info_id}")
@limiter.limit("3/minute")
async def delete_financial_info(
    request: Request,
    financial_info_id: str = Path(..., description="Financial Info ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    # Validate user belongs to manager's department
    existing_info = await services.get_financial_info_by_id(db, financial_info_id)
    await validate_user_in_department(db, existing_info.user_id, current_user.user_id)
    
    return await services.delete_financial_info(db, financial_info_id)
