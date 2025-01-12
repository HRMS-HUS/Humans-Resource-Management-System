from sqlalchemy import Column, String, DateTime, Date, Sequence, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..configs.database import Base

class DaysWorking(Base):
    __tablename__ = "days_working"

    working_id = Column(String, Sequence("working_id_seq"), primary_key=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    day = Column(Date, nullable=False, index=True)
    login_time = Column(DateTime(timezone=True), nullable=True)
    logout_time = Column(DateTime(timezone=True), nullable=True)
    total_hours = Column(Float, nullable=True)

    # Relationships
    user = relationship("Users", back_populates="attendance_records")