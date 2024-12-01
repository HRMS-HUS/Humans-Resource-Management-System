from sqlalchemy.ext.asyncio import AsyncSession
from ..models import userPersonalInfo as models_user_info
from ..models import users as models_user
from ..schemas import users as schemas_user
from ..models import auth as models
from ..schemas import auth as schemas
from ..controllers import users, auth
from fastapi import HTTPException,status, Depends, APIRouter, Query
from sqlalchemy import select, and_, func, text, delete
from ..utils import crypto, jwt, email, otp
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import os
from pathlib import Path


router = APIRouter()

@router.post("/auth/register", response_model = schemas_user.UserCreate)
async def register(user: schemas_user.UserCreate = Query(...) ,db: AsyncSession = Depends(get_db)):
    stmt = (
        select(
            models_user.Users

        )
        .where(models_user.Users.username == user.username)
    )
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    

    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already register")
    
    user.password = crypto.hash_password(user.password)
    return await users.create_user(db, user)

@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    stmt = (
        select(
            models_user.Users,
            models_user_info.UserPersonalInfo.email
        )
        .join(models_user_info.UserPersonalInfo, models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id)
        .where(
            models_user.Users.username == form_data.username
        )
    )
    result = await db.execute(stmt)
    user_info = result.first()
    
    if user_info:
        db_user, email_user = user_info
        verify_password = crypto.verify_password(form_data.password, db_user.password)
        if not verify_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Username or Password")
        
        otp_code = otp.create_otp()
        await auth.create_otp_code(db, db_user.username, otp_code)
        
        subject = "OTP"
        recipient = [email_user]
        
        # Read and format the HTML template
        template_path = Path(__file__).parent.parent / 'templates' / 'otp_email_login.html'
        with open(template_path, 'r') as file:
            html_template = file.read()
        
        message = html_template.format(username=db_user.username, otp_code=otp_code)
        
        await email.send_mail(subject, recipient, message)
        
        return {"message": "OTP sent"}

@router.post("/auth/verify-otp")
async def verify_otp(request: schemas.VerifyOTPRequest = Query(...), db: AsyncSession = Depends(get_db)):
    db_code = await auth.check_otp_code(db, request.otp_code)

    if not db_code:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    

    access_token_expires = jwt.timedelta(minutes=jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await jwt.create_access_token(
        data={"sub": db_code.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/forgot_password")
async def forgot_password(request: schemas.ForgotPassword = Query(...), db: AsyncSession = Depends(get_db)):
    stmt = (
        select(models_user.Users, models_user_info.UserPersonalInfo.email)
        .join(models_user_info.UserPersonalInfo, models_user.Users.user_id == models_user_info.UserPersonalInfo.user_id)
        .where(models_user.Users.username == request.username)
    )
    result = await db.execute(stmt)
    user_info = result.first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Not Found")
    email_user = user_info[1]
    reset_code = otp.create_otp()
    await auth.create_otp_code(db, request.username, reset_code)
    subject = "Reset code"
    recipient = [email_user]
    
    # Read and format the HTML template
    template_path = Path(__file__).parent.parent / 'templates' / 'otp_email_forgot_password.html'
    with open(template_path, 'r') as file:
        html_template = file.read()
    
    message = html_template.format(username=request.username, reset_code=reset_code)
    
    await email.send_mail(subject, recipient, message)
    
    return {"message": "Password reset email sent"}


@router.post("/auth/reset_password")
async def reset_passwords(request: schemas.ResetPassword = Query(...), db: AsyncSession = Depends(get_db)):
    otp_code = await auth.check_otp_code(db, request.otp_code)
    
    if not otp_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Reset Code Not Found")
    
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="new same confirm")
    
    await auth.reset_password(db, request.new_password, request.username)
    return {"message": "Password reset successful"}