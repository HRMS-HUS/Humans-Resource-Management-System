from sqlalchemy import Column, String, DateTime, ForeignKey
from ..database import Base

class DeptAnnouncement(Base):
    __tablename__ = "dept_announcement"

    announcement_id = Column(String, primary_key=True, index=True, nullable=False)
    department_id = Column(String, ForeignKey("department.department_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    announcement_title = Column(String, nullable=False)
    announcement_description = Column(String, nullable=False)
    create_at = Column(DateTime, nullable=False)