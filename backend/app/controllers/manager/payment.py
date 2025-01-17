from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import payment as schemas
from ...services import payment as services
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

@router.post("/manager/payment", response_model=schemas.PaymentResponse)
@limiter.limit("5/minute")
async def create_payment(
    request: Request,
    payment: schemas.PaymentCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    await validate_user_in_department(db, payment.user_id, current_user.user_id)
    return await services.create_payment(db, payment)

@router.get("/manager/payment/{payment_id}", response_model=schemas.PaymentResponse)
@limiter.limit("10/minute")
async def get_payment(
    request: Request,
    payment_id: str = Path(..., description="Payment ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    payment = await services.get_payment_by_id(db, payment_id)
    await validate_user_in_department(db, payment.user_id, current_user.user_id)
    return payment

@router.get("/manager/payment/user/{user_id}", response_model=List[schemas.PaymentResponse])
@limiter.limit("10/minute")
async def get_user_payments(
    request: Request,
    user_id: str = Path(..., description="User ID to retrieve payments"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    await validate_user_in_department(db, user_id, current_user.user_id)
    return await services.get_payments_by_user_id(db, user_id)

@router.put("/manager/payment/{payment_id}", response_model=schemas.PaymentResponse)
@limiter.limit("5/minute")
async def update_payment(
    request: Request,
    payment_id: str = Path(..., description="Payment ID to update"),
    payment: schemas.PaymentUpdate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    existing_payment = await services.get_payment_by_id(db, payment_id)
    await validate_user_in_department(db, existing_payment.user_id, current_user.user_id)
    return await services.update_payment(db, payment_id, payment)

@router.delete("/manager/payment/{payment_id}")
@limiter.limit("3/minute")
async def delete_payment(
    request: Request,
    payment_id: str = Path(..., description="Payment ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_manager)
):
    existing_payment = await services.get_payment_by_id(db, payment_id)
    await validate_user_in_department(db, existing_payment.user_id, current_user.user_id)
    return await services.delete_payment(db, payment_id)
