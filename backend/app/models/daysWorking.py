from sqlalchemy import Column, String, DateTime, Date, Sequence
from ..configs.database import Base

class DaysWorking(Base):
    __tablename__ = "days_working"

    working_id = Column(String, Sequence("working_id_seq"), primary_key=True, index=True, nullable=False)
    day = Column(Date, nullable=True)
    starting_hours = Column(DateTime(timezone=True), nullable=True)
    ending_hours = Column(DateTime(timezone=True), nullable=True)