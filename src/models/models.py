## spring2 brnach

from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import Numeric, String,ForeignKey,Integer, Column, DateTime, Date, Enum as SAEnum, select
from sqlalchemy.orm import DeclarativeBase, Session, validates


class Base(DeclarativeBase):
    pass

def enum_values(enum_class):
    return [member.value for member in enum_class]


from sqlalchemy import select
from sqlalchemy.orm import Session

def generate_id(session: Session, model: type) -> str:

    if model is Customer:
        attribute = Customer.customer_id
        prefix = "CUS"

    elif model is Account:
        attribute = Account.account_id
        prefix = "ACC"

    elif model is Complaint:
        attribute = Complaint.complaint_id
        prefix = "CMP"

    else:
        raise ValueError(f"Unsupported model: {model}")

    existing_ids = session.scalars(
        select(attribute)
    ).all()

    numbers = [
        int(existing_id[len(prefix):])
        for existing_id in existing_ids
        if existing_id.startswith(prefix)
        and existing_id[len(prefix):].isdigit()
    ]

    next_number = max(numbers, default=0) + 1

    return f"{prefix}{next_number:03d}"




class ComplaintStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    UNDER_REVIEW = "UNDER_REVIEW"
    CLOSED = "CLOSED"

class ComplaintCategory(str, Enum):
    FEE_DISPUTE = "Fee Dispute"
    SERVICE_DELAY = "Service Delay"
    TRANSACTION_ERROR = "Transaction Error"
    ONLINE_BANKING = "Online Banking"
    CARD_ISSUE = "Card Issue"
    CUSTOMER_SERVICE = "Customer Service"
    FRAUD_CLAIM = "Fraud Claim"

class ComplaintPriority(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

## sprint one documentation

VALID_STATUS_TRANSITIONS = {
    ComplaintStatus.OPEN: {
        ComplaintStatus.IN_PROGRESS
    },
    ComplaintStatus.IN_PROGRESS: {
        ComplaintStatus.UNDER_REVIEW
    },
    ComplaintStatus.UNDER_REVIEW: {
        ComplaintStatus.CLOSED
    },
    ComplaintStatus.CLOSED: set()
}


class Customer(Base):
    __tablename__ = "customer"
    customer_id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, default=None)
    phone_number = Column(String, default=None)
    segment = Column(String, default=None)
    date_created = Column(DateTime, default=datetime.now)


class Account(Base):
    __tablename__ = "account"
    account_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customer.customer_id"), nullable=False)
    account_number = Column(String, nullable=False, unique = True)
    account_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    opened_date = Column(Date, nullable=False)  
    current_balance = Column(Numeric(15, 2), default = Decimal("0.00"))


class Complaint(Base):
    __tablename__ = "complaint"
    complaint_id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customer.customer_id"), nullable = False)
    channel = Column(String, nullable=False)
    category = Column(SAEnum(ComplaintCategory,values_callable = enum_values), nullable=False)
    complaint_text = Column(String, nullable=False)
    status = Column(SAEnum(ComplaintStatus ,values_callable = enum_values), nullable=False)
    received_at = Column(DateTime, nullable=False, default=datetime.now) 

    account_id = Column(String, ForeignKey("account.account_id"), nullable=True)
    priority = Column(SAEnum(ComplaintPriority,values_callable = enum_values), nullable=True)
    assigned_analyst_id = Column(String, nullable=True)

    @validates("category", "status", "priority")
    def validate_enums(self, key, value):
        expected_type = {
            "category": ComplaintCategory,
            "priority": ComplaintPriority,
            "status": ComplaintStatus,
        }[key]

        if value is None and key == "priority":
            return value

        if not isinstance(value, expected_type):
            raise ValueError(f"Invalid {key}") 

        return value
    
    def change_status(
        self,
        new_status: ComplaintStatus,
        changed_by: str | None = None,
        comments: str | None = None
    ) -> "ComplaintStatusEvent":

        if not isinstance(new_status, ComplaintStatus):
            raise ValueError("Invalid complaint status")

        if new_status not in VALID_STATUS_TRANSITIONS[self.status]:
            raise ValueError(
                f"Invalid transition: {self.status.value} -> {new_status.value}"
            )

        event = ComplaintStatusEvent(
            complaint_id=self.complaint_id,
            old_status=self.status,
            new_status=new_status,
            changed_by=changed_by,
            comments=comments
        )

        self.status = new_status
        return event


class ComplaintStatusEvent(Base):
    __tablename__ = "complaint_status_history"

    history_id = Column(Integer, primary_key=True, index=True)

    complaint_id = Column(String, ForeignKey("complaint.complaint_id"), nullable=False)
    new_status = Column(SAEnum(ComplaintStatus,values_callable=enum_values), nullable=False)
    old_status = Column(SAEnum(ComplaintStatus,values_callable=enum_values), nullable=True)
    changed_by = Column(String, default=None)
    changed_at = Column(DateTime, default=datetime.now)
    comments = Column(String, default=None)

    @validates("new_status", "old_status")
    def validate_statuses(self, key, value):

        if value is None and key == "old_status":
            return value

        if not isinstance(value, ComplaintStatus):
            raise ValueError(f"Invalid {key}: {value}")

        return value
