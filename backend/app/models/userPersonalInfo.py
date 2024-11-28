from sqlalchemy import Column, ForeignKey, String, Date, Enum
from ..database import Base
import enum

class MaritalStatusEnum(enum.Enum):
        Married = "Married"
        Single = "Single"
        Widowed = "Widowed"

class UserPersonalInfo(Base):
    __tablename__ = "users_personal_info"

    personal_info_id = Column(String, primary_key=True, index=True, nullable=False) 
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), index=True, nullable= False)
    fullname = Column(String, nullable= False)
    citizen_card = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    sex = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    marital_status = Column(Enum(MaritalStatusEnum),nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    