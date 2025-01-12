from sqlalchemy import Column, ForeignKey, String, Float, Date, Sequence
from ..configs.database import Base

class Expense(Base):
    __tablename__ = "expense"
    expense_id = Column(String, Sequence("expense_id_seq"),primary_key=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    expense_item_name = Column(String,nullable=True)
    expense_item_store = Column(String, nullable=True)
    expense_date = Column(Date, nullable=True)
    amount = Column(Float, nullable=True)