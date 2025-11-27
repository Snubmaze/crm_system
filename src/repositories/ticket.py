from typing import Dict, Iterable, Optional, List, Tuple
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ticket import Ticket, TicketStatus
from src.models.operator import Operator
from src.models.source import Source


class TicketRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        lead_id: int,
        source_id: int,
        operator_id: Optional[int],
        message: str,
    ) -> Ticket:
        
        ticket = Ticket(
            lead_id=lead_id,
            source_id=source_id,
            operator_id=operator_id,
            message=message,
            status=TicketStatus.ACTIVE,
        )
        self.session.add(ticket)
        await self.session.flush()
        return ticket

    async def get_active_counts_for_operators(
        self,
        operator_ids: Iterable[int],
    ) -> Dict[int, int]:
        """
        Возвращает словарь: {operator_id: count_active_tickets}
        """
        operator_ids = list(operator_ids)
        if not operator_ids:
            return {}

        stmt: Select = (
            select(Ticket.operator_id, func.count(Ticket.id))
            .where(
                Ticket.operator_id.in_(operator_ids),
                Ticket.status == TicketStatus.ACTIVE,
            )
            .group_by(Ticket.operator_id)
        )

        result = await self.session.execute(stmt)
        rows = result.all()

        return {operator_id: count for operator_id, count in rows}

    async def get_distribution_by_operator_and_source(
        self,
    ) -> List[Tuple[str, str, int]]:
        """
        Возвращает список кортежей: (operator_name, source_name, tickets_count)
        """
        stmt: Select = (
            select(Operator.name, Source.name, func.count(Ticket.id))
            .join(Operator, Ticket.operator_id == Operator.id)
            .join(Source, Ticket.source_id == Source.id)
            .group_by(Operator.name, Source.name)
            .order_by(Operator.name, Source.name)
        )

        result = await self.session.execute(stmt)
        return list(result.all())

