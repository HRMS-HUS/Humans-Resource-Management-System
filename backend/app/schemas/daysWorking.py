from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class DaysWorkingBase(BaseModel):
    day: Optional[date] = None
    starting_hours: Optional[datetime] = None
    ending_hours: Optional[datetime] = None

class DaysWorkingCreate(DaysWorkingBase):
    pass

class DaysWorkingUpdate(BaseModel):
    day: Optional[date] = None
    starting_hours: Optional[datetime] = None
    ending_hours: Optional[datetime] = None

class DaysWorkingResponse(DaysWorkingBase):
    working_id: str

    class Config:
        orm_mode = True
