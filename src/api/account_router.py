from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.schemas.account_schema import AccountCreate
from src.services.account_service import AccountService
from src.repositories.account_repository_sqlalchemy import AccountRepository


router = APIRouter(tags=["Accounts"])

service_account = AccountService(
    account_repository=AccountRepository()
)


@router.post("/accounts")
def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db)
):
    return service_account.create_account(db, account)


@router.get("/accounts")
def get_accounts(db: Session = Depends(get_db)):
    return service_account.get_accounts(db)
