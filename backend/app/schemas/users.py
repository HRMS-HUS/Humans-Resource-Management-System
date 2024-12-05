from pydantic import BaseModel
from typing import Optional
from ..models import users

class User(BaseModel):
    user_id: str
    role: users.RoleEnum
    status: users.StatusEnum

class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(UserCreate):
    role: Optional[users.RoleEnum] = None
    status: Optional[users.StatusEnum] = None