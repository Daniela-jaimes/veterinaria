from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
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
    AppointmentStatus,
)

if TYPE_CHECKING:
    from app.models.pet import Pet
    from app.models.veterinarian import Veterinarian


class Appointment(Base):
    __tablename__ = "appointment"
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="chk_appointment_duration"),
        Index("idx_appointment_pet", "pet_id"),
        Index("idx_appointment_vet_date", "vet_id", "scheduled_at"),
    )

    appointment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pet.pet_id", ondelete="RESTRICT"), nullable=False)
    vet_id: Mapped[int] = mapped_column(
        ForeignKey("veterinarian.vet_id", ondelete="RESTRICT"), nullable=False
    )
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("30"))
    reason: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[AppointmentStatus] = mapped_column(
        pg_enum(AppointmentStatus, "appointment_status"),
        nullable=False,
        server_default=text("'scheduled'"),
    )
    notes: Mapped[str | None] = mapped_column(Text)

    pet: Mapped["Pet"] = relationship(lazy="raise")
    vet: Mapped["Veterinarian"] = relationship(lazy="raise")
