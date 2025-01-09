from sqlalchemy import Column, String, Date, Sequence
from ..configs.database import Base

class DaysHoliday(Base):
    __tablename__ = "days_holiday"

    holiday_id = Column(String, Sequence("holiday_id_seq"),primary_key=True, index=True, nullable=False)
    holiday_name = Column(String, nullable=True)
    holiday_date = Column(Date, nullable=True)