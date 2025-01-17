from pydantic import BaseModel
from datetime import date
from typing import Optional

class ExpenseBase(BaseModel):
    expense_item_name: Optional[str] = None
    expense_item_store: Optional[str] = None
    expense_date: Optional[date] = None
    amount: Optional[float] = None

class ExpenseCreate(ExpenseBase):
    user_id: Optional[str] = None

class ExpenseUpdate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    expense_id: str
    user_id: str

    class Config:
        orm_mode = True
