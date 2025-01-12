from sqlalchemy.ext.asyncio import AsyncSession
from ..models import payment as models
from ..schemas import payment as schemas
from fastapi import HTTPException, status
from sqlalchemy import select, delete, update
from typing import List
from ..utils.redis_lock import DistributedLock
from ..services import users as user_service
from ..utils.logger import logger

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
            detail=f"Internal server error while validating user"
        )

async def create_payment(db: AsyncSession, payment: schemas.PaymentCreate):
    try:
        await _validate_user_exists(db, payment.user_id)
        db_payment = models.Payment(**payment.dict())
        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)
        await logger.info("Created payment", {
            "payment_id": db_payment.payment_id,
            "user_id": payment.user_id,
            "amount": payment.payment_amount
        })
        return db_payment
    except Exception as e:
        await logger.error("Create payment failed", error=e)
        await db.rollback()
        raise

async def get_payment_by_id(db: AsyncSession, payment_id: str):
    try:
        result = await db.execute(
            select(models.Payment).filter(
                models.Payment.payment_id == payment_id
            )
        )
        payment = result.scalar_one_or_none()

        if not payment:
            await logger.warning("Payment not found", {"payment_id": payment_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        await logger.info("Retrieved payment", {"payment_id": payment_id})
        return payment
    except Exception as e:
        await logger.error("Get payment by id failed", error=e)
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
            await logger.warning("No payments found", {"user_id": user_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No payments found for this user"
            )
        await logger.info("Retrieved payments for user", {"user_id": user_id, "count": len(payments)})
        return payments
    except Exception as e:
        await logger.error("Get payments by user failed", error=e)
        raise

async def get_all_payments(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.Payment]:
    try:
        result = await db.execute(
            select(models.Payment).offset(skip).limit(limit)
        )
        payments = result.scalars().all()
        await logger.info("Retrieved all payments", {"count": len(payments), "skip": skip, "limit": limit})
        return payments
    except Exception as e:
        await logger.error("Get all payments failed", error=e)
        raise

async def update_payment(
    db: AsyncSession, payment_id: str, payment: schemas.PaymentUpdate
):
    async with DistributedLock(f"payment:{payment_id}"):
        try:
            query = (
                update(models.Payment)
                .where(models.Payment.payment_id == payment_id)
                .values(**payment.dict(exclude_unset=True))  # Added exclude_unset=True
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
