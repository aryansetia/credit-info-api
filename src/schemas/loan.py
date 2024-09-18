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
        json_schema_extra = {
            "examples": [
                {
                    "loan_amount": 50000,
                    "taken_on": "2023-08-15T12:34:56Z",
                    "loan_bank_provider": "Bank of Springfield",
                    "loan_status": "DUE"
                }
            ]
        }
class LoanCreate(LoanBase):
    loan_amount: int
    taken_on: datetime
    loan_bank_provider: str
    loan_status: str

class LoanUpdate(LoanBase):
    pass

