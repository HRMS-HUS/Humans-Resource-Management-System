from sqlalchemy import Column, ForeignKey, String, Date, Sequence
from sqlalchemy.orm import relationship
from ..configs.database import Base

class UserPersonalEvent(Base):
    __tablename__ = "user_personal_event"

    event_id = Column(String, Sequence("event_id_seq"),  primary_key=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False, index=True)
    event_title = Column(String, nullable=True)
    event_description = Column(String, nullable=True)
    event_start_date = Column(Date, nullable=True)
    event_end_date = Column(Date, nullable=True)
    
    # Relationships
    user = relationship("Users", back_populates="events")