from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserPersonalEventBase(BaseModel):
    user_id: str
    event_title: str
    event_description: str
    event_start_date: date
    event_end_date: date
    

class UserPersonalEventCreate(UserPersonalEventBase):
    pass

class UserPersonalEventUpdate(BaseModel):
    event_title: Optional[str] = None
    event_description: Optional[str] = None
    event_start_date: Optional[date] = None
    event_end_date: Optional[date] = None

class UserPersonalEventResponse(UserPersonalEventBase):
    event_id: str

    class Config:
        orm_mode = True