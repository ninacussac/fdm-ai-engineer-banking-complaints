
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.data.connection import get_db
from src.schemas.customer_schema import CustomerCreate
from src.services.customer_service import CustomerService
from src.repositories.customer_repository_sqlalchemy import CustomerRepository
from src.services.complaint_service import ComplaintService
from src.repositories.complaint_repository_sqlalchemy import ComplaintRepository
from src.repositories.account_repository_sqlalchemy import AccountRepository

router = APIRouter(tags=["Customers"])

service_customer = CustomerService(customer_repository=CustomerRepository())

service_complaint = ComplaintService(
    complaint_repository=ComplaintRepository(),
    customer_repository=CustomerRepository(),
    account_repository=AccountRepository()
)

@router.post("/customers")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    return service_customer.create_customer(db, customer)


@router.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    return service_customer.get_customers(db)


@router.get("/customers/{customer_id}")
def get_customer_id( customer_id:str, db:Session = Depends(get_db)):
    try :
        return service_customer.get_customer_by_id(db,customer_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

@router.get("/customers/{customer_id}/complaints")
def get_customer_complaints(customer_id:str, db:Session=Depends(get_db)):
    try:
        return service_complaint.get_customer_complaints(db,customer_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
