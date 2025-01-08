from sqlalchemy import Column, String, ForeignKey
from ..configs.database import Base

class UserMessage(Base):
    __tablename__ = "user_message"
    message_id = Column(String, primary_key=True, index = True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    text = Column(String, nullable=False)