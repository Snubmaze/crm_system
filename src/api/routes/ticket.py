from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.ticket import TicketCreate, TicketResponse
from src.services import AllOperatorsBusyError, SourceNotFoundError, TicketService
from src.core.db import get_db

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    payload: TicketCreate,
    db: AsyncSession = Depends(get_db),
):
    service = TicketService(db)

    try:
        ticket = await service.create_ticket(
            email=payload.email,
            source_name=payload.source,
            message=payload.message,
        )
    except SourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except AllOperatorsBusyError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    return TicketResponse(
        id=ticket.id,
        lead_email=ticket.lead.email,
        source=ticket.source.name,
        operator_id=ticket.operator_id,
        status=ticket.status.value,
        created_at=ticket.created_at,
    )
