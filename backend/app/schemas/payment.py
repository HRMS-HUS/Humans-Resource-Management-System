from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import date

class PaymentMethodEnum(str, Enum):
    Check = "Check"
    Bank_Transfer = "Bank Transfer"
    Cash = "Cash"

class PaymentBase(BaseModel):
    user_id: str
    payment_method: Optional[PaymentMethodEnum] = None
    payment_month: Optional[int] = None
    payment_date: Optional[int] = None
    payment_amount: Optional[float] = None
    comments: Optional[str] = None
    payment_fine: Optional[float] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    payment_method: Optional[PaymentMethodEnum] = None
    payment_month: Optional[int] = None
    payment_date: Optional[int] = None
    payment_amount: Optional[float] = None
    comments: Optional[str] = None
    payment_fine: Optional[float] = None

class PaymentResponse(PaymentBase):
    payment_id: str

    class Config:
        orm_mode = True
