from pydantic import BaseModel, Field


class OperatorCreate(BaseModel):
    name: str = Field(..., min_length=1)
    max_active_tickets: int = Field(..., ge=0)
    is_active: bool = True


class OperatorUpdate(BaseModel):
    name: str | None = Field(None, min_length=1)
    max_active_tickets: int | None = Field(None, ge=0)
    is_active: bool | None = None


class OperatorResponse(BaseModel):
    id: int
    name: str
    max_active_tickets: int
    is_active: bool

    class Config:
        from_attributes = True
