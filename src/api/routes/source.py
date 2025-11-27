from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.repositories import SourceRepository, OperatorRepository
from src.api.schemas.source import (
    SourceCreate,
    SourceResponse,
    SourceOperatorWeightsUpdate,
)

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post(
    "",
    response_model=SourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_source(
    payload: SourceCreate,
    db: AsyncSession = Depends(get_db),
):
    repo = SourceRepository(db)

    existing = await repo.get_by_name(payload.name)
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Source '{payload.name}' already exists",
        )

    source = await repo.create(name=payload.name)

    await db.commit()
    await db.refresh(source)
    return source


@router.get("", response_model=list[SourceResponse])
async def list_sources(db: AsyncSession = Depends(get_db)):
    repo = SourceRepository(db)
    return await repo.list_all()


@router.put(
    "/{source_id}/operators",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def set_source_operators(
    source_id: int,
    payload: SourceOperatorWeightsUpdate,
    db: AsyncSession = Depends(get_db),
):
    source_repo = SourceRepository(db)
    operator_repo = OperatorRepository(db)

    source = await source_repo.get_by_id(source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")

    operator_ids = [item.operator_id for item in payload.operators]

    for operator_id in operator_ids:
        operator = await operator_repo.get_by_id(operator_id)
        if operator is None:
            raise HTTPException(
                status_code=400,
                detail=f"Operator {operator_id} not found",
            )

    operators_weights = [(item.operator_id, item.weight) for item in payload.operators]

    await source_repo.set_operator_weights(source, operators_weights)
    await db.commit()
