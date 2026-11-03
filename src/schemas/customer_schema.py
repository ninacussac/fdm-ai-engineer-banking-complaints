from pydantic import BaseModel, Field
from datetime import datetime


class CustomerCreate(BaseModel):
    first_name:str
    last_name:str
    email:str | None = None
    phone_number:str | None = None
    segment:str | None = None
    date_created: datetime = Field(default_factory=datetime.now)