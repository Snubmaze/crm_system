from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base


class TicketStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)

    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id"),
        nullable=False,
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id"),
        nullable=False,
    )
    operator_id: Mapped[int | None] = mapped_column(
        ForeignKey("operators.id"),
        nullable=True,
    )

    status: Mapped[TicketStatus] = mapped_column(
        nullable=False,
        default=TicketStatus.ACTIVE,
    )

    message: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.now(),
    )
    closed_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    lead: Mapped["Lead"] = relationship(back_populates="tickets")
    source: Mapped["Source"] = relationship(back_populates="tickets")
    operator: Mapped["Operator"] = relationship(back_populates="tickets")
