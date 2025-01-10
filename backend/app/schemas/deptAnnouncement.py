from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeptAnnouncementBase(BaseModel):
    department_id: str
    announcement_title: str
    announcement_description: str

class DeptAnnouncementCreate(DeptAnnouncementBase):
    pass

class DeptAnnouncementUpdate(BaseModel):
    department_id: Optional[str] = None
    announcement_title: Optional[str] = None
    announcement_description: Optional[str] = None

class DeptAnnouncementResponse(DeptAnnouncementBase):
    announcement_id: str

    class Config:
        orm_mode = True
