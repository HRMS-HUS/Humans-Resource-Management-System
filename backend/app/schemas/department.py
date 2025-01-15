from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from enum import Enum
from ..models import department

class DepartmentBase(BaseModel):
    department_name: Optional[str] = None
    manager_id: Optional[str] = None
    location: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    start_date: Optional[date] = None
    status: Optional[department.StatusEnum] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None
    manager_id: Optional[str] = None
    location: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    start_date: Optional[date] = None
    status: Optional[department.StatusEnum] = None

class DepartmentResponse(DepartmentBase):
    department_id: str

    class Config:
        orm_mode = True

class DepartmentManagerInfo(BaseModel):
    user_id: str
    fullname: Optional[str]
    
class DepartmentResponseWithManager(BaseModel):
    department_id: str
    name: str
    description: Optional[str] = None
    manager_id: str
    manager: Optional[DepartmentManagerInfo] = None

    class Config:
        orm_mode = True
