from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.lead import Lead
from src.models.ticket import Ticket


class LeadRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> Optional[Lead]:
        stmt = select(Lead).where(Lead.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, email: str) -> Lead:
        lead = Lead(email=email)
        self.session.add(lead)
        await self.session.flush()
        return lead

    async def list_with_tickets(self) -> List[Lead]:
        stmt = (
            select(Lead)
            .options(
                selectinload(Lead.tickets).selectinload(Ticket.source),
            )
            .order_by(Lead.id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().unique().all())
