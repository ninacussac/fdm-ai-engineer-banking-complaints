from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.rag.answer_service import answer_question
from src.api.error_handlers import AppError


router = APIRouter(prefix="/policy", tags=["Policy"])


class PolicyQuery(BaseModel):
    question: str = Field(min_length=1)


@router.post("/query")
def query_policy(request: PolicyQuery):
    try:
        return answer_question(request.question)

    except ValueError:
        raise AppError(
            code="INVALID_QUERY",
            message="Invalid policy question",
            status_code=400
        )

    except Exception:
        raise AppError(
            code="POLICY_SERVICE_UNAVAILABLE",
            message="Policy answer service unavailable",
            status_code=503
        )
