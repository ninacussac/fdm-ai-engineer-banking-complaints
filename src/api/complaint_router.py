from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.data.connection import get_db
from src.schemas.complaint_schema import ComplaintCreate
from src.services.complaint_service import ComplaintService

from src.repositories.customer_repository_sqlalchemy import CustomerRepository
from src.repositories.account_repository_sqlalchemy import AccountRepository
from src.repositories.complaint_repository_sqlalchemy import ComplaintRepository


router = APIRouter(prefix="/bank", tags=["Complaints"])

service_complaint = ComplaintService(
    complaint_repository=ComplaintRepository(),
    customer_repository=CustomerRepository(),
    account_repository=AccountRepository()
)


@router.post("/complaints")
def create_complaint(complaint: ComplaintCreate,db: Session = Depends(get_db)):
    return service_complaint.create_complaint(db, complaint)


@router.get("/complaints")
def get_complaints(db: Session = Depends(get_db)):
    return service_complaint.get_complaints(db)
