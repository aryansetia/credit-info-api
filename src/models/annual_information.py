from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from src.db import Base

class AnnualInformation(Base):
    __tablename__ = "annual_information"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    annual_turnover = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)
    fiscal_year = Column(String, nullable=False)
    reported_by_company_date = Column(Date, nullable=False)

    company = relationship("Company", back_populates="annual_info")
