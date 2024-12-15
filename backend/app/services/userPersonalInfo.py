from sqlalchemy.ext.asyncio import AsyncSession
from ..models import userPersonalInfo as models
from ..schemas import userPersonalInfo as schemas
from fastapi import HTTPException,status
from sqlalchemy import select, delete, update

async def create_user_info(db: AsyncSession, user: schemas.UserInfoCreate):
    db_user = models.UserPersonalInfo(
        user_id = user.user_id,
        fullname = user.fullname,
        citizen_card = user.citizen_card,
        date_of_birth = user.date_of_birth,
        sex = user.sex,
        phone = user.phone,
        email = user.email,
        marital_status = user.marital_status,
        address = user.address,
        city = user.city,
        country = user.country
    )
    
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
            detail="Personal information not found"
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
            detail="Personal information not found for this user"
        )
    
    return personal_info

async def update_user_personal_info(
    db: AsyncSession, 
    personal_info_id: str, 
    user: schemas.UserInfoCreate
):
    
    await get_user_personal_info_by_id(db, personal_info_id)
    
    update_data = {
        "user_id": user.user_id,
        "fullname": user.fullname,
        "citizen_card": user.citizen_card,
        "date_of_birth": user.date_of_birth,
        "sex": user.sex,
        "phone": user.phone,
        "email": user.email,
        "marital_status": user.marital_status,
        "address": user.address,
        "city": user.city,
        "country": user.country
    }
    
    stmt = update(models.UserPersonalInfo).where(
        models.UserPersonalInfo.personal_info_id == personal_info_id
    ).values(**update_data)
    
    result = await db.execute(stmt)
    await db.commit()
    
    updated_info = await get_user_personal_info_by_id(db, personal_info_id)
    return updated_info

async def delete_user_personal_info(db: AsyncSession, personal_info_id: str):
    
    await get_user_personal_info_by_id(db, personal_info_id)
    
    stmt = delete(models.UserPersonalInfo).where(
        models.UserPersonalInfo.personal_info_id == personal_info_id
    )
    
    await db.execute(stmt)
    await db.commit()
    
    return {"detail": "Personal information deleted successfully"}

async def get_all_user_personal_info(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
):
    
    result = await db.execute(
        select(models.UserPersonalInfo)
        .offset(skip)
        .limit(limit)
    )
    
    personal_infos = result.scalars().all()
    
    
    if not personal_infos:
        return []
    
    return personal_infos