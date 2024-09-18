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

class AnnualInformationCreate(AnnualInformationBase):
    annual_turnover: int
    profit: int
    fiscal_year: int
    reported_by_company_date: datetime 

class AnnualInformationUpdate(AnnualInformationBase):
    pass

