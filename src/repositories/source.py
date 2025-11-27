from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.source import Source
from src.models.source_operator_weight import SourceOperatorWeight


class SourceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_name(self, name: str) -> Optional[Source]:
        stmt = select(Source).where(Source.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, source_id: int) -> Optional[Source]:
        stmt = select(Source).where(Source.id == source_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Source]:
        stmt = select(Source).order_by(Source.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, *, name: str) -> Source:
        source = Source(name=name)
        self.session.add(source)
        await self.session.flush()
        return source

    async def set_operator_weights(
        self,
        source: Source,
        operators_weights: list[tuple[int, int]],
    ) -> None:
        await self.session.execute(
            delete(SourceOperatorWeight).where(
                SourceOperatorWeight.source_id == source.id,
            )
        )

        for operator_id, weight in operators_weights:
            sow = SourceOperatorWeight(
                source_id=source.id,
                operator_id=operator_id,
                weight=weight,
            )
            self.session.add(sow)

        await self.session.flush()
