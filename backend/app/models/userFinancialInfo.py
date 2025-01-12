from sqlalchemy import Column, ForeignKey, String, Float, Sequence
from sqlalchemy.orm import relationship
from ..configs.database import Base

class UserFinancialInfo(Base):
    __tablename__ = "users_financial_info"

    financial_info_id = Column(String, Sequence("personal_id_seq"), primary_key=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    salaryBasic = Column(Float, nullable=False)
    salaryGross = Column(Float, nullable=False)
    salaryNet = Column(Float, nullable=False)
    allowanceHouseRent = Column(Float, nullable=True)
    allowanceMedical = Column(Float, nullable=True)
    allowanceSpecial = Column(Float, nullable=True)
    allowanceFuel = Column(Float, nullable=True)
    allowancePhoneBill = Column(Float, nullable=True)
    allowanceOther = Column(Float, nullable=True)
    allowanceTotal = Column(Float, nullable=True)
    deductionProvidentFund = Column(Float, nullable=True)
    deductionTax = Column(Float, nullable=True)
    deductionOther = Column(Float, nullable=True)
    deductionTotal = Column(Float, nullable=True)
    bankName = Column(String, nullable=True)
    accountName = Column(String, nullable=True)
    accountNumber = Column(String, nullable=True)
    iban = Column(String, nullable=True)
    
    # Relationships
    user = relationship("Users", back_populates="financial_info")