from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from enum import Enum

class StatusEnum(str, Enum):
    Active = "Active"
    Inactive = "Inactive"

class DepartmentBase(BaseModel):
    department_name: str
    manager_id: str
    location: Optional[str] = None
    contact_email: EmailStr
    start_date: Optional[date] = None
    status: StatusEnum = StatusEnum.Active

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None
    manager_id: Optional[str] = None
    location: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    start_date: Optional[date] = None
    status: Optional[StatusEnum] = None

class DepartmentResponse(DepartmentBase):
    department_id: str

    class Config:
        orm_mode = True
