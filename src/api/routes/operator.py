from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.repositories import OperatorRepository
from src.api.schemas.operator import (
    OperatorCreate,
    OperatorUpdate,
    OperatorResponse,
)

router = APIRouter(prefix="/operators", tags=["operators"])


@router.post(
    "",
    response_model=OperatorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_operator(
    payload: OperatorCreate,
    db: AsyncSession = Depends(get_db),
):
    repo = OperatorRepository(db)

    operator = await repo.create(
        name=payload.name,
        max_active_tickets=payload.max_active_tickets,
        is_active=payload.is_active,
    )

    await db.commit()
    await db.refresh(operator)
    return operator


@router.get("", response_model=list[OperatorResponse])
async def list_operators(
    db: AsyncSession = Depends(get_db),
):
    repo = OperatorRepository(db)
    operators = await repo.list_all()
    return operators


@router.patch("/{operator_id}", response_model=OperatorResponse)
async def update_operator(
    operator_id: int,
    payload: OperatorUpdate,
    db: AsyncSession = Depends(get_db),
):
    repo = OperatorRepository(db)

    operator = await repo.get_by_id(operator_id)
    if operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")

    updated = await repo.update(
        operator,
        name=payload.name,
        max_active_tickets=payload.max_active_tickets,
        is_active=payload.is_active,
    )

    await db.commit()
    await db.refresh(updated)
    return updated
