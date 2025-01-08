from pydantic import BaseModel, EmailStr
from datetime import date
from ..models import userPersonalInfo as user_info

from typing import Optional

class UserInfoBase(BaseModel):
    user_id: str
    fullname: str
    citizen_card: str
    date_of_birth: date
    sex: str
    phone: str
    email: EmailStr
    marital_status: user_info.MaritalStatusEnum
    address: str
    city: str
    country: str

class UserInfoCreate(UserInfoBase):
    pass

class UserInfoUpdate(BaseModel):
    fullname: Optional[str] = None
    citizen_card: Optional[str] = None
    date_of_birth: Optional[date] = None
    sex: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    marital_status: Optional[user_info.MaritalStatusEnum] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class UserInfoResponse(UserInfoBase):
    personal_info_id: str

    class Config:
        orm_mode = True