from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class TicketCreate(BaseModel):
    email: EmailStr = Field(...)
    source: str = Field(...)
    message: str = Field(..., min_length=1)


class TicketResponse(BaseModel):
    id: int
    lead_email: EmailStr
    source: str
    operator_id: int | None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
