from sqlalchemy import Column, String, DateTime, Date, Sequence, Float, ForeignKey, Time
from sqlalchemy.orm import relationship
from ..configs.database import Base
from sqlalchemy.types import TypeDecorator, Time
import datetime

class TimezoneAwareTime(TypeDecorator):
    impl = Time
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None and value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value

    def process_result_value(self, value, dialect):
        if value is not None and value.tzinfo is None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value

class DaysWorking(Base):
    __tablename__ = "days_working"

    working_id = Column(String, Sequence("working_id_seq"), primary_key=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    day = Column(Date, nullable=False, index=True)
    login_time = Column(TimezoneAwareTime(timezone=True), nullable=True)
    logout_time = Column(TimezoneAwareTime(timezone=True), nullable=True)
    total_hours = Column(Float, nullable=True)

    # Relationships
    user = relationship("Users", back_populates="attendance_records")