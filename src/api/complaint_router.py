from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from src.data.connection import get_db
from src.schemas.complaint_schema import ComplaintCreate
from src.services.complaint_service import ComplaintService
from src.models.models import ComplaintStatus
from src.repositories.customer_repository_sqlalchemy import CustomerRepository
from src.repositories.account_repository_sqlalchemy import AccountRepository
from src.repositories.complaint_repository_sqlalchemy import ComplaintRepository


router = APIRouter(tags=["Complaints"])

service_complaint = ComplaintService(
    complaint_repository=ComplaintRepository(),
    customer_repository=CustomerRepository(),
    account_repository=AccountRepository()
)


@router.post("/complaints", status_code=201)
def create_complaint(complaint: ComplaintCreate,db: Session = Depends(get_db)):
    try:
        return service_complaint.create_complaint(db, complaint)
    except ValueError as error:
        raise HTTPException(status_code=422,detail=str(error))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/complaints")
def get_complaints(db: Session = Depends(get_db)):
    return service_complaint.get_complaints(db)


@router.get("/complaints/{complaint_id}")
def get_complaint_by_id(complaint_id:str,db: Session = Depends(get_db)):
    try:
        return service_complaint.get_complaint_by_id(db, complaint_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.patch("/complaints/{complaint_id}/status",
              responses={404: {"description": "Complaint not found"},
                        409: {"description": "Invalid status transition"}})
def update_complaint_status(complaint_id:str, new_status:ComplaintStatus = Body(...,embed=True),
                            changed_by:str|None=Body(None),
                            comments:str|None=Body(None),
                            db:Session = Depends(get_db)):
    try:
        return service_complaint.change_status(db=db, complaint_id=complaint_id,
                                               new_status=new_status, changed_by=changed_by,
                                               comments=comments)
    except ValueError as error:
        message = str(error)
         # the complaint does not exist
        if "does not exist" in message:
            raise HTTPException(status_code=404, detail=message)
         # the transition is not valid
        raise HTTPException(status_code=409, detail=message)
