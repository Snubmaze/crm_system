from typing import List, Tuple
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
        """
        Возвращает список (оператор, weight) для заданного source_id.
        """
        stmt = (
            select(Operator, SourceOperatorWeight.weight)
            .join(SourceOperatorWeight, SourceOperatorWeight.operator_id == Operator.id)
            .where(SourceOperatorWeight.source_id == source_id)
        )

        result = await self.session.execute(stmt)
        rows = result.all()

        return [(row[0], row[1]) for row in rows]

    async def get_by_id(self, operator_id: int) -> Operator | None:
        stmt = select(Operator).where(Operator.id == operator_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
