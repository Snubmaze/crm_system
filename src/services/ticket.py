import random
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.ticket import Ticket
from src.repositories import (
    LeadRepository,
    OperatorRepository,
    SourceRepository,
    TicketRepository,
)
from src.services.exceptions import AllOperatorsBusyError, SourceNotFoundError


class TicketService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.lead_repo = LeadRepository(session)
        self.source_repo = SourceRepository(session)
        self.operator_repo = OperatorRepository(session)
        self.ticket_repo = TicketRepository(session)

    async def create_ticket(
        self,
        *,
        email: str,
        source_name: str,
        message: str,
    ) -> Ticket:
        lead = await self.lead_repo.get_by_email(email)
        if lead is None:
            lead = await self.lead_repo.create(email=email)

        source = await self.source_repo.get_by_name(source_name)
        if source is None:
            raise SourceNotFoundError(source_name)

        operator_weight_pairs = await self.operator_repo.get_for_source_with_weights(
            source_id=source.id,
        )
        if not operator_weight_pairs:
            raise AllOperatorsBusyError(
                f"Для источника '{source_name}' не настроены операторы.",
            )

        operator_ids = [op.id for op, _ in operator_weight_pairs]
        active_counts = await self.ticket_repo.get_active_counts_for_operators(
            operator_ids,
        )

        available: list[tuple[int, int]] = []
        for op, weight in operator_weight_pairs:
            if not op.is_active:
                continue
            current = active_counts.get(op.id, 0)
            if current >= op.max_active_tickets:
                continue
            available.append((op.id, weight))

        if not available:
            raise AllOperatorsBusyError()

        operator_id = self._choose_operator_by_weight(available)

        ticket = await self.ticket_repo.create(
            lead_id=lead.id,
            source_id=source.id,
            operator_id=operator_id,
            message=message,
        )

        await self.session.commit()

        stmt = (
            select(Ticket)
            .options(
                selectinload(Ticket.lead),
                selectinload(Ticket.source),
            )
            .where(Ticket.id == ticket.id)
        )
        result = await self.session.execute(stmt)
        ticket_full = result.scalar_one()

        return ticket_full

    @staticmethod
    def _choose_operator_by_weight(
        operator_weight_pairs: list[tuple[int, int]],
    ) -> int:
        operator_ids = [op_id for op_id, _ in operator_weight_pairs]
        weights = [w for _, w in operator_weight_pairs]
        return random.choices(operator_ids, weights=weights, k=1)[0]
