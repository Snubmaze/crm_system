from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="source",
    )

    operator_weights: Mapped[list["SourceOperatorWeight"]] = relationship(
        back_populates="source",
        cascade="all, delete-orphan",
    )