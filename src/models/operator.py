from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Operator(Base):
    __tablename__ = "operators"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    max_active_tickets: Mapped[int] = mapped_column(nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="operator",
    )

    source_weights: Mapped[list["SourceOperatorWeight"]] = relationship(
        back_populates="operator",
        cascade="all, delete-orphan",
    )