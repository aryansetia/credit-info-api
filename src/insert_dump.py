from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from src.models.annual_information import AnnualInformation
from src.models.loan import Loan
from src.models.company import Company
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from faker import Faker
from datetime import datetime, timedelta
import random
import os

fake = Faker()

Base = declarative_base()

DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://postgres:postgres@db:5433/credit-info")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

# Create a new session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to generate random date
def generate_random_date(start_year, end_year):
    start_date = datetime(year=start_year, month=1, day=1)
    end_date = datetime(year=end_year, month=12, day=31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def insert_dummy_data(db: Session):
    # Create dummy companies
    companies = []
    for _ in range(10):
        company = Company(
            name=fake.company(),
            company_id=fake.uuid4(),
            address=fake.address(),
            registration_date=fake.date_this_decade(),
            number_of_employees=fake.random_int(min=50, max=500),
            contact_number=fake.phone_number(),
            contact_email=fake.email(),
            company_website=fake.url()
        )
        companies.append(company)

    db.add_all(companies)
    db.commit()

    # Insert dummy annual information
    annual_infos = []
    for company in companies:
        for year in range(2021, 2023):
            annual_info = AnnualInformation(
                company_id=company.id,
                annual_turnover=fake.random_number(digits=9),
                profit=fake.random_number(digits=8),
                fiscal_year=year,
                reported_by_company_date=fake.date_this_year()
            )
            annual_infos.append(annual_info)

    db.add_all(annual_infos)
    db.commit()

    # Insert dummy loans
    loans = []
    loan_statuses = ["PAID", "DUE", "INITIATED"]
    for company in companies:
        for _ in range(2):
            loan = Loan(
                company_id=company.id,
                loan_amount=fake.random_number(digits=7),
                taken_on=generate_random_date(2020, 2023),
                loan_bank_provider=fake.company(),
                loan_status=random.choice(loan_statuses)
            )
            loans.append(loan)

    db.add_all(loans)
    db.commit()


if __name__ == "__main__":
    with SessionLocal() as db:
        insert_dummy_data(db)
