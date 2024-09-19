from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv


load_dotenv()  

DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://postgres:postgres@db:5433/credit-info")

if not DATABASE_URL: 
    raise ValueError("DATABASE_URL environment variable is not set")


engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    try:
        from src.models.annual_information import AnnualInformation
        from src.models.loan import Loan
        from src.models.company import Company

        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
