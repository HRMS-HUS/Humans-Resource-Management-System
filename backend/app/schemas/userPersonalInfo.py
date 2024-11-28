from pydantic import BaseModel, EmailStr

from typing import Optional

class UserInfoCreate(BaseModel):
    fullname: str
    email: EmailStr