from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Lead(Base):
    __tablename__ = "leads"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="lead",
        cascade="all, delete-orphan",
    )