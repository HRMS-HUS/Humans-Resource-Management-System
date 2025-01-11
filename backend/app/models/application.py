from sqlalchemy import Column, ForeignKey, String, Date, Boolean, Enum, Sequence
from ..configs.database import Base
import enum

class LeaveTypeEnum(enum.Enum):
    Normal = "Normal"
    Student = "Student"
    Illness = "Illness"
    Marriage = "Marriage"
class StatusEnumApplication(enum.Enum):
    Approved = "Approved"
    Rejected = "Rejected"
    Pending = "Pending"

class Application(Base):
    __tablename__ = "application"

    application_id = Column(String, Sequence("application_id_seq"),primary_key=True, index=True,nullable=False)
    user_id = Column(String, nullable=False)
    leave_type = Column(Enum(LeaveTypeEnum), nullable=True)
    reason = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date,nullable=True)
    status = Column(Enum(StatusEnumApplication), nullable=False, default=StatusEnumApplication.Pending)