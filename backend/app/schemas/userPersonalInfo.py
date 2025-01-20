from pydantic import BaseModel, EmailStr, validator
from datetime import date
from ..models import userPersonalInfo as user_info
from ..validations.user_info_validator import (
    validate_phone, validate_citizen_card
)
from typing import Optional

class UserInfoBase(BaseModel):
    user_id: Optional[str] = None
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
    department_id: Optional[str] = None
    photo_url: Optional[str] = None

    @validator('phone')
    def check_phone(cls, v):
        if v is not None:  # Only validate if value is provided
            validate_phone(v)
        return v

    @validator('citizen_card')
    def check_citizen_card(cls, v):
        if v is not None:  # Only validate if value is provided
            validate_citizen_card(v)
        return v

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
    department_id: Optional[str] = None

    @validator('phone')
    def check_phone(cls, v):
        if v is not None:  # Only validate if value is provided
            validate_phone(v)
        return v

    @validator('citizen_card')
    def check_citizen_card(cls, v):
        if v is not None:  # Only validate if value is provided
            validate_citizen_card(v)
        return v

class UserInfoUpdateNoDepartment(BaseModel):
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

    @validator('phone')
    def check_phone(cls, v):
        if v is not None:  # Only validate if value is provided
            validate_phone(v)
        return v

    @validator('citizen_card')
    def check_citizen_card(cls, v):
        if v is not None:  # Only validate if value is provided
            validate_citizen_card(v)
        return v

class UserInfoPhotoUpdate(BaseModel):
    photo_url: Optional[str] = None

class UserInfoResponse(UserInfoBase):
    personal_info_id: str

    class Config:
        orm_mode = True