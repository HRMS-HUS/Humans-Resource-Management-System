from sqlalchemy import Column, String, Integer, Boolean, DateTime, Sequence, Enum
from ..database import Base
from datetime import datetime, timedelta
import enum

class RoleEnum(enum.Enum):
    Admin = "Admin"
    User = "User"

class StatusEnum(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"

class StatusEnum(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"

class Users(Base):
    __tablename__ = "users"

    user_id = Column(String, Sequence("user_id_seq"), primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.User, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.Active, nullable=False)

def utc_plus_7():
    return datetime.utcnow() + timedelta(hours=7)

class OTPCode(Base):
    __tablename__ = 'otp_code'
    
    otp_id = Column(String, Sequence("code_id_seq"), primary_key=True, index=True)
    username = Column(String, nullable=True, unique=True)
    otp_code = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.Active)
    expired_in = Column(DateTime, default=utc_plus_7)