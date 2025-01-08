from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import HTTPException, status
from ..models import userPersonalInfo as models
from ..schemas import userPersonalInfo as schemas
from typing import List
from ..utils.redis_lock import DistributedLock


async def create_user_info(user: schemas.UserInfoCreate, db: AsyncSession):
    async with DistributedLock(f"personal_info:user:{user.user_id}"):
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
        return db_user


async def get_user_personal_info_by_id(db: AsyncSession, personal_info_id: str):
    result = await db.execute(
        select(models.UserPersonalInfo).filter(
            models.UserPersonalInfo.personal_info_id == personal_info_id
        )
    )
    personal_info = result.scalar_one_or_none()

    if not personal_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal information not found",
        )

    return personal_info


async def get_user_personal_info_by_user_id(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(models.UserPersonalInfo).filter(
            models.UserPersonalInfo.user_id == user_id
        )
    )
    personal_info = result.scalar_one_or_none()

    if not personal_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal information not found for this user",
        )

    return personal_info


async def update_user_personal_info(
    db: AsyncSession, personal_info_id: str, user: schemas.UserInfoCreate
):
    async with DistributedLock(f"personal_info:{personal_info_id}"):
        db_user = await get_user_personal_info_by_id(db, personal_info_id)

        for key, value in user.dict().items():
            setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)
        return db_user


async def delete_user_personal_info(db: AsyncSession, personal_info_id: str):
    async with DistributedLock(f"personal_info:{personal_info_id}"):
        db_user = await get_user_personal_info_by_id(db, personal_info_id)
        await db.delete(db_user)
        await db.commit()
        return {"message": "Personal info deleted successfully"}


async def get_all_user_personal_info(db: AsyncSession, skip: int = 0, limit: int = 100):

    result = await db.execute(select(models.UserPersonalInfo).offset(skip).limit(limit))

    personal_infos = result.scalars().all()

    if not personal_infos:
        return []

    return personal_infos
