from sqlalchemy import Column, ForeignKey, String, Float, Integer, Enum
from ..configs.database import Base
import enum

class PaymentEnum(enum.Enum):
    Check = "Check"
    Bank_Transfer = "Bank Transfer"
    Cash = "Cash"
class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(String, primary_key=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    payment_method = Column(String, nullable=False)
    payment_month = Column(Integer, nullable=False)
    payment_date = Column(Integer, nullable=False)
    payment_fine = Column(Float, nullable=True)
    payment_amount = Column(Float, nullable=False)
    comments = Column(String, nullable=False ) 