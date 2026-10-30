
from datetime import datetime

from pydantic import BaseModel, Field

from src.models.models import ComplaintStatus


class ComplaintStatusEventCreate(BaseModel):
    complaint_id: str
    new_status: ComplaintStatus
    old_status: ComplaintStatus
    changed_by: str | None = None
    changed_at: datetime = Field(default_factory=datetime.now)
    comments: str | None = None
