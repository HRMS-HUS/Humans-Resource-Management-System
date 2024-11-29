from pydantic import BaseModel
from typing import Optional
from ..models import users

class ForgotPassword(BaseModel):
    username: str

class ResetPassword(BaseModel):
    username: str
    otp_code: str
    new_password: str
    confirm_password: str

class VerifyOTPRequest(BaseModel):
    username: str
    otp_code: str