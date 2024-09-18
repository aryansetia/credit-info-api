from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LoanBase(BaseModel):
    loan_amount: Optional[int] = None
    taken_on: Optional[datetime] = None
    loan_bank_provider: Optional[str] = None
    loan_status: Optional[str] = None

    class Config:
        orm_mode = True

class LoanCreate(LoanBase):
    loan_amount: int
    taken_on: datetime
    loan_bank_provider: str
    loan_status: str

class LoanUpdate(LoanBase):
    pass

