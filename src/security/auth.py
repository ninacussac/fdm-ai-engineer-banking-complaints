
import secrets
from dataclasses import dataclass

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config import settings


@dataclass(frozen=True)
class AuthenticatedActor:
    actor_id: str
    role: str


bearer_scheme = HTTPBearer(auto_error=False)


def resolve_actor_from_token(token: str | None) -> AuthenticatedActor:

    if not token:
        raise PermissionError("Missing authentication token.")

    users = [
        (settings.BANKING_ANALYST_TOKEN,
         settings.BANKING_ANALYST_ID, "Analyst"),

        (settings.BANKING_SUPERVISOR_TOKEN,
         settings.BANKING_SUPERVISOR_ID, "Supervisor"),

        (settings.BANKING_VIEWER_TOKEN,
         settings.BANKING_VIEWER_ID, "Viewer"),
    ]

    for configured_token, actor_id, role in users:
        if configured_token and secrets.compare_digest(
            token, configured_token
        ):
            return AuthenticatedActor(
                actor_id=actor_id,
                role=role,
            )

    raise PermissionError("Invalid authentication token.")


def get_authenticated_actor(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
) -> AuthenticatedActor:

    try:
        token = credentials.credentials if credentials else None
        return resolve_actor_from_token(token)

    except PermissionError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
