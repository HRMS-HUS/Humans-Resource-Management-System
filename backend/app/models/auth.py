from sqlalchemy import Column, String, Integer, Boolean, DateTime, Sequence, Enum
from ..database import Base
from datetime import datetime, timedelta
import enum

def utc_plus_7():
    return datetime.utcnow() + timedelta(hours=7)
class StatusEnum(enum.Enum):
    Active = "A"
    Inactive = "I"

class PasswordResetCode(Base):
    __tablename__ = 'password_reset_codes'
    
    reset_id = Column(String, Sequence("code_id_seq"), primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    reset_code = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.Active)
    expired_in = Column(DateTime, default=utc_plus_7)