from mcp.server.fastmcp import FastMCP
from pydantic import Field

from src.agents.tools import get_customer as lookup_customer,get_accounts as lookup_accounts,get_complaint as lookup_complaint,search_policy as lookup_policy
from src.data.connection import SessionLocal
from src.services.case_note_service import CaseNoteService
from src.security.mcp_auth import get_mcp_actor

mcp = FastMCP("BankingComplaintMCP")
case_note_service = CaseNoteService()

# T-001: Customer Lookup
@mcp.tool(name="get_customer",
    description="Returns the information on a customer given its customer_id id.")
def get_customer(
    customer_id: str = Field(description="Id of the customer that will be look up")
    ) -> dict | None:
    """Retrieve a synthetic customer by ID."""
    return lookup_customer(customer_id)


# T-002: Account Lookup
@mcp.tool(name="get_accounts",
    description="Returns the information on all the accounts of the customer given the customer_id id.")
def get_accounts(
    customer_id: str = Field(description="Id of the customer that will be look up")
                 ) -> list[dict]:
    """Retrieve account summaries for a customer."""
    return lookup_accounts(customer_id)


# T-003: Complaint Lookup
@mcp.tool(name="get_complaint",
    description="Returns the information on a complaint given its complaint_id id.")
def get_complaint(
    complaint_id: str = Field(description="Id of the complaint that will be retrieve")
    ) -> dict | None:
    """Retrieve complaint details by ID."""
    return lookup_complaint(complaint_id)


# T-004: Policy Lookup
@mcp.tool(name="search_policy",
    description="Search approved internal banking policy documents "
        "and return the top_k most relevant evidence chunks "
        "with their metadata.")
def search_policy(
    query: str = Field(description="Natural language query used to search banking "
                "policies, procedures, and complaint guidelines."), 
    top_k: int = Field(default = 3,  description="Maximum number of policy chunks to return.")
    ) -> list[dict]:
    """Search approved internal banking policies."""
    return lookup_policy(query=query,top_k=top_k)


# # T-005: Create Case Note
# @mcp.tool(name="create_case_note", 
#           description="Create a case note and record an audit event.")
# def create_case_note(
#     complaint_id: str = Field(description="ID of the complaint."),
#     note: str = Field(description="Content of the case note."),
#     evidence_refs: list[str] = Field(description="Supporting evidence references."),
# ) -> dict:

#     actor = get_mcp_actor()

#     with SessionLocal() as db:
#         return case_note_service.create_case_note(
#             db=db,
#             complaint_id=complaint_id,
#             note=note,
#             evidence_refs=evidence_refs,
#             actor_id=actor.actor_id,
#             actor_role=actor.role,
#         )


if __name__ == "__main__":
    mcp.run(transport="stdio")