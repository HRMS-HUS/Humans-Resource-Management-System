from sqlalchemy.ext.asyncio import AsyncSession
from ..models import userPersonalInfo as models
from ..schemas import userPersonalInfo as schemas
from fastapi import HTTPException,status

async def create_user_info(db: AsyncSession, user: schemas.UserInfoCreate):
    db_user = models.UserPersonalInfo(
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