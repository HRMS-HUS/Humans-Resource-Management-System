from sqlalchemy import Column, ForeignKey, String, Date
from ..database import Base

class Job(Base):
    __tablename__ = "job"

    job_id = Column(String, primary_key=True, index=True, nullable=False)
    user_id = Column(String, ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    job_tittle = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)