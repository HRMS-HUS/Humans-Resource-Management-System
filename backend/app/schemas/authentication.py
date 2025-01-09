from pydantic import BaseModel, EmailStr
from typing import Optional
from ..models import users

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    email: EmailStr
    otp_code: str
    new_password: str
    confirm_password: str

class VerifyOTP(BaseModel):
    username: str
    otp_code: str