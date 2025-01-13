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
from ..utils.logger import logger
from ..services import daysWorking as services


async def register(
    user: schemas_user.UserCreate = Query(...), db: AsyncSession = Depends(get_db)
):
    stmt = select(models_user.Users).where(models_user.Users.username == user.username)
    result = await db.execute(stmt)
    db_user = result.scalars().first()

    if (db_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already register"
        )

    user.password = crypto.hash_password(user.password)
    return await users.create_user(db, user)


async def login(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
    try:
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

        # Check if user is admin - reject if true
        if db_user.role == user_model.RoleEnum.Admin:
            await logger.warning("Admin attempted to use regular login", {"username": form_data.username})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Administrators must use 2FA login. Please use the admin login endpoint.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not crypto.verify_password(form_data.password, db_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Add check for inactive user
        if not db_user.status == user_model.StatusEnum.Active:
            await logger.warning("Login attempt by inactive user", {"username": form_data.username})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is inactive. Please contact administrator.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = jwt.timedelta(minutes=jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = jwt.timedelta(days=jwt.REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Create access and refresh tokens
        access_token = await jwt.create_access_token(
            data={"sub": db_user.user_id}, 
            expires_delta=access_token_expires
        )
        refresh_token = await jwt.create_refresh_token(
            data={"sub": db_user.user_id}
        )

        # Store tokens in Redis
        await redis_client.setex(
            db_user.user_id, 
            int(access_token_expires.total_seconds()), 
            access_token
        )
        await redis_client.setex(
            f"refresh_token:{db_user.user_id}",
            int(refresh_token_expires.total_seconds()),
            refresh_token
        )

        await logger.info("User logged in", {"username": form_data.username})
        
        # Create attendance record
        await services.create_attendance_record(db_user.user_id, db)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "role": db_user.role
        }
    except Exception as e:
        await logger.error("Login failed", error=e)
        raise

async def logout_me(current_user: models_user.Users, db: AsyncSession):
    try:
        # Extract user_id from the User object
        user_id = str(current_user.user_id)
        
        # Update attendance record with logout time
        await services.update_attendance_logout(user_id, db)
        
        # Remove access token from Redis using user_id as key
        deleted = await redis_client.delete(user_id)
        if deleted == 0:
            await logger.warning("Logout failed: Token not found", {"user_id": user_id})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not logged in or token already expired"
            )
        await logger.info("User logged out successfully", {"user_id": user_id})
        return {"detail": "Logged out successfully"}
    except Exception as e:
        await logger.error("Error during logout", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during logout: {str(e)}"
        )

async def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        # Check if input is email or username
        is_email = '@' in form_data.username

        if is_email:
            # Query user by email
            stmt = (
                select(models_user.Users, models_user_info.UserPersonalInfo.email)
                .join(
                    models_user_info.UserPersonalInfo,
                    models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id
                )
                .where(models_user_info.UserPersonalInfo.email == form_data.username)
            )
        else:
            # Query user by username
            stmt = (
                select(models_user.Users, models_user_info.UserPersonalInfo.email)
                .join(
                    models_user_info.UserPersonalInfo,
                    models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id
                )
                .where(models_user.Users.username == form_data.username)
            )

        
        result = await db.execute(stmt)
        user_info = result.first()

        if not user_info:
            await logger.warning("Login attempt failed: Incorrect Username or Password or Email not found", {"username": form_data.username})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect Username or Password or Email not found"
            )
        
        db_user, email_user = user_info

        if not crypto.verify_password(form_data.password, db_user.password):
            await logger.warning("Login attempt failed: Incorrect Password", {"username": form_data.username})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect Username or Password"
            )
        # Add check for inactive user
        if not db_user.status == user_model.StatusEnum.Active:
            await logger.warning("Login attempt by inactive user", {"username": form_data.username})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is inactive. Please contact administrator.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not db_user.role == user_model.RoleEnum.Admin:
            await logger.warning("Login attempt by non-admin user", {"username": form_data.username})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate and store OTP
        otp_code = otp.create_otp()
        await redis_client.setex(db_user.user_id, 600, otp_code)
        # Send email with OTP
        subject = "OTP for Login"
        recipient = [email_user]
        
        template_path = Path(__file__).parent.parent / 'templates' / 'otp_email_login.html'
        with open(template_path, 'r') as file:
            html_template = file.read()
        
        message = html_template.format(username=db_user.username, otp_code=otp_code)
        
        await email.send_mail(subject, recipient, message)
        await logger.info("OTP sent successfully", {"username": db_user.username})
        
        return {"message": "OTP sent successfully"}
    except Exception as e:
        await logger.error("Error during login process", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending OTP: {str(e)}"
        )

async def verify_otp(request: schemas.VerifyOTP = Query(...), db: AsyncSession = Depends(get_db)):
    try:
        # Check if input is email or username
        is_email = '@' in request.username

        if is_email:
            # Query user by email
            stmt = (
                select(models_user.Users)
                .join(
                    models_user_info.UserPersonalInfo,
                    models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id
                )
                .where(models_user_info.UserPersonalInfo.email == request.username)
            )
        else:
            # Query user by username
            stmt = (
                select(models_user.Users)
                .where(models_user.Users.username == request.username)
            )

        result = await db.execute(stmt)
        user_info = result.scalars().first()

        if not user_info:
            await logger.warning("OTP verification failed: User not found", {"username": request.username})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Username or Email"
            )
        
        # Use user_id as the key for Redis to unify username/email
        redis_otp = await redis_client.get(user_info.user_id)
        
        if redis_otp is None:
            await logger.warning("OTP verification failed: OTP not found", {"username": request.username})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve OTP from Redis"
            )
        if redis_otp != request.otp_code:
            await logger.warning("OTP verification failed: Invalid OTP", {"username": request.username})
            raise HTTPException(
                status_code=400, detail="Invalid OTP"
            )

        await redis_client.delete(user_info.user_id)

        access_token_expires = jwt.timedelta(minutes=jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = jwt.timedelta(days=jwt.REFRESH_TOKEN_EXPIRE_DAYS)
        
        # Create access and refresh tokens
        access_token = await jwt.create_access_token(
            data={"sub": user_info.user_id},
            expires_delta=access_token_expires
        )
        refresh_token = await jwt.create_refresh_token(
            data={"sub": user_info.user_id}
        )

        # Store tokens in Redis
        await redis_client.setex(
            user_info.user_id, 
            int(access_token_expires.total_seconds()), 
            access_token
        )
        await redis_client.setex(
            f"refresh_token:{user_info.user_id}",
            int(refresh_token_expires.total_seconds()),
            refresh_token
        )

        await logger.info("User logged in successfully", {"username": user_info.username})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        await logger.error("Error during OTP verification", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying OTP: {str(e)}"
        )

async def logout_admin(current_user: models_user.Users, db: AsyncSession):
    try:
        # Extract user_id from the User object
        user_id = str(current_user.user_id)
        # Remove access token from Redis using user_id as key
        deleted = await redis_client.delete(user_id)
        if deleted == 0:
            await logger.warning("Logout failed: Token not found", {"user_id": user_id})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not logged in or token already expired"
            )
        await logger.info("User logged out successfully", {"user_id": user_id})
        return {"detail": "Logged out successfully"}
    except Exception as e:
        await logger.error("Error during logout", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during logout: {str(e)}"
        )

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
    
# async def logout(request: str, db: AsyncSession):
#     try:
#         # Get user_id from username
#         is_email = '@' in request

#         if is_email:
#             # Query user by email
#             stmt = (
#                 select(models_user.Users)
#                 .join(
#                     models_user_info.UserPersonalInfo,
#                     models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id
#                 )
#                 .where(models_user_info.UserPersonalInfo.email == request)
#             )
#         else:
#             # Query user by username
#             stmt = (
#                 select(models_user.Users)
#                 .where(models_user.Users.username == request)
#             )

#         result = await db.execute(stmt)
#         user_info = result.scalars().first()

#         if not user_info:
#             await logger.warning("OTP verification failed: User not found")
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Invalid Username or Email"
#             )
        
#         # Remove access token from Redis using user_id as key
#         deleted = await redis_client.delete(user_info.user_id)
#         if deleted == 0:
#             await logger.warning("Logout failed: Token not found", {"user_id": user_info.user_id})
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="User is not logged in or token already expired"
#             )
#         await logger.info("User logged out successfully", {"user_id": user_info.user_id})
#         return {"detail": "Logged out successfully"}
#     except Exception as e:
#         await logger.error("Error during logout", {"error": str(e)})
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error during logout: {str(e)}"
#         )

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

async def reset_passwords(
    request: schemas.ResetPassword = Query(...), db: AsyncSession = Depends(get_db)
):
    async with DistributedLock(f"reset_password:{request.email}"):
        try:
            # Check if email exists in database
            stmt = (
                select(models_user_info.UserPersonalInfo)
                .where(models_user_info.UserPersonalInfo.email == request.email)
            )
            result = await db.execute(stmt)
            user_info = result.scalars().first()
            
            if not user_info:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Email not found in system"
                )

            # Verify if email matches OTP request
            redis_otp = await redis_client.get(request.email)
            if redis_otp is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No password reset was requested for this email"
                )

            if redis_otp != request.otp_code:
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid OTP code"
                )

            await redis_client.delete(request.email)

            if request.new_password != request.confirm_password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="New password and confirm password do not match"
                )

            await reset_password(db, request.new_password, request.email)
            await logger.info("Password reset successful", {"email": request.email})
            return {"message": "Password reset successfully"}
        except Exception as e:
            await logger.error("Password reset failed", error=e)
            raise