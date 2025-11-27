import random
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

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

        available_operators: list[tuple[int, int]] = []

        for operator, weight in operator_weight_pairs:
            if not operator.is_active:
                continue

            current_load = active_counts.get(operator.id, 0)
            if current_load >= operator.max_active_tickets:
                continue

            available_operators.append((operator.id, weight))

        if not available_operators:
            raise AllOperatorsBusyError()

        operator_id = self._choose_operator_by_weight(available_operators)

        ticket = await self.ticket_repo.create(
            lead_id=lead.id,
            source_id=source.id,
            operator_id=operator_id,
            message=message,
        )

        await self.session.commit()
        await self.session.refresh(ticket)

        return ticket


    @staticmethod
    def _choose_operator_by_weight(
        operator_weight_pairs: list[tuple[int, int]],
    ) -> int:
 
        operator_ids = [op_id for op_id, _ in operator_weight_pairs]
        weights = [weight for _, weight in operator_weight_pairs]

        chosen_id: int = random.choices(operator_ids, weights=weights, k=1)[0]
        return chosen_id
