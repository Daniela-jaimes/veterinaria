from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.vaccine import Vaccine


class Vaccination(Base):
    __tablename__ = "vaccination"
    __table_args__ = (
        CheckConstraint("next_due_date IS NULL OR next_due_date >= date_given", name="chk_vaccination_dates"),
        Index("idx_vaccination_consultation", "consultation_id"),
        Index("idx_vaccination_vaccine", "vaccine_id"),
    )

    vaccination_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consultation_id: Mapped[int] = mapped_column(
        ForeignKey("consultation.consultation_id", ondelete="RESTRICT"), nullable=False
    )
    vaccine_id: Mapped[int] = mapped_column(
        ForeignKey("vaccine.vaccine_id", ondelete="RESTRICT"), nullable=False
    )
    batch_number: Mapped[str | None] = mapped_column(String(100))
    date_given: Mapped[date] = mapped_column(Date, nullable=False)
    next_due_date: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)

    vaccine: Mapped["Vaccine"] = relationship(lazy="raise")
