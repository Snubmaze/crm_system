from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.repositories import LeadRepository
from src.api.schemas.lead import LeadResponse, LeadTicketShort

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("", response_model=list[LeadResponse])
async def list_leads_with_tickets(
    db: AsyncSession = Depends(get_db),
):
    repo = LeadRepository(db)
    leads = await repo.list_with_tickets()

    result: list[LeadResponse] = []

    for lead in leads:
        tickets_short: list[LeadTicketShort] = []

        for t in lead.tickets:
            tickets_short.append(
                LeadTicketShort(
                    id=t.id,
                    source_name=t.source.name,
                    operator_id=t.operator_id,
                    status=t.status.value,
                    created_at=t.created_at,
                )
            )

        result.append(
            LeadResponse(
                id=lead.id,
                email=lead.email,
                tickets=tickets_short,
            )
        )

    return result
