from pydantic import BaseModel
from typing import Optional
from datetime import date

class DaysHolidayBase(BaseModel):
    holiday_name: str
    holiday_date: date

class DaysHolidayCreate(DaysHolidayBase):
    pass

class DaysHolidayUpdate(BaseModel):
    holiday_name: Optional[str] = None
    holiday_date: Optional[date] = None

class DaysHolidayResponse(DaysHolidayBase):
    holiday_id: str

    class Config:
        orm_mode = True
