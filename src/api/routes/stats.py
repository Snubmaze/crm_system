from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.repositories import TicketRepository

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get(
    "/distribution",
    summary="Распределение обращений по операторам и источникам",
)
async def distribution(
    db: AsyncSession = Depends(get_db),
):
    repo = TicketRepository(db)
    rows = await repo.get_distribution_by_operator_and_source()

    return [
        {
            "operator_name": operator_name,
            "source_name": source_name,
            "tickets_count": tickets_count,
        }
        for operator_name, source_name, tickets_count in rows
    ]
