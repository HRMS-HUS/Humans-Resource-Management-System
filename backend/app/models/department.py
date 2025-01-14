from sqlalchemy import Column, String, ForeignKey, Date, Enum,Sequence
import enum
from ..configs.database import Base
from sqlalchemy.orm import relationship

class StatusEnum(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"

class Department(Base):
    __tablename__ = "department"
    department_id = Column(String, Sequence("department_id_seq"),primary_key=True, index=True, nullable=False)
    department_name = Column(String, nullable=True)
    manager_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    location = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.Active, nullable=False)
    
    # Relationships
    manager = relationship("Users", back_populates="managed_departments")
    employees = relationship("UserPersonalInfo", back_populates="department")
    announcements = relationship("DeptAnnouncement", back_populates="department")
