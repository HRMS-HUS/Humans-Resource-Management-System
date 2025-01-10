from pydantic import BaseModel, EmailStr, validator
from datetime import date
from ..models import userPersonalInfo as user_info
from ..validations.user_info_validator import (
    validate_phone, validate_citizen_card, validate_birth_date,
    validate_sex, validate_name, validate_address, validate_location
)
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
    department_id: Optional[str] = None
    photo_url: Optional[str] = None

    @validator('phone')
    def check_phone(cls, v):
        validate_phone(v)
        return v

    @validator('citizen_card')
    def check_citizen_card(cls, v):
        validate_citizen_card(v)
        return v

    @validator('date_of_birth')
    def check_birth_date(cls, v):
        validate_birth_date(v)
        return v

    @validator('sex')
    def check_sex(cls, v):
        validate_sex(v)
        return v

    @validator('fullname')
    def check_name(cls, v):
        validate_name(v)
        return v

    @validator('address')
    def check_address(cls, v):
        validate_address(v)
        return v

    @validator('city', 'country')
    def check_location(cls, v):
        validate_location(v)
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
    photo_url: Optional[str] = None

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
    photo_url: Optional[str] = None

class UserInfoResponse(UserInfoBase):
    personal_info_id: str

    class Config:
        orm_mode = True