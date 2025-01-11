from sqlalchemy import Column, String, ForeignKey, Sequence
from ..configs.database import Base

class UserMessage(Base):
    __tablename__ = "user_message"
    message_id = Column(String, Sequence("message_id_seq"), primary_key=True, index = True, nullable=False)
    sender_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    text = Column(String, nullable=False)