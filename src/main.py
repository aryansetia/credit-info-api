from fastapi import FastAPI
from sqlalchemy.orm import Session
from src.db import create_tables, SessionLocal
from src.routers import credits, company, user_login
from src.models.company import Company
from src.insert_dump import insert_dummy_data

app = FastAPI(
    title="Credit Information API",
    description="An API to manage credit and company information.",
    version="1.0.0",
)

app.include_router(company.router)
app.include_router(credits.router)
app.include_router(user_login.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Credit Information API"}

@app.on_event("startup")
async def on_startup():
    create_tables()  # Ensure tables are created
    
    with SessionLocal() as db:
        try:
            # Check if the table contains any rows
            count = db.query(Company).count()
            
            if count == 0:
                print("Database is empty. Inserting dummy data...")
                insert_dummy_data(db)
            else:
                print("Database already populated.")
                
        except Exception as e:
            print("Error during startup:", e)
            # Handle exception (e.g., logging the error)
