from fastapi import APIRouter

from src.schemas.policy_schema import PolicyQuery
from src.rag.answer_service import answer_question
from src.api.error_handlers import AppError

router = APIRouter(prefix="/policy", tags=["Policy"])

@router.post("/query",
    responses={
        422: {"description": "Invalid request"},
        503: {"description": "Policy service unavailable"},
    },
)
def query_policy(request: PolicyQuery):
    try:
        return answer_question(request.question,document_type=request.document_type,
            effective_version=request.effective_version,access_label=request.access_label,)

    except ValueError:
        raise AppError(
            code="INVALID_QUERY",
            message="Invalid policy question",
            status_code=422,
        )

    except Exception:
        raise AppError(
            code="POLICY_SERVICE_UNAVAILABLE",
            message="Policy answer service unavailable",
            status_code=503,
        )