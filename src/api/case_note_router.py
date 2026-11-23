from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.data.connection import get_db
from src.schemas.case_note_schema import CaseNoteCreate
from src.services.case_note_service import CaseNoteService
from src.security.auth import AuthenticatedActor,get_authenticated_actor
from src.api.error_handlers import AppError

router = APIRouter(tags=["Case Notes"])

case_note_service = CaseNoteService()

@router.post("/complaints/{complaint_id}/notes",status_code=201)
def create_case_note(
    complaint_id: str,
    payload: CaseNoteCreate,
    db: Session = Depends(get_db),
    actor: AuthenticatedActor = Depends(get_authenticated_actor),
):
    try:
        return case_note_service.create_case_note(
            db=db,
            complaint_id=complaint_id,
            note=payload.note,
            evidence_refs=payload.evidence_refs,
            actor_id=actor.actor_id,
            actor_role=actor.role,
        )

    except PermissionError:
        raise AppError(
            code="ACCESS_DENIED",
            message="You are not authorized to create case notes.",
            status_code=403#Forbidden
        )

    except ValueError:
        raise AppError(
            code="INVALID_CASE_NOTE",
            message="Invalid case note data.",
            status_code=422#Unprocessable Content
        )

    except SQLAlchemyError:
        raise AppError(
            code="DEPENDENCY_UNAVAILABLE",
            message="Database unavailable.",
            status_code=503 #service unavailable
        )
