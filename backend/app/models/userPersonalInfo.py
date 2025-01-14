from sqlalchemy import Column, ForeignKey, String, Date, Enum, Sequence
from sqlalchemy.orm import relationship
from ..configs.database import Base
import enum

class MaritalStatusEnum(enum.Enum):
        Married = "Married"
        Single = "Single"
        Widowed = "Widowed"

class UserPersonalInfo(Base):
    __tablename__ = "users_personal_info"

    personal_info_id = Column(String, Sequence("personal_id_seq"), primary_key=True, index=True, nullable=False) 
    user_id = Column(String, ForeignKey("users.user_id",onupdate="CASCADE", ondelete="CASCADE"), index=True, nullable= False)
    fullname = Column(String, nullable= True)
    citizen_card = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    sex = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True, index=True)
    marital_status = Column(Enum(MaritalStatusEnum),nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    department_id = Column(String, ForeignKey("department.department_id", ondelete="CASCADE"), nullable=True, index=True)
    photo_url = Column(String, nullable=True)
    
    # Relationships
    user = relationship("Users", back_populates="personal_info")
    department = relationship("Department", back_populates="employees")