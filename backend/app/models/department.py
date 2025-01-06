from sqlalchemy import Column, String, ForeignKey, Date, Enum
import enum
from ..database import Base

class StatusEnum(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"

class Department(Base):
    __tablename__ = "department"
    department_id = Column(String, primary_key=True, index=True, nullable=False)
    department_name = Column(String, nullable=True)
    manager_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    location = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.Active, nullable=False)
