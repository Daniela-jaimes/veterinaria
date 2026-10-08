from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    ForeignKey,
    Integer,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.pet import Pet


class MedicalRecord(Base):
    __tablename__ = "medical_record"

    medical_record_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(
        ForeignKey("pet.pet_id", ondelete="RESTRICT"), nullable=False, unique=True
    )
    opened_on: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    general_notes: Mapped[str | None] = mapped_column(Text)

    pet: Mapped["Pet"] = relationship(lazy="raise")
