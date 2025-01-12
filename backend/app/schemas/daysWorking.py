from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class DaysWorkingBase(BaseModel):
    user_id: str
    day: Optional[date] = None
    login_time: Optional[datetime] = None
    logout_time: Optional[datetime] = None
    total_hours: Optional[float] = None

class DaysWorkingCreate(DaysWorkingBase):
    pass

class DaysWorkingUpdate(BaseModel):
    logout_time: datetime
    total_hours: float

class DaysWorkingResponse(DaysWorkingBase):
    working_id: str

    class Config:
        orm_mode = True
