from sqlalchemy import Column, String, DateTime, Date
from ..database import Base

class DaysWorking(Base):
    __tablename__ = "days_working"

    working_id = Column(String, primary_key=True, index=True, nullable=False)
    day = Column(Date, nullable=False)
    starting_hours = Column(DateTime, nullable=False)
    ending_hours = Column(DateTime, nullable=False)