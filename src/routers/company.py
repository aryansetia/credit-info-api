from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from src.db import get_db
from src.models.company import Company
from fastapi.responses import JSONResponse
from src.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse


router = APIRouter()

# POST - to create a new company 
@router.post("/company", response_model=CompanyResponse, status_code=201)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(
        name=company.name,
        company_id=company.company_id,
        address=company.address,
        registration_date=company.registration_date,
        number_of_employees=company.number_of_employees,
        contact_number=company.contact_number,
        contact_email=company.contact_email,
        company_website=company.company_website
    )

    try:
        db.add(db_company)
        db.commit()
        response_data = {
            "message": "Company created successfully",
        }
        return JSONResponse(content=response_data, status_code=201)
    
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Database error: {str(e.orig)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


# GET - to get all companies
@router.put("/company/{company_id}", response_model=CompanyResponse)
def update_company(company_id: str, company: CompanyUpdate, db: Session = Depends(get_db)):
    try:
        print("company_id", company_id)
        # Raises NoResultFound if not found
        db_company = db.query(Company).filter(
            Company.company_id == company_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Company not found")

    try:
        for key, value in company.dict(exclude_unset=True).items():
            setattr(db_company, key, value)

        db.commit()
        db.refresh(db_company)
        return db_company
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid data: {str(e.orig)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
