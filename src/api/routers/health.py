from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.data.connection import engine

router = APIRouter(prefix="/health",tags=["Health"])

@router.get("/live")
def liveness_check():
    return {"status": "alive"}


@router.get("/ready")
def readiness_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"status": "ready"}

    except SQLAlchemyError:
        raise HTTPException(status_code=503,detail="Database unavailable")