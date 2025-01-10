# services/userFinancialInfo.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException, status
from ..models import userFinancialInfo as models
from ..schemas import userFinancialInfo as schemas
from typing import List
from ..utils.redis_lock import DistributedLock

class DatabaseOperationError(Exception):
    pass

async def create_financial_info(
    financial: schemas.UserFinancialInfoCreate, db: AsyncSession
):
    async with DistributedLock(f"financial_info:user:{financial.user_id}"):
        try:
            # Check if user already has financial info
            existing = await db.execute(
                select(models.UserFinancialInfo).filter(
                    models.UserFinancialInfo.user_id == financial.user_id
                )
            )
            if existing.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Financial info already exists for this user",
                )

            db_financial = models.UserFinancialInfo(**financial.dict())
            db.add(db_financial)
            await db.commit()
            await db.refresh(db_financial)
            return db_financial
        except HTTPException:
            await db.rollback()
            raise
        except DatabaseOperationError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def update_financial_info(
    db: AsyncSession, financial_info_id: str, financial: schemas.UserFinancialInfoUpdate
):
    async with DistributedLock(f"financial_info:{financial_info_id}"):
        try:
            db_financial = await get_financial_info_by_id(db, financial_info_id)

            for key, value in financial.dict().items():
                setattr(db_financial, key, value)

            await db.commit()
            await db.refresh(db_financial)
            return db_financial
        except HTTPException:
            await db.rollback()
            raise
        except DatabaseOperationError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def get_financial_info_by_id(db: AsyncSession, financial_info_id: str):
    try:
        result = await db.execute(
            select(models.UserFinancialInfo).filter(
                models.UserFinancialInfo.financial_info_id == financial_info_id
            )
        )
        financial_info = result.scalar_one_or_none()

        if not financial_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Financial info not found"
            )
        return financial_info
    except HTTPException:
        raise


async def get_all_financial_info(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.UserFinancialInfo]:
    result = await db.execute(
        select(models.UserFinancialInfo).offset(skip).limit(limit)
    )
    financial_infos = result.scalars().all()
    return financial_infos if financial_infos else []


async def delete_financial_info(db: AsyncSession, financial_info_id: str):
    async with DistributedLock(f"financial_info:{financial_info_id}"):
        try:
            await get_financial_info_by_id(db, financial_info_id)

            stmt = delete(models.UserFinancialInfo).where(
                models.UserFinancialInfo.financial_info_id == financial_info_id
            )

            await db.execute(stmt)
            await db.commit()
            return {"detail": "Financial info deleted successfully"}
        except HTTPException:
            await db.rollback()
            raise
        except DatabaseOperationError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def get_user_financial_info_by_user_id(db: AsyncSession, user_id: str):
    try:
        result = await db.execute(
            select(models.UserFinancialInfo).filter(
                models.UserFinancialInfo.user_id == user_id
            )
        )
        user_financial_info = result.scalar_one_or_none()

        if not user_financial_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Personal information not found for this user",
            )
        return user_financial_info
    except HTTPException:
        raise
