from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class SourceOperatorWeight(Base):
    __tablename__ = "source_operator_weights"
    __table_args__ = (
        UniqueConstraint("source_id", "operator_id", name="uq_source_operator"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id", ondelete="CASCADE"),
        nullable=False,
    )
    operator_id: Mapped[int] = mapped_column(
        ForeignKey("operators.id", ondelete="CASCADE"),
        nullable=False,
    )

    weight: Mapped[int] = mapped_column(Integer, nullable=False)

    source: Mapped["Source"] = relationship(back_populates="operator_weights")
    operator: Mapped["Operator"] = relationship(back_populates="source_weights")
