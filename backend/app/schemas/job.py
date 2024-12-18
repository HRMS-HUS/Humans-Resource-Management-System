from pydantic import BaseModel
from typing import Optional
from datetime import date

class JobBase(BaseModel):
    user_id: str
    job_tittle: str
    start_date: date
    end_date: date

class JobCreate(JobBase):
    job_id: str

class Job(JobBase):
    job_id: str

    class Config:
        orm_mode = True
