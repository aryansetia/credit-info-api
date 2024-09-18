from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db import get_db
from models.company import Company
from models.annual_information import AnnualInformation
from models.loan import Loan
from schemas.annual_information import AnnualInformationCreate, AnnualInformationUpdate
from schemas.loan import LoanCreate, LoanUpdate
from typing import List, Optional


router = APIRouter()


# helper function to calculate credit information
def calculate_credit(company_id: int, db: Session):

    annual_info = (
        db.query(AnnualInformation)
        .filter(AnnualInformation.company_id == company_id)
        .order_by(AnnualInformation.fiscal_year.desc())
        .limit(2)
        .all()
    )

    due_loans = (
        db.query(Loan)
        .filter(Loan.company_id == company_id, Loan.loan_status == "DUE")
        .all()
    )

    total_turnover = sum(ai.annual_turnover for ai in annual_info)
    total_due_loans = sum(loan.loan_amount for loan in due_loans)

    credit_info = total_turnover - total_due_loans
    return credit_info


# GET - to fetch credits information of all the companies
@router.get("/credits", response_model=List[dict], status_code=status.HTTP_200_OK)
def get_all_credits(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    credits = []
    if not companies:
        raise HTTPException(status_code=404, detail="No companies found")
    try:
        for company in companies:
            credit_info = calculate_credit(company.id, db)
            credits.append({
                "company_id": company.company_id,
                "company_name": company.name,
                "credit_info": credit_info
            })
        return JSONResponse(
            {
                "message": "success",
                "data": credits
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# GET - to fetch the credit information of a specific company using its id
@router.get("/credits/{company_id}", response_model=dict, status_code=status.HTTP_200_OK)
def get_credit_by_company_id(company_id: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(
        Company.company_id == company_id).first()
    
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    try:
        credit_info = calculate_credit(company.id, db)

        return JSONResponse(
            content={
                "message": "success",
                "data": {
                    "company_id": company.company_id,
                    "company_name": company.name,
                    "credit_info": credit_info
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# POST - to add credit information of a company by adding annual and loan information
@router.post("/credits/{company_id}", response_model=dict, status_code=status.HTTP_201_CREATED)
def add_credit_info(company_id: str,
                    annual_info: AnnualInformationCreate,
                    loan_info: LoanCreate,
                    db: Session = Depends(get_db)):

    # Check if company exists
    company = db.query(Company).filter(
        Company.company_id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    new_annual_info = AnnualInformation(
        annual_turnover=annual_info.annual_turnover,
        profit=annual_info.profit,
        fiscal_year=annual_info.fiscal_year,
        reported_by_company_date=annual_info.reported_by_company_date,
        company_id=company.id
    )

    new_loan = Loan(
        loan_amount=loan_info.loan_amount,
        taken_on=loan_info.taken_on,
        loan_bank_provider=loan_info.loan_bank_provider,
        loan_status=loan_info.loan_status,
        company_id=company.id
    )

    try:
        db.add(new_annual_info)
        db.add(new_loan)
        db.commit()

        return JSONResponse(
            content={
                "message": "Credit information added successfully",
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")


# PUT - simulate updating credit information of a company 
@router.put("/credits/{company_id}", response_model=dict, status_code=status.HTTP_200_OK)
def update_credit_info(company_id: str, annual_info: Optional[AnnualInformationUpdate] = None, loan_info: Optional[LoanUpdate] = None, db: Session = Depends(get_db)):
    company = db.query(Company).filter(
        Company.company_id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

 
    return JSONResponse(
        content={
            "message": "Credit information updated successfully"
        }
    )
  
# DELETE - simulate deleting credit information of a company
@router.delete("/credits/{company_id}", response_model=dict, status_code=status.HTTP_200_OK)
def delete_credit_info(company_id: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(
        Company.company_id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return JSONResponse(
        content={
            "message": "Credit information deleted successfully"
        }
    )
