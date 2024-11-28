from sqlalchemy.ext.asyncio import AsyncSession
from ..models import userPersonalInfo as models_user_info
from ..models import users as models
from ..schemas import users as schemas
from ..controllers import users
from fastapi import HTTPException,status, Depends, APIRouter, Query
from sqlalchemy import select, and_, func, text, delete
from ..utils import crypto, jwt, email, otp
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


router = APIRouter()


@router.get("/auth/me", response_model=schemas.UserCreate)
async def read_users_me(token: str = Query(...), db: AsyncSession = Depends(get_db), current: models.Users = Depends(jwt.get_current_admin)):
    user = await jwt.get_current_user(token, db)
    return user

@router.post("/auth/register", response_model = schemas.UserCreate)
async def register(user: schemas.UserCreate = Query(...) ,db: AsyncSession = Depends(get_db)):
    stmt = (
        select(
            models.Users

        )
        .where(models.Users.username == user.username)
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
            models.Users,
            models_user_info.UserPersonalInfo.email
        )
        .join(models_user_info.UserPersonalInfo, models.Users.user_id == models_user_info.UserPersonalInfo.user_id)
        .where(
            models.Users.username == form_data.username
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
        await users.create_otp_code(db, db_user.username, otp_code)
        subject = "OTP"
        recipient = [email_user]
        message = f"""<!DOCTYPE html>
<html>
<head>
    <title>Password Reset</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 16px;
            line-height: 1.5;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f9;
        }}
        h1 {{
            font-size: 24px;
            margin-bottom: 20px;
            color: #333;
        }}
        p {{
            margin-bottom: 15px;
            color: #555;
        }}
        a {{
            color: #007bff;
            text-decoration: none;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        .otp {{
            display: inline-block;
            padding: 10px 20px;
            margin: 20px 0;
            background-color: #007bff;
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            border-radius: 5px;
            letter-spacing: 2px;
        }}
        .footer {{
            margin-top: 30px;
            font-size: 14px;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello, {db_user.username}</h1>
        <p>To log in, please use the following one-time password (OTP):</p>
        <p class="otp">{otp_code}</p>
        <p>If you didn't request this, you can ignore this email.</p>
        <p>Your password won't change until you use the token to create a new one.</p>
        <div class="footer">
            <p>Thank you,<br>T1 VÔ ĐỊCH</p>
        </div>
    </div>
</body>
</html>
"""
    await email.send_mail(subject, recipient, message)
    return {"message:" "OTP sent"}

@router.post("/auth/verify-otp")
async def verify_otp(request: schemas.VerifyOTPRequest = Query(...), db: AsyncSession = Depends(get_db)):
    db_code = await users.check_otp_code(db, request.otp_code)

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
        select(models.Users, models_user_info.UserPersonalInfo.email)
        .join(models_user_info.UserPersonalInfo, models.Users.user_id == models_user_info.UserPersonalInfo.user_id)
        .where(models.Users.username == request.username)
    )
    result = await db.execute(stmt)
    user_info = result.first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Not Found")
    email_user = user_info[1]
    reset_code = otp.create_otp()
    await users.create_otp_code(db, request.username, reset_code)
    subject = "Reset code"
    recipient = [email_user]
    message = f"""<!DOCTYPE html>
<html>
<head>
    <title>Password Reset</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 16px;
            line-height: 1.5;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f9;
        }}
        h1 {{
            font-size: 24px;
            margin-bottom: 20px;
            color: #333;
        }}
        p {{
            margin-bottom: 15px;
            color: #555;
        }}
        a {{
            color: #007bff;
            text-decoration: none;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        .otp {{
            display: inline-block;
            padding: 10px 20px;
            margin: 20px 0;
            background-color: #007bff;
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            border-radius: 5px;
            letter-spacing: 2px;
        }}
        .footer {{
            margin-top: 30px;
            font-size: 14px;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello, {request.username}</h1>
        <p>Someone has requested a password reset. If you requested this, you can use the following token to reset your password:</p>
        <p class="otp">{reset_code}</p>
        <p>If you didn't request this, you can ignore this email.</p>
        <p>Your password won't change until you use the token to create a new one.</p>
        <div class="footer">
            <p>Thank you,<br>T1 VÔ ĐỊCH</p>
        </div>
    </div>
</body>
</html>
"""
    await email.send_mail(subject, recipient, message)
    return {"message": "Password reset email sent"}


@router.post("/auth/reset_password")
async def reset_passwords(request: schemas.ResetPassword = Query(...), db: AsyncSession = Depends(get_db)):
    otp_code = await users.check_otp_code(db, request.otp_code)
    
    if not otp_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Reset Code Not Found")
    
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="new same confirm")
    
    await users.reset_password(db, request.new_password, request.username)
    return {"message": "Password reset successful"}