from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException, status
from ..models import userPersonalInfo as models
from ..schemas import userPersonalInfo as schemas
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

async def create_user_info(user: schemas.UserInfoCreate, db: AsyncSession):
    async with DistributedLock(f"personal_info:user:{user.user_id}"):
        try:
            await _validate_user_exists(db, user.user_id)
            # Check if user already has personal info
            existing = await db.execute(
                select(models.UserPersonalInfo).filter(
                    models.UserPersonalInfo.user_id == user.user_id
                )
            )
            if existing.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Personal info already exists for this user",
                )

            db_user = models.UserPersonalInfo(**user.dict())
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            await logger.info("Created user personal info", {
                "personal_info_id": db_user.personal_info_id,
                "user_id": user.user_id
            })
            return db_user
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
            await logger.error("Create user personal info failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def get_user_personal_info_by_id(db: AsyncSession, personal_info_id: str):
    try:
        result = await db.execute(
            select(models.UserPersonalInfo).filter(
                models.UserPersonalInfo.personal_info_id == personal_info_id
            )
        )
        personal_info = result.scalar_one_or_none()

        if not personal_info:
            await logger.warning("Personal info not found", {"personal_info_id": personal_info_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Personal information not found",
            )
        await logger.info("Retrieved personal info", {"personal_info_id": personal_info_id})
        return personal_info
    except HTTPException:
        raise
    except Exception as e:
        await logger.error("Get personal info failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def get_user_personal_info_by_user_id(db: AsyncSession, user_id: str):
    try:
        result = await db.execute(
            select(models.UserPersonalInfo).filter(
                models.UserPersonalInfo.user_id == user_id
            )
        )
        personal_info = result.scalar_one_or_none()

        if not personal_info:
            await logger.warning("Personal info not found for user", {"user_id": user_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Personal information not found for this user",
            )
        await logger.info("Retrieved personal info for user", {"user_id": user_id})
        return personal_info
    except HTTPException:
        raise
    except Exception as e:
        await logger.error("Get personal info by user failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def update_user_personal_info(
    db: AsyncSession, personal_info_id: str, user: schemas.UserInfoUpdate
):
    async with DistributedLock(f"personal_info:{personal_info_id}"):
        try:
            db_user = await get_user_personal_info_by_id(db, personal_info_id)

            for key, value in user.dict().items():
                setattr(db_user, key, value)

            await db.commit()
            await db.refresh(db_user)
            await logger.info("Updated user personal info", {
                "personal_info_id": personal_info_id
            })
            return db_user
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
            await logger.error("Update user personal info failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def update_user_personal_info_no_department(
    db: AsyncSession, personal_info_id: str, user: schemas.UserInfoUpdateNoDepartment
):
    async with DistributedLock(f"personal_info:{personal_info_id}"):
        try:
            db_user = await get_user_personal_info_by_id(db, personal_info_id)

            for key, value in user.dict().items():
                if value is not None:  # Only update non-None values
                    setattr(db_user, key, value)

            await db.commit()
            await db.refresh(db_user)
            await logger.info("Updated user personal info without department", {
                "personal_info_id": personal_info_id
            })
            return db_user
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
            await logger.error("Update user personal info without department failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def update_user_personal_info_photo(
    db: AsyncSession, personal_info_id: str, photo_data: schemas.UserInfoPhotoUpdate
):
    async with DistributedLock(f"personal_info:{personal_info_id}"):
        try:
            db_user = await get_user_personal_info_by_id(db, personal_info_id)
            db_user.photo_url = photo_data.photo_url

            await db.commit()
            await db.refresh(db_user)
            await logger.info("Updated user profile photo", {
                "personal_info_id": personal_info_id
            })
            return db_user
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
            await logger.error("Update user profile photo failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def delete_user_personal_info(db: AsyncSession, personal_info_id: str):
    async with DistributedLock(f"personal_info:{personal_info_id}"):
        try:
            db_user = await get_user_personal_info_by_id(db, personal_info_id)
            await db.delete(db_user)
            await db.commit()
            await logger.info("Deleted user personal info", {
                "personal_info_id": personal_info_id
            })
            return {"message": "Personal info deleted successfully"}
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
            await logger.error("Delete user personal info failed", error=e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )


async def get_all_user_personal_info(db: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        result = await db.execute(
            select(models.UserPersonalInfo).offset(skip).limit(limit)
        )
        personal_infos = result.scalars().all()
        await logger.info("Retrieved all user personal info", {
            "count": len(personal_infos)
        })
        return personal_infos if personal_infos else []
    except Exception as e:
        await logger.error("Get all user personal info failed", error=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
