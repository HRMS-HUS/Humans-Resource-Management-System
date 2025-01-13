from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, time
from zoneinfo import ZoneInfo

class DaysWorkingBase(BaseModel):
    user_id: str
    day: Optional[date] = None
    login_time: Optional[time] = None
    logout_time: Optional[time] = None
    total_hours: Optional[float] = None

    @validator('login_time', 'logout_time', pre=True)
    def ensure_timezone(cls, v):
        if v and not getattr(v, 'tzinfo', None):
            # Add UTC timezone if not present
            return v.replace(tzinfo=ZoneInfo('UTC'))
        return v

class DaysWorkingCreate(DaysWorkingBase):
    pass

class DaysWorkingUpdate(BaseModel):
    logout_time: time
    total_hours: float

    @validator('logout_time', pre=True)
    def ensure_timezone(cls, v):
        if v and not getattr(v, 'tzinfo', None):
            return v.replace(tzinfo=ZoneInfo('UTC'))
        return v

class DaysWorkingResponse(DaysWorkingBase):
    working_id: str

    class Config:
        orm_mode = True
        json_encoders = {
            time: lambda t: t.isoformat()
        }
