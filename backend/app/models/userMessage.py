from sqlalchemy import Column, String, ForeignKey, Sequence, DateTime, Boolean
from sqlalchemy.orm import relationship
from ..configs.database import Base
from datetime import datetime

class UserMessage(Base):
    __tablename__ = "user_message"
    message_id = Column(String, Sequence("message_id_seq"), primary_key=True, index = True, nullable=False)
    sender_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    text = Column(String, nullable=False)
    # created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # is_read = Column(Boolean, default=False, nullable=False)
    # status = Column(String, default="sent", nullable=False)  # sent, delivered, read
    
    # Relationships
    sender = relationship("Users", foreign_keys=[sender_id], back_populates="messages_sent")
    receiver = relationship("Users", foreign_keys=[receiver_id], back_populates="messages_received")