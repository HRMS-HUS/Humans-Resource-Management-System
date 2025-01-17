from sqlalchemy import Column, ForeignKey, String, Float, Integer, Enum, Sequence
from sqlalchemy.orm import relationship
from ..configs.database import Base
import enum

class PaymentEnum(enum.Enum):
    Check = "Check"
    Bank_Transfer = "Bank Transfer"
    Cash = "Cash"
class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(String, Sequence("payment_id_seq"), primary_key=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    payment_method = Column(Enum(PaymentEnum), nullable=True, default=PaymentEnum.Check)
    payment_month = Column(Integer, nullable=True)
    payment_date = Column(Integer, nullable=True)
    payment_fine = Column(Float, nullable=True)
    payment_amount = Column(Float, nullable=True)
    comments = Column(String, nullable=True)
    
    # Relationships
    user = relationship("Users", back_populates="payments")