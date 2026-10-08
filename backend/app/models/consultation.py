from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, pg_enum
from app.models.enums import (
    ConsultationType,
)

if TYPE_CHECKING:
    from app.models.treatment import Treatment
    from app.models.vaccination import Vaccination
    from app.models.veterinarian import Veterinarian


class Consultation(Base):
    __tablename__ = "consultation"
    __table_args__ = (
        CheckConstraint("weight_kg IS NULL OR weight_kg > 0", name="chk_consultation_weight"),
        CheckConstraint("temperature_c IS NULL OR temperature_c > 0", name="chk_consultation_temperature"),
        CheckConstraint("heart_rate IS NULL OR heart_rate >= 0", name="chk_consultation_heart_rate"),
        CheckConstraint(
            "respiratory_rate IS NULL OR respiratory_rate >= 0", name="chk_consultation_respiratory_rate"
        ),
        Index("idx_consultation_medical_record", "medical_record_id"),
        Index("idx_consultation_vet", "vet_id"),
    )

    consultation_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    medical_record_id: Mapped[int] = mapped_column(
        ForeignKey("medical_record.medical_record_id", ondelete="RESTRICT"), nullable=False
    )
    appointment_id: Mapped[int | None] = mapped_column(
        ForeignKey("appointment.appointment_id", ondelete="RESTRICT"), unique=True
    )
    vet_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarian.vet_id", ondelete="RESTRICT"), nullable=False
    )
    consultation_type: Mapped[ConsultationType] = mapped_column(
        pg_enum(ConsultationType, "consultation_type"),
        nullable=False,
        server_default=text("'checkup'"),
    )
    consultation_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    temperature_c: Mapped[Decimal | None] = mapped_column(Numeric(4, 1))
    heart_rate: Mapped[int | None] = mapped_column(Integer)
    respiratory_rate: Mapped[int | None] = mapped_column(Integer)
    mucosal_state: Mapped[str | None] = mapped_column(String(50))
    anamnesis: Mapped[str | None] = mapped_column(Text)
    diagnosis: Mapped[str | None] = mapped_column(Text)
    prognosis: Mapped[str | None] = mapped_column(String(50))
    treatment_plan: Mapped[str | None] = mapped_column(Text)
    next_checkup: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)

    vet: Mapped["Veterinarian"] = relationship(lazy="raise")
    treatments: Mapped[list["Treatment"]] = relationship(lazy="raise", order_by="Treatment.treatment_id")
    vaccinations: Mapped[list["Vaccination"]] = relationship(
        lazy="raise", order_by="Vaccination.vaccination_id"
    )
