from typing import List, Tuple, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.operator import Operator
from src.models.source_operator_weight import SourceOperatorWeight


class OperatorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_for_source_with_weights(
        self,
        source_id: int,
    ) -> List[Tuple[Operator, int]]:
        
        stmt = (
            select(Operator, SourceOperatorWeight.weight)
            .join(SourceOperatorWeight, SourceOperatorWeight.operator_id == Operator.id)
            .where(SourceOperatorWeight.source_id == source_id)
        )
        result = await self.session.execute(stmt)
        rows = result.all()
        return [(row[0], row[1]) for row in rows]

    async def get_by_id(self, operator_id: int) -> Optional[Operator]:
        stmt = select(Operator).where(Operator.id == operator_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Operator]:
        stmt = select(Operator).order_by(Operator.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(
        self,
        *,
        name: str,
        max_active_tickets: int,
        is_active: bool = True,
    ) -> Operator:
        
        operator = Operator(
            name=name,
            max_active_tickets=max_active_tickets,
            is_active=is_active,
        )
        self.session.add(operator)
        await self.session.flush()
        return operator

    async def update(
        self,
        operator: Operator,
        *,
        name: str | None = None,
        max_active_tickets: int | None = None,
        is_active: bool | None = None,
    ) -> Operator:
        
        if name is not None:
            operator.name = name
        if max_active_tickets is not None:
            operator.max_active_tickets = max_active_tickets
        if is_active is not None:
            operator.is_active = is_active

        await self.session.flush()
        return operator
