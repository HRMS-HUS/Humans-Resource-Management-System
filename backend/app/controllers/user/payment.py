from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import payment as schemas
from ...models import users as models
from ...services import payment as services
from ...utils import jwt
from ...configs.database import get_db
from typing import List

router = APIRouter()

@router.get(
    "/me/payment",
    response_model=List[schemas.PaymentResponse]
)
async def get_current_user_payments(
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    return await services.get_payments_by_user_id(db, current_user.user_id)

@router.get(
    "/me/payment/{payment_id}",
    response_model=schemas.PaymentResponse
)
async def get_payment_me(
    payment_id: str = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.Users = Depends(jwt.get_active_user),
):
    payment = await services.get_payment_by_id(db, payment_id)
    if payment.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this payment"
        )
    return payment
