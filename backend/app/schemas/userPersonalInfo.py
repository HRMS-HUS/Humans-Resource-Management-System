from pydantic import BaseModel, EmailStr
from datetime import date
from ..models import userPersonalInfo as user_info

from typing import Optional

class UserInfoCreate(BaseModel):
    fullname: str
    citizen_card: str
    date_of_birth: date
    sex: str
    phone: str
    email: EmailStr
    marital_status:  user_info.MaritalStatusEnum
    address: str
    city: str
    country: str