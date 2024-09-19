from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.db import Base
import enum

class LoanStatus(str, enum.Enum):
    PAID = "PAID"
    DUE = "DUE"
    INITIATED = "INITIATED"

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    loan_amount = Column(Float, nullable=False)
    taken_on = Column(Date, nullable=False)
    loan_bank_provider = Column(String, nullable=False)
    loan_status = Column(Enum(LoanStatus), default=LoanStatus.INITIATED)

    company = relationship("Company", back_populates="loans")
