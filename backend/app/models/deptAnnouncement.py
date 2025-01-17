from sqlalchemy import Column, String, DateTime, ForeignKey, Sequence
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..configs.database import Base
from datetime import datetime

class DeptAnnouncement(Base):
    __tablename__ = "dept_announcement"

    announcement_id = Column(String, Sequence("deptannou_id_seq"),primary_key=True, index=True, nullable=False)
    department_id = Column(String, ForeignKey("department.department_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, index=True) #phải tồn tại department_id
    announcement_title = Column(String, nullable=True)
    announcement_description = Column(String, nullable=True)
    create_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    department = relationship("Department", back_populates="announcements")