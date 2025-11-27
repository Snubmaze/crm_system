from pydantic import BaseModel, Field


class SourceCreate(BaseModel):
    name: str = Field(..., min_length=1)


class SourceResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SourceOperatorWeightItem(BaseModel):
    operator_id: int
    weight: int = Field(..., ge=0)


class SourceOperatorWeightsUpdate(BaseModel):
    operators: list[SourceOperatorWeightItem]
