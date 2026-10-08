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
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, pg_enum
from app.models.enums import (
    TreatmentStatus,
)

if TYPE_CHECKING:
    from app.models.medication import Medication


class Treatment(Base):
    __tablename__ = "treatment"
    __table_args__ = (
        CheckConstraint("end_date IS NULL OR end_date >= start_date", name="chk_treatment_dates"),
        Index("idx_treatment_consultation", "consultation_id"),
        Index("idx_treatment_medication", "medication_id"),
    )

    treatment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    consultation_id: Mapped[int] = mapped_column(
        ForeignKey("consultation.consultation_id", ondelete="RESTRICT"), nullable=False
    )
    medication_id: Mapped[int] = mapped_column(
        ForeignKey("medication.medication_id", ondelete="RESTRICT"), nullable=False
    )
    dosage: Mapped[str | None] = mapped_column(String(50))
    frequency: Mapped[str | None] = mapped_column(String(50))
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    instructions: Mapped[str | None] = mapped_column(Text)
    status: Mapped[TreatmentStatus] = mapped_column(
        pg_enum(TreatmentStatus, "treatment_status"),
        nullable=False,
        server_default=text("'active'"),
    )

    medication: Mapped["Medication"] = relationship(lazy="raise")
