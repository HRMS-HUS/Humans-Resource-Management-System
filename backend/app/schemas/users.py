from pydantic import BaseModel, validator
from typing import Optional
from ..models import users
from ..validations.user_validator import validate_password, validate_username

class User(BaseModel):
    user_id: str
    username: Optional[str] = None
    role: Optional[users.RoleEnum] = None
    status: Optional[users.StatusEnum] = None

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[users.RoleEnum] = None

    @validator('password')
    def validate_password(cls, v):
        validate_password(v)
        return v

    @validator('username')
    def validate_username(cls, v):
        validate_username(v)
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[users.RoleEnum] = None
    status: Optional[users.StatusEnum] = None

class ChangePassword(BaseModel):
    current_password: str
    new_password: str

    @validator('new_password')
    def validate_new_password(cls, v):
        validate_password(v)
        return v

class AdminChangePassword(BaseModel):
    new_password: str

    @validator('new_password')
    def validate_new_password(cls, v):
        validate_password(v)
        return v