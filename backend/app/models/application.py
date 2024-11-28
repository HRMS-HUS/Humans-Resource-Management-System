from sqlalchemy import Column, ForeignKey, String, Date, Boolean, Enum
from ..database import Base
import enum

class LeaveTypeEnum(enum.Enum):
    Normal = "Normal"
    Student = "Student"
    Illness = "Illness"
    Marriage = "Marriage"
class StatusEnum(enum.Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"

class Application(Base):
    __tablename__ = "application"

    application_id = Column(String, primary_key=True, index=True,nullable=False)
    user_id = Column(String, nullable=False)
    leave_type = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date,nullable=False)
    status = Column(String, nullable=False, default="Pending")