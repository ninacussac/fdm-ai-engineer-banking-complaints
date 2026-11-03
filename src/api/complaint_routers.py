from fastapi import FastAPI,APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from src.data.connection import get_db
from src.schemas.customer_schema import CustomerCreate, ComplaintCreate, AccountCreate, ComplaintStatusEventCreate
from src.services.customer_service import CustomerService, ComplaintService, AccountService, ComplaintStatusEventService
service_customer = CustomerService()
service_account = AccountService()
service_complaint = ComplaintService()
service_event = ComplaintStatusEventService()

PREFIX_URL = "/bank"
router = APIRouter(prefix=PREFIX_URL)

@router.post("/customers")
def create_customer(customer:CustomerCreate,db:Session=Depends(get_db)):
    return service_customer.create_customer(db,customer)

@router.get("/customers")
def get_customers(db:Session=Depends(get_db)):
    return service_customer.get_customers(db)


@router.post("/accounts")
def create_account(account:AccountCreate,db:Session=Depends(get_db)):
    return service_account.create_account(db,account)

@router.get("/accounts")
def get_accounts(db:Session=Depends(get_db)):
    return service_account.get_accounts(db)


@router.post("/complaints")
def create_complaint(complaint:ComplaintCreate,db:Session=Depends(get_db)):
    return service_complaint.create_complaint(db,complaint)

@router.get("/complaints")
def get_complaints(db:Session=Depends(get_db)):
    return service_complaint.get_complaints(db)


@router.post("/events")
def create_event(event:ComplaintStatusEventCreate,db:Session=Depends(get_db)):
    return service_event.create_event(db,event)

@router.get("/events")
def get_events(db:Session=Depends(get_db)):
    return service_event.get_events(db)
