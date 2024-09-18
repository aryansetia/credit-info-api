from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from db import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    company_id = Column(String, unique=True, nullable=False, index=True)
    address = Column(String, nullable=False)
    registration_date = Column(Date, nullable=False)
    number_of_employees = Column(Integer, nullable=False)
    contact_number = Column(String, nullable=False)
    contact_email = Column(String, nullable=False, unique=True)
    company_website = Column(String, nullable=False)

    annual_info = relationship("AnnualInformation", back_populates="company", cascade="all, delete")
    loans = relationship("Loan", back_populates="company", cascade="all, delete")
