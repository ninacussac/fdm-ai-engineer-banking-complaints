from decimal import Decimal

from pydantic import BaseModel, Field
from datetime import datetime, date

from src.models.models import ComplaintCategory, ComplaintStatus, ComplaintPriority


class CustomerCreate(BaseModel):
    first_name:str
    last_name:str
    email:str | None = None
    phone_number:str | None = None
    segment:str | None = None
    date_created: datetime = Field(default_factory=datetime.now)


class AccountCreate(BaseModel):
    customer_id:str
    account_number:str
    account_type:str
    status:str
    opened_date:date
    current_balance: Decimal = Decimal("0.00")


class ComplaintCreate(BaseModel):
    customer_id:str
    channel:str
    category:ComplaintCategory
    complaint_text:str
    status:ComplaintStatus
    received_at:datetime = Field(default_factory=datetime.now)
    account_id:str
    priority:ComplaintPriority
    assigned_analyst_id:str|None = None


class ComplaintStatusEventCreate(BaseModel):
    complaint_id:str
    new_status:ComplaintStatus
    old_status:ComplaintStatus
    changed_by:str|None = None
    changed_at:datetime = Field(default_factory=datetime.now)
    comments:str|None = None