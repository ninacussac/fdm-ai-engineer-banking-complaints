from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.data.connection import get_db
from src.schemas.complaint_status_event_schema import (ComplaintStatusEventCreate)
from src.services.complaint_status_event_service import (ComplaintStatusEventService)
from src.repositories.complaint_status_event_repository_sqlalchemy import (ComplaintStatusEventRepository)


router = APIRouter(tags=["Complaint Status Events"])

service_event = ComplaintStatusEventService(event_repository=ComplaintStatusEventRepository())


@router.post("/events")
def create_event(event: ComplaintStatusEventCreate,db: Session = Depends(get_db)):
    return service_event.create_event(db, event)


@router.get("/events")
def get_events(db: Session = Depends(get_db)):
    return service_event.get_events(db)
