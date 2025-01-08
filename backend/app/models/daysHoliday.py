from sqlalchemy import Column, String, Date
from ..configs.database import Base

class DaysHoliday(Base):
    __tablename__ = "days_holiday"

    holiday_id = Column(String, primary_key=True, index=True, nullable=False)
    date = Column(Date, nullable=False)