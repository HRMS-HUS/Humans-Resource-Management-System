# schemas/userFinancialInfo.py
from pydantic import BaseModel, Field
from typing import Optional

class UserFinancialInfoBase(BaseModel):
    user_id: str
    salaryBasic: float 
    salaryGross: float
    salaryNet: float
    allowanceHouseRent: Optional[float] = None
    allowanceMedical: Optional[float] = None
    allowanceSpecial: Optional[float] = None
    allowanceFuel: Optional[float] = None
    allowancePhoneBill: Optional[float] = None
    allowanceOther: Optional[float] = None
    allowanceTotal: Optional[float] = None
    deductionProvidentFund: Optional[float] = None
    deductionTax: Optional[float] = None
    deductionOther: Optional[float] = None
    deductionTotal: Optional[float] = None
    bankName: str
    accountName: str
    accountNumber: str
    iban: Optional[str] = None

class UserFinancialInfoCreate(UserFinancialInfoBase):
    pass

class UserFinancialInfoResponse(UserFinancialInfoBase):
    financial_info_id: str