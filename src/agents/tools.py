from src.data.connection import SessionLocal
from src.services.customer_service import CustomerService
from src.repositories.customer_repository_sqlalchemy import CustomerRepository
from src.repositories.account_repository_sqlalchemy import AccountRepository
from src.repositories.complaint_repository_sqlalchemy import ComplaintRepository
from src.services.complaint_service import ComplaintService
from src.services.account_service import AccountService
from src.rag.retrieval_service import retrieve


def get_customer(customer_id: str):
    if not isinstance(customer_id, str) or not customer_id.strip():
        raise ValueError("customer_id is required")

    with SessionLocal() as db:
        customer_service = CustomerService(customer_repository=CustomerRepository())
        customer = customer_service.get_customer_by_id(db, customer_id)

        if customer is None:
            return None

        return {
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "segment": customer.segment,
        }



def get_accounts(customer_id: str):
    if not isinstance(customer_id, str) or not customer_id.strip():
        raise ValueError("customer_id is required")

    with SessionLocal() as db:
        account_service = AccountService(account_repository=AccountRepository())

        accounts = account_service.get_accounts_by_customer(db, customer_id)

        return [
            {
                "account_id": account.account_id,
                "customer_id": account.customer_id,
                "account_type": account.account_type,
                "status": account.status,
            }
            for account in accounts
        ]


def get_complaint(complaint_id: str) -> dict | None:
    if not isinstance(complaint_id, str) or not complaint_id.strip():
        raise ValueError("Invalid complaint ID.")
    complaint_service = ComplaintService(
        complaint_repository=ComplaintRepository(),
        customer_repository=CustomerRepository(),
        account_repository=AccountRepository(),
    )
    with SessionLocal() as db:
        return complaint_service.get_complaint_with_history(db, complaint_id)


def search_policy(query, top_k=3):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query is required")

    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
        raise ValueError("top_k must be a positive integer")

    return retrieve(
        query=query,
        top_k=top_k
    )