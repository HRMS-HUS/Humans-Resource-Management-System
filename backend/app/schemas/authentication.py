from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from ..models import users
from ..validations.user_validator import validate_password

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    email: EmailStr
    otp_code: str
    new_password: str
    confirm_password: str

    @validator('new_password')
    def validate_new_password(cls, v):
        validate_password(v)
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v

class VerifyOTP(BaseModel):
    username: str
    otp_code: str