from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnnualInformationBase(BaseModel):
    annual_turnover: Optional[int] = None
    profit: Optional[int] = None
    fiscal_year: Optional[int] = None
    reported_by_company_date: Optional[datetime] = None 

    class Config:
        orm_mode = True
        json_schema_extra = {
            "examples": [
                {
                    "annual_turnover": 1500000,
                    "profit": 300000,
                    "fiscal_year": 2023,
                    "reported_by_company_date": "2024-01-15T10:00:00Z"
                }
            ]
        }

class AnnualInformationCreate(AnnualInformationBase):
    annual_turnover: int
    profit: int
    fiscal_year: int
    reported_by_company_date: datetime 

class AnnualInformationUpdate(AnnualInformationBase):
    pass

