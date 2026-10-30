from datetime import datetime

from pydantic import BaseModel, Field

from src.models.models import (
    ComplaintCategory,
    ComplaintStatus,
    ComplaintPriority
)

class ComplaintCreate(BaseModel):
    customer_id: str
    channel: str
    category: ComplaintCategory
    complaint_text: str
    status: ComplaintStatus
    received_at: datetime = Field(default_factory=datetime.now)
    account_id: str|None = None
    priority: ComplaintPriority
    assigned_analyst_id: str | None = None
