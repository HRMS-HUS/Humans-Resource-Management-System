from pydantic import BaseModel
from typing import Optional
from ..models import users

class User(BaseModel):
    user_id: str
    username: str
    role: users.RoleEnum
    status: users.StatusEnum

class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(UserCreate):
    role: Optional[users.RoleEnum] = None
    status: Optional[users.StatusEnum] = None

class ChangePassword(BaseModel):
    current_password: str
    new_password: str

class AdminChangePassword(BaseModel):
    new_password: str