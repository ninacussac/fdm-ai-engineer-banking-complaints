
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.middleware.auth_context import get_access_token

from src.security.auth import AuthenticatedActor,resolve_actor_from_token


MCP_RESOURCE_URL = "http://127.0.0.1:8000/mcp"


class BankingTokenVerifier(TokenVerifier):

    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            actor = resolve_actor_from_token(token)

        except PermissionError:
            return None

        return AccessToken(
            token=token,
            client_id="banking-cli",
            subject=actor.actor_id,
            scopes=[f"role:{actor.role}"],
            resource=MCP_RESOURCE_URL,
        )


def get_mcp_actor() -> AuthenticatedActor:

    access_token = get_access_token()

    if access_token is None or not access_token.subject:
        raise PermissionError("Authentication required.")

    allowed_roles = {"Analyst", "Supervisor", "Viewer"}

    roles = [
        role
        for role in allowed_roles
        if f"role:{role}" in access_token.scopes
    ]

    if len(roles) != 1:
        raise PermissionError("Invalid actor role.")

    return AuthenticatedActor(
        actor_id=access_token.subject,
        role=roles[0],
    )