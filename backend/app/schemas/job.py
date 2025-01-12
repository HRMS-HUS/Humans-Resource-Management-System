from pydantic import BaseModel
from typing import Optional
from datetime import date

class JobBase(BaseModel):
    user_id: Optional[str] = None
    job_tittle: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    job_tittle: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
class Job(JobBase):
    job_id: str

    class Config:
        orm_mode = True
