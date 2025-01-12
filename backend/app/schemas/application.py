from pydantic import BaseModel, validator
from datetime import date
from typing import Optional
from enum import Enum

class LeaveTypeEnum(str, Enum):
    Normal = "Normal"
    Student = "Student"
    Illness = "Illness"
    Marriage = "Marriage"

class StatusEnum(str, Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"

class ApplicationBase(BaseModel):
    user_id: Optional[str] = None
    leave_type: Optional[LeaveTypeEnum] = None
    reason: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[StatusEnum] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    leave_type: Optional[LeaveTypeEnum] = None
    reason: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[StatusEnum] = None

class ApplicationResponse(ApplicationBase):
    application_id: str
    
    class Config:
        orm_mode = True
