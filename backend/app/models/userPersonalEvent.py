from sqlalchemy import Column, ForeignKey, String, Date
from ..database import Base

class UserPersonalEvent(Base):
    __tablename__ = "user_personal_event"

    event_id = Column(String, primary_key=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    event_title = Column(String, nullable=False)
    event_description = Column(String, nullable=False)
    event_start_date = Column(Date, nullable=False)
    event_end_date = Column(Date, nullable=False)