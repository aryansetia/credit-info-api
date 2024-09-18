from pydantic import BaseModel
from typing import Optional
from datetime import date

class CompanyBase(BaseModel):
    name: Optional[str] = None
    company_id: Optional[str] = None
    address: Optional[str] = None
    registration_date: Optional[date] = None  # It's still a date here
    number_of_employees: Optional[int] = None
    contact_number: Optional[str] = None
    contact_email: Optional[str] = None
    company_website: Optional[str] = None

    class Config:
        orm_mode = True

class CompanyCreate(CompanyBase):
    name: str
    company_id: str
    address: str
    registration_date: date
    number_of_employees: int
    contact_number: str
    contact_email: str

class CompanyUpdate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    
    @classmethod
    def from_orm(cls, obj):
        # Convert `registration_date` to string if it's not None
        data = super().from_orm(obj)
        if isinstance(data.registration_date, date):
            data.registration_date = data.registration_date.strftime('%Y-%m-%d')
        return data
