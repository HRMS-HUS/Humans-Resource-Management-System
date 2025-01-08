from sqlalchemy.ext.asyncio import AsyncSession
from ..models import users as models_user
from ..schemas import users as schemas_user
from ..models import authentication as models
from ..models import users as user_model
from ..schemas import authentication as schemas
from fastapi import HTTPException,status
from sqlalchemy import select, and_, func, text, delete
from ..utils import crypto
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import userPersonalInfo as models_user_info
from ..models import users as models_user
from ..schemas import users as schemas_user
from ..models import authentication as models
from ..schemas import authentication as schemas
from ..services import users
from fastapi import HTTPException, status, Depends, APIRouter, Query
from sqlalchemy import select, and_, func, text, delete
from ..utils import crypto, jwt, email, otp
from ..configs.database import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import os
from pathlib import Path

async def get_user_id_by_username(db: AsyncSession, username: str) -> int:
    stmt = select(user_model.Users.user_id).where(user_model.Users.username == username)
    result = await db.execute(stmt)
    user_id = result.scalars().first()
    
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user_id

async def create_otp_code(db: AsyncSession, username: str, otp_code: str):
    user_id = await get_user_id_by_username(db, username)
    expired_time = func.now() - text("interval '10 minutes'")

    stmt = (
        select(models.OTPCode)
        .where(
            models.OTPCode.user_id == user_id,
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
        user_id = user_id,
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

async def register(
    user: schemas_user.UserCreate = Query(...), db: AsyncSession = Depends(get_db)
):
    stmt = select(models_user.Users).where(models_user.Users.username == user.username)
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already register"
        )

    user.password = crypto.hash_password(user.password)
    return await users.create_user(db, user)


async def login(form_data: OAuth2PasswordRequestForm, db: AsyncSession):

    stmt = select(models_user.Users).where(
        models_user.Users.username == form_data.username
    )
    result = await db.execute(stmt)
    user_info = result.scalars().first()

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db_user = user_info

    if not crypto.verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = jwt.timedelta(minutes=jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await jwt.create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def forgot_password(
    request: schemas.ForgotPassword = Query(...), db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(models_user.Users, models_user_info.UserPersonalInfo.email)
        .join(
            models_user_info.UserPersonalInfo,
            models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id,
        )
        .where(models_user.Users.username == request.username)
    )
    result = await db.execute(stmt)
    user_info = result.first()
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User Not Found"
        )
    email_user = user_info[1]
    reset_code = otp.create_otp()
    await create_otp_code(db, request.username, reset_code)
    subject = "Reset code"
    recipient = [email_user]

    template_path = (
        Path(__file__).parent.parent / "templates" / "otp_email_forgot_password.html"
    )
    with open(template_path, "r") as file:
        html_template = file.read()

    message = html_template.format(username=request.username, reset_code=reset_code)

    await email.send_mail(subject, recipient, message)

    return {"message": "Password reset email sent"}


async def reset_passwords(
    request: schemas.ResetPassword = Query(...), db: AsyncSession = Depends(get_db)
):
    otp_code = await check_otp_code(db, request.otp_code)

    if not otp_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reset Code Not Found"
        )

    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="new same confirm"
        )

    await reset_password(db, request.new_password, request.username)
    return {"message": "Password reset successful"}