
from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class AccountCreate(BaseModel):
    customer_id: str
    account_number: str
    account_type: str
    status: str
    opened_date: date
    current_balance: Decimal = Decimal("0.00")
