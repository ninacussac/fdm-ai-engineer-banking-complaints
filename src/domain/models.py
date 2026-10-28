from dataclasses import dataclass, field
from datetime import datetime,date
from decimal import Decimal
from enum import Enum

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

@dataclass
class Customer:
    customer_id: str
    first_name: str
    last_name: str
    email: str | None = None
    phone_number: str | None = None
    segment: str | None = None
    date_created: datetime = field(default_factory=datetime.now)

@dataclass
class Account:
    account_id:str
    customer_id:str
    account_number:str
    account_type:str
    status:str
    opened_date:date
    current_balance:Decimal=field(
        default_factory=lambda:Decimal("0.00")
    )

@dataclass
class Complaint:
    complaint_id:str
    customer_id:str
    channel:str
    category:ComplaintCategory
    complaint_text:str
    status:ComplaintStatus
    received_at:datetime

    account_id:str|None=None
    priority:ComplaintPriority|None=None
    assigned_analyst_id:str|None=None

    def __post_init__(self):
        if not isinstance(self.category, ComplaintCategory):
            raise ValueError("Invalid complaint category")

        if not isinstance(self.status, ComplaintStatus):
            raise ValueError("Invalid complaint status")

        if (self.priority is not None
            and not isinstance(self.priority, ComplaintPriority)):
            raise ValueError("Invalid complaint priority")

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

        old_status = self.status

        event = ComplaintStatusEvent(
            complaint_id=self.complaint_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by,
            comments=comments
        )

        self.status = new_status

        return event

@dataclass
class ComplaintStatusEvent:
    complaint_id:str
    new_status:ComplaintStatus

    history_id:int|None=None
    old_status:ComplaintStatus|None=None
    changed_by:str|None=None
    changed_at:datetime= field(default_factory=datetime.now)
    comments:str|None=None

    def __post_init__(self):
        if not isinstance(self.new_status, ComplaintStatus):
            raise ValueError("Invalid new status")

        if (
            self.old_status is not None
            and not isinstance(self.old_status, ComplaintStatus)
        ):
            raise ValueError("Invalid old status")
