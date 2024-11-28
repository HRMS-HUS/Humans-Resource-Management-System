from sqlalchemy.ext.asyncio import AsyncSession
from ..models import userPersonalInfo as models
from ..schemas import userPersonalInfo as schemas
from fastapi import HTTPException,status

async def create_user_info(db: AsyncSession, user: schemas.UserInfoCreate):
    db_user = models.UserPersonalInfo(
        email=user.email,
        fullname = user.fullname
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user