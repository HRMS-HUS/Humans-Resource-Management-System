from sqlalchemy.ext.asyncio import AsyncSession
from ..models import users as models_user
from ..schemas import users as schemas_user
from ..models import auth as models
from ..schemas import auth as schemas
from fastapi import HTTPException,status
from sqlalchemy import select, and_, func, text, delete
from ..utils import crypto

async def create_otp_code(db: AsyncSession, username: str, otp_code: str):
    expired_time = func.now() - text("interval '10 minutes'")

    stmt = (
        select(models.OTPCode)
        .where(
            models.OTPCode.username == username,
        )
    )
    result = await db.execute(stmt)
    old_code = result.scalars().first()

    if old_code:
        await db.execute(
            delete(
                models.OTPCode
            )
            .where(models.OTPCode.otp_id == old_code.otp_id)
        )
        await db.commit()
    
    new_otp_code = models.OTPCode(
        username = username,
        otp_code = otp_code
    )
    db.add(new_otp_code)
    await db.commit()
    await db.refresh(new_otp_code)
    return new_otp_code

async def check_otp_code(db: AsyncSession, otp_code: str):
    expired_time = func.now() - text("interval '10 minutes'")
    stmt = (
        select(models.OTPCode)
        .where(
            and_(
                models.OTPCode.status == models.StatusEnum.Active,
                models.OTPCode.otp_code == otp_code,
                models.OTPCode.expired_in >= expired_time
            )
        )
    )
    
    result = await db.execute(stmt)
    db_code = result.scalars().first()
    
    if not db_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset password code")
    
    return db_code

async def reset_password(db: AsyncSession,new_password: str, username: str):
    stmt = (
        select(
            models_user.Users
            )
        .where(models_user.Users.username == username)
    )
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Not Found")

    user.password = crypto.hash_password(new_password)
    db.add(user)
    await db.commit()
    return user.password
