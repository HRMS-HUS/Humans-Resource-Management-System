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
from ..configs.redis import redis_client
from ..utils.redis_lock import DistributedLock

async def get_user_id_by_username(db: AsyncSession, username: str) -> int:
    stmt = select(user_model.Users.user_id).where(user_model.Users.username == username)
    result = await db.execute(stmt)
    user_id = result.scalars().first()
    
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user_id

async def get_user_id_by_email(db: AsyncSession, email: str) -> int:
    stmt = (
        select(models_user.Users.user_id)
        .join(
            models_user_info.UserPersonalInfo,
            models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id,
        )
        .where(models_user_info.UserPersonalInfo.email == email)
    )
    result = await db.execute(stmt)
    user_id = result.scalars().first()
    
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    
    return user_id

# async def create_otp_code(db: AsyncSession, email: str, otp_code: str):
#     user_id = await get_user_id_by_email(db, email)
#     expired_time = func.now() - text("interval '10 minutes'")

#     stmt = (
#         select(models.OTPCode)
#         .where(
#             models.OTPCode.user_id == user_id,
#         )
#     )
#     result = await db.execute(stmt)
#     old_code = result.scalars().first()

#     if old_code:
#         await db.execute(
#             delete(models.OTPCode)
#             .where(models.OTPCode.otp_id == old_code.otp_id)
#         )
#         await db.commit()
    
#     new_otp_code = models.OTPCode(
#         user_id = user_id,
#         otp_code = otp_code
#     )
#     db.add(new_otp_code)
#     await db.commit()
#     await db.refresh(new_otp_code)
#     return new_otp_code

# async def check_otp_code(db: AsyncSession, otp_code: str):
#     expired_time = func.now() - text("interval '10 minutes'")
#     stmt = (
#         select(models.OTPCode)
#         .where(
#             and_(
#                 models.OTPCode.status == models.StatusEnum.Active,
#                 models.OTPCode.otp_code == otp_code,
#                 models.OTPCode.expired_in >= expired_time
#             )
#         )
#     )
    
#     result = await db.execute(stmt)
#     db_code = result.scalars().first()
    
#     if not db_code:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset password code")
    
#     return db_code

async def reset_password(db: AsyncSession, new_password: str, email: str):
    stmt = (
        select(
            models_user.Users
        )
        .join(
            models_user_info.UserPersonalInfo,
            models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id,
        )
        .where(models_user_info.UserPersonalInfo.email == email)
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
    # Check if input is email or username
    is_email = '@' in form_data.username

    if (is_email):
        # Query user by email
        stmt = (
            select(models_user.Users)
            .join(
                models_user_info.UserPersonalInfo,
                models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id,
            )
            .where(models_user_info.UserPersonalInfo.email == form_data.username)
        )
    else:
        # Query user by username
        stmt = select(models_user.Users).where(
            models_user.Users.username == form_data.username
        )

    result = await db.execute(stmt)
    user_info = result.scalars().first()

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db_user = user_info

    if not crypto.verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = jwt.timedelta(minutes=jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await jwt.create_access_token(
        data={"sub": db_user.user_id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
#     # Query to get both user and email information
#     stmt = (
#         select(
#             models_user.Users,
#             models_user_info.UserPersonalInfo.email
#         )
#         .join(
#             models_user_info.UserPersonalInfo, 
#             models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id
#         )
#         .where(models_user.Users.username == form_data.username)
#     )
#     result = await db.execute(stmt)
#     user_info = result.first()
    
#     if not user_info:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect Username or Password"
#         )
        
#     db_user, email_user = user_info
    
#     if not crypto.verify_password(form_data.password, db_user.password):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect Username or Password"
#         )
    
#     try:
#         # Generate and store OTP
#         otp_code = otp.create_otp()
#         # await create_otp_code(db, email_user, otp_code)
#         await redis_client.setex(db_user.username, 600, otp_code)
#         value = await redis_client.get(db_user.username)
#         if value is None:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Failed to retrieve OTP from Redis"
#             )  # Xử lý khi không có giá trị
#         # Send email with OTP
#         subject = "OTP for Login"
#         recipient = [email_user]
        
#         template_path = Path(__file__).parent.parent / 'templates' / 'otp_email_login.html'
#         with open(template_path, 'r') as file:
#             html_template = file.read()
        
#         message = html_template.format(username=db_user.username, otp_code=otp_code)
        
#         await email.send_mail(subject, recipient, message)
        
#         return value
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error sending OTP: {str(e)}"
#         )

# async def verify_otp(request: schemas.VerifyOTP = Query(...), db: AsyncSession = Depends(get_db)):
#     redis_otp = await redis_client.get(request.username)
#     if redis_otp is None:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Failed to retrieve OTP from Redis"
#         )  # Xử lý khi không có giá trị
#     if redis_otp != request.otp_code:
#             raise HTTPException(
#                 status_code=400, detail="Invalid OTP"
#             )
#     await redis_client.delete(request.username)

#     access_token_expires = jwt.timedelta(minutes=jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = await jwt.create_access_token(
#         data={"sub": request.username},
#         expires_delta=access_token_expires
#     )
    
#     await redis_client.setex(request.username, int(access_token_expires.total_seconds()), access_token)

#     return {"access_token": access_token, "token_type": "bearer"}

async def forgot_password(
    request: schemas.ForgotPassword = Query(...), db: AsyncSession = Depends(get_db)
):
    async with DistributedLock(f"forgot_password:{request.email}"):
        stmt = (
            select(models_user.Users, models_user_info.UserPersonalInfo)
            .join(
                models_user_info.UserPersonalInfo,
                models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id,
            )
            .where(models_user_info.UserPersonalInfo.email == request.email)
        )
        result = await db.execute(stmt)
        user_info = result.first()
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email Not Found"
            )
        
        username = user_info[0].username
        email_user = user_info[1].email
        reset_code = otp.create_otp()
        await redis_client.setex(email_user, 600, reset_code)
        subject = "Reset code"
        recipient = [email_user]

        template_path = (
            Path(__file__).parent.parent / "templates" / "otp_email_forgot_password.html"
        )
        with open(template_path, "r") as file:
            html_template = file.read()

        message = html_template.format(username=username, reset_code=reset_code)

        await email.send_mail(subject, recipient, message)

        return {"message": "Password reset email sent"}


async def reset_passwords(
    request: schemas.ResetPassword = Query(...), db: AsyncSession = Depends(get_db)
):
    async with DistributedLock(f"reset_password:{request.email}"):
        redis_otp = await redis_client.get(request.email)
        if redis_otp is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve OTP from Redis"
            )  # Xử lý khi không có giá trị

        if redis_otp != request.otp_code:
                raise HTTPException(
                    status_code=400, detail="Invalid OTP"
                )
        await redis_client.delete(request.email)

        if request.new_password != request.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="new same confirm"
            )

        await reset_password(db, request.new_password, request.email)
        return {"message": "Password reset successfully"}