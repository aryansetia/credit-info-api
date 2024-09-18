from fastapi import FastAPI, Request
from db import create_tables
from routers import credits, company
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


# Create FastAPI instance
app = FastAPI(
    title="Credit Information API",
    description="An API to manage credit and company information.",
    version="1.0.0",)

app.include_router(company.router)
app.include_router(credits.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Credit Information API"}

@app.on_event("startup")
def on_startup():
    create_tables()
