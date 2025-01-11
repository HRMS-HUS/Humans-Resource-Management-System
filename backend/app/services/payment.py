from sqlalchemy.ext.asyncio import AsyncSession
from ..models import payment as models
from ..schemas import payment as schemas
from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from typing import List
from ..utils.redis_lock import DistributedLock
from ..services import users as user_service

async def _validate_user_exists(db: AsyncSession, user_id: str):
    try:
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error while validating user: {str(e)}"
        )

async def create_payment(db: AsyncSession, payment: schemas.PaymentCreate):
    await _validate_user_exists(db, payment.user_id)
    
    async with DistributedLock(f"payment:user:{payment.user_id}"):
        try:
            db_payment = models.Payment(
                user_id=payment.user_id,
                payment_method=payment.payment_method,
                payment_month=payment.payment_month,
                payment_date=payment.payment_date,
                payment_amount=payment.payment_amount,
                payment_fine=payment.payment_fine,
                comments=payment.comments
            )
            db.add(db_payment)
            await db.commit()
            await db.refresh(db_payment)
            return db_payment
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

async def get_payment_by_id(db: AsyncSession, payment_id: str):
    try:
        result = await db.execute(
            select(models.Payment).filter(
                models.Payment.payment_id == payment_id
            )
        )
        payment = result.scalar_one_or_none()

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        return payment
    except HTTPException:
        raise

async def get_payments_by_user_id(db: AsyncSession, user_id: str):
    try:
        result = await db.execute(
            select(models.Payment).filter(
                models.Payment.user_id == user_id
            )
        )
        payments = result.scalars().all()

        if not payments:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No payments found for this user"
            )
        return payments
    except HTTPException:
        raise

async def get_all_payments(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.Payment]:
    result = await db.execute(
        select(models.Payment).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_payment(
    db: AsyncSession, payment_id: str, payment: schemas.PaymentUpdate
):
    async with DistributedLock(f"payment:{payment_id}"):
        try:
            query = (
                update(models.Payment)
                .where(models.Payment.payment_id == payment_id)
                .values(payment.dict(exclude_unset=True))
            )

            result = await db.execute(query)
            await db.commit()

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found"
                )

            return await get_payment_by_id(db, payment_id)
        except HTTPException:
            await db.rollback()
            raise
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

async def delete_payment(db: AsyncSession, payment_id: str):
    async with DistributedLock(f"payment:{payment_id}"):
        try:
            result = await db.execute(
                delete(models.Payment).where(
                    models.Payment.payment_id == payment_id
                )
            )
            await db.commit()

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found"
                )

            return {"message": "Payment deleted successfully"}
        except HTTPException:
            await db.rollback()
            raise
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
