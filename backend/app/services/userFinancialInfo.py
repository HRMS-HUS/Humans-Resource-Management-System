# services/userFinancialInfo.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException, status
from ..models import userFinancialInfo as models
from ..schemas import userFinancialInfo as schemas
from typing import List
from ..utils.redis_lock import DistributedLock
from ..utils.logger import logger
from ..services import users as user_service

class DatabaseOperationError(Exception):
    pass

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
            detail="Internal server error while validating user"
        )

async def create_financial_info(
    financial: schemas.UserFinancialInfoCreate, db: AsyncSession
):
    async with DistributedLock(f"financial_info:user:{financial.user_id}"):
        try:
            await _validate_user_exists(db, financial.user_id)
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
            await logger.info("Created financial info", {
                "financial_info_id": db_financial.financial_info_id,
                "user_id": financial.user_id
            })
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
        except Exception as e:
            await logger.error("Create financial info failed", error=e)
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
            await logger.info("Updated financial info", {
                "financial_info_id": financial_info_id,
                "user_id": db_financial.user_id
            })
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
        except Exception as e:
            await logger.error("Update financial info failed", error=e)
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
            await logger.warning("Financial info not found", {"financial_info_id": financial_info_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Financial info not found"
            )
        await logger.info("Retrieved financial info", {"financial_info_id": financial_info_id})
        return financial_info
    except HTTPException:
        raise
    except Exception as e:
        await logger.error("Get financial info by id failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def get_all_financial_info(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[models.UserFinancialInfo]:
    try:
        result = await db.execute(
            select(models.UserFinancialInfo).offset(skip).limit(limit)
        )
        financial_infos = result.scalars().all()
        await logger.info("Retrieved all financial info", {"count": len(financial_infos)})
        return financial_infos if financial_infos else []
    except Exception as e:
        await logger.error("Get all financial info failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def delete_financial_info(db: AsyncSession, financial_info_id: str):
    async with DistributedLock(f"financial_info:{financial_info_id}"):
        try:
            await get_financial_info_by_id(db, financial_info_id)

            stmt = delete(models.UserFinancialInfo).where(
                models.UserFinancialInfo.financial_info_id == financial_info_id
            )

            await db.execute(stmt)
            await db.commit()
            await logger.info("Deleted financial info", {"financial_info_id": financial_info_id})
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
        except Exception as e:
            await logger.error("Delete financial info failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def get_user_financial_info_by_user_id(db: AsyncSession, user_id: str):
    try:
        await _validate_user_exists(db, user_id)
        result = await db.execute(
            select(models.UserFinancialInfo).filter(
                models.UserFinancialInfo.user_id == user_id
            )
        )
        user_financial_info = result.scalar_one_or_none()

        if not user_financial_info:
            await logger.warning("Financial info not found", {"user_id": user_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Personal information not found for this user",
            )
        await logger.info("Retrieved financial info", {"user_id": user_id})
        return user_financial_info
    except HTTPException:
        raise
    except Exception as e:
        await logger.error("Get financial info failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
