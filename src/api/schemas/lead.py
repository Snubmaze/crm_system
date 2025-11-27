from datetime import datetime
from pydantic import BaseModel, EmailStr


class LeadTicketShort(BaseModel):
    id: int
    source_name: str
    operator_id: int | None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LeadResponse(BaseModel):
    id: int
    email: EmailStr
    tickets: list[LeadTicketShort]

    class Config:
        from_attributes = True
