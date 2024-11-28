from sqlalchemy import Column, String
from ..database import Base

class Department(Base):
    __tablename__ = "department"
    department_id = Column(String, primary_key=True, index=True, nullable=False)
    department_name = Column(String, nullable=False)