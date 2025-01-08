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

class UserFinancialInfoUpdate(BaseModel):
    salaryBasic: Optional[float] = None
    salaryGross: Optional[float] = None
    salaryNet: Optional[float] = None
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
    bankName: Optional[str] = None
    accountName: Optional[str] = None
    accountNumber: Optional[str] = None
    iban: Optional[str] = None

class UserFinancialInfoResponse(UserFinancialInfoBase):
    financial_info_id: str

    class Config:
        orm_mode = True