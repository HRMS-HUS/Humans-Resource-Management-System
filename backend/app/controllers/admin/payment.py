from fastapi import APIRouter, Depends, status, Query, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import payment as schemas
from ...models import users as models
from ...services import payment as services
from ...utils import jwt
from ...configs.database import get_db
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post(
    "/admin/payment",
    response_model=schemas.PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
async def create_payment(
    request: Request,
    payment: schemas.PaymentCreate = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.create_payment(db, payment)

@router.get(
    "/admin/payment/{payment_id}",
    response_model=schemas.PaymentResponse
)
@limiter.limit("10/minute")
async def get_payment_by_id(
    request: Request,
    payment_id: str = Path(..., description="Payment ID to retrieve"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_payment_by_id(db, payment_id)

@router.put(
    "/admin/payment/{payment_id}",
    response_model=schemas.PaymentResponse
)
@limiter.limit("5/minute")
async def update_payment(
    request: Request,
    payment: schemas.PaymentUpdate = Query(...),
    payment_id: str = Path(..., description="Payment ID to update"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.update_payment(db, payment_id, payment)

@router.delete("/admin/payment/{payment_id}")
@limiter.limit("3/minute")
async def delete_payment(
    request: Request,
    payment_id: str = Path(..., description="Payment ID to delete"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.delete_payment(db, payment_id)

@router.get(
    "/admin/payment",
    response_model=List[schemas.PaymentResponse]
)
@limiter.limit("10/minute")
async def get_all_payments(
    request: Request,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_all_payments(db, skip=skip, limit=limit)

@router.get(
    "/admin/payment/user/{user_id}",
    response_model=List[schemas.PaymentResponse]
)
@limiter.limit("10/minute")
async def get_payments_by_user_id(
    request: Request,
    user_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_current_admin),
):
    return await services.get_payments_by_user_id(db, user_id)
