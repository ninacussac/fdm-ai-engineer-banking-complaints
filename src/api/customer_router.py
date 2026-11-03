
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.data.connection import get_db
from src.schemas.customer_schema import CustomerCreate
from src.services.customer_service import CustomerService
from src.repositories.customer_repository_sqlalchemy import CustomerRepository


router = APIRouter(prefix="/bank", tags=["Customers"])

service_customer = CustomerService(
    customer_repository=CustomerRepository()
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
