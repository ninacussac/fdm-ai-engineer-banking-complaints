from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from src.data.connection import get_db
from src.schemas.complaint_schema import ComplaintCreate
from src.services.complaint_service import ComplaintService
from src.models.models import ComplaintStatus
from src.repositories.customer_repository_sqlalchemy import CustomerRepository
from src.repositories.account_repository_sqlalchemy import AccountRepository
from src.repositories.complaint_repository_sqlalchemy import ComplaintRepository
from src.api.error_handlers import AppError

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
    except ValueError:
        raise AppError(
            code="INVALID_COMPLAINT_DATA",
            message="Invalid complaint data",
            status_code=422
        )
    except OperationalError:
        raise AppError(
            code="DEPENDENCY_UNAVAILABLE",
            message="Database unavailable",
            status_code=503
        )
    except Exception:
        raise AppError(
            code="INTERNAL_ERROR",
            message="Internal server error",
            status_code=500
        )

@router.get("/complaints")
def get_complaints(db: Session = Depends(get_db)):
    return service_complaint.get_complaints(db)



@router.get("/complaints/{complaint_id}",
    responses={404: {"description": "Complaint not found"},
                503: {"description": "Database unavailable"},},)
def get_complaint_by_id(complaint_id: str,db: Session = Depends(get_db)):
    try:
        complaint = service_complaint.get_complaint_with_history(db, complaint_id)

        if complaint is None:
            raise AppError(
                code="COMPLAINT_NOT_FOUND",
                message="Complaint not found",
                status_code=404,
            )

        return complaint

    except OperationalError:
        raise AppError(
            code="DEPENDENCY_UNAVAILABLE",
            message="Database unavailable",
            status_code=503,
        )



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
        if "does not exist" in message:
            raise AppError(
                code = "COMPLAINT_NOT_FOUND",
                message = "Complaint not found",
                status_code = 404
            )
         # the transition is not valid
        raise AppError(
            code = "INVALID_STATUS_TRANSITION",
            message = "Invalid status transition",
            status_code=409
        )
