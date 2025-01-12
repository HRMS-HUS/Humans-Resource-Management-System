from sqlalchemy import Column, String, Integer, Boolean, DateTime, Sequence, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..configs.database import Base
from datetime import datetime, timedelta
import enum

class RoleEnum(enum.Enum):
    Admin = "Admin"
    Manager = "Manager"
    User = "User"

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
    
    # Relationships
    personal_info = relationship("UserPersonalInfo", back_populates="user", uselist=False)
    financial_info = relationship("UserFinancialInfo", back_populates="user", uselist=False)
    events = relationship("UserPersonalEvent", back_populates="user")
    messages_sent = relationship("UserMessage", foreign_keys="[UserMessage.sender_id]", back_populates="sender")
    messages_received = relationship("UserMessage", foreign_keys="[UserMessage.receiver_id]", back_populates="receiver")
    payments = relationship("Payment", back_populates="user")
    jobs = relationship("Job", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    managed_departments = relationship("Department", back_populates="manager")
    applications = relationship("Application", back_populates="user")
    attendance_records = relationship("DaysWorking", back_populates="user", cascade="all, delete")