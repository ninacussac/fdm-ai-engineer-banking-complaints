
from sqlalchemy.orm import Session

from src.models.models import Account, generate_id


class AccountRepository:

    def create(self, db: Session, account_data):
        account = Account(
            account_id=generate_id(db, Account),
            customer_id=account_data.customer_id,
            account_number=account_data.account_number,
            account_type=account_data.account_type,
            status=account_data.status,
            opened_date=account_data.opened_date,
            current_balance=account_data.current_balance,
        )

        db.add(account)
        db.commit()
        db.refresh(account)

        return account

    def get_all(self, db: Session):
        return db.query(Account).all()

    def get_by_id(self, db: Session, account_id: str):
        return db.get(Account, account_id)
