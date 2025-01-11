from pydantic import BaseModel, validator
from datetime import date
from typing import Optional
from ..validations.event_validator import (
    validate_event_dates
)

class UserPersonalEventBase(BaseModel):
    user_id: str
    event_title: Optional[str] = None
    event_description: Optional[str] = None
    event_start_date: Optional[date] = None
    event_end_date: Optional[date] = None

    @validator('event_end_date')
    def check_dates(cls, v, values):
        if 'event_start_date' in values:
            validate_event_dates(values['event_start_date'], v)
        return v

class UserPersonalEventCreate(UserPersonalEventBase):
    pass

class UserPersonalEventUpdate(BaseModel):
    event_title: Optional[str] = None
    event_description: Optional[str] = None
    event_start_date: Optional[date] = None
    event_end_date: Optional[date] = None

    @validator('event_end_date')
    def check_dates(cls, v, values):
        if 'event_start_date' in values:
            validate_event_dates(values['event_start_date'], v)
        return v

class UserPersonalEventResponse(UserPersonalEventBase):
    event_id: str

    class Config:
        orm_mode = True