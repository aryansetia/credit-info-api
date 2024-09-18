from pydantic import BaseModel
from typing import Optional
from datetime import date

class CompanyBase(BaseModel):
    name: Optional[str] = None
    company_id: Optional[str] = None
    address: Optional[str] = None
    registration_date: Optional[date] = None  
    number_of_employees: Optional[int] = None
    contact_number: Optional[str] = None
    contact_email: Optional[str] = None
    company_website: Optional[str] = None

    class Config:
        orm_mode = True

        json_schema_extra = {
            "examples": [
                {
                    "name": "Acme Corp",
                    "company_id": "12345",
                    "address": "123 Elm Street, Springfield",
                    "registration_date": "2022-01-01",
                    "number_of_employees": 100,
                    "contact_number": "+1-555-1234",
                    "contact_email": "contact@acme.com",
                    "company_website": "https://www.acme.com"
                }
            ]
        }

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
        data = super().from_orm(obj)
        if isinstance(data.registration_date, date):
            data.registration_date = data.registration_date.strftime('%Y-%m-%d')
        return data
