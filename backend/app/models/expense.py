from sqlalchemy import Column, ForeignKey, String, Float, Date
from ..database import Base

class Expense(Base):
    __tablename__ = "expense"
    expense_id = Column(String, primary_key=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    expense_item_name = Column(String,nullable=False )
    expense_item_store = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)