from sqlalchemy import Column, String, DateTime, ForeignKey, Sequence
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..configs.database import Base
from datetime import datetime, timezone, timedelta
def utc_plus_7():
    return datetime.utcnow() + timedelta(hours=7)

class DeptAnnouncement(Base):
    __tablename__ = "dept_announcement"

    announcement_id = Column(String, Sequence("deptAnnou_id_seq"),primary_key=True, index=True, nullable=False)
    department_id = Column(String, ForeignKey("department.department_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    announcement_title = Column(String, nullable=False)
    announcement_description = Column(String, nullable=False)
    create_at = Column(DateTime(timezone=True), default=utc_plus_7)
    
    # Relationships
    department = relationship("Department", back_populates="announcements")