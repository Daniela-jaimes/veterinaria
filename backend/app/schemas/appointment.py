from typing import ClassVar

from pydantic import Field

from app.models.enums import AppointmentStatus
from app.schemas.common import IdInt, InputModel, NaiveDatetime, ORMModel, UpdateModel
from app.schemas.pet import PetBrief
from app.schemas.veterinarian import VeterinarianBrief


class AppointmentCreate(InputModel):
    """Toda cita nace en estado 'scheduled'."""
    pet_id: IdInt
    vet_id: IdInt
    scheduled_at: NaiveDatetime
    duration_minutes: int = Field(30, gt=0, le=1440)
    reason: str | None = Field(None, max_length=255)
    notes: str | None = None


class AppointmentUpdate(UpdateModel):
    nullable_fields: ClassVar[frozenset[str]] = frozenset({"reason", "notes"})
    pet_id: IdInt | None = None
    vet_id: IdInt | None = None
    scheduled_at: NaiveDatetime | None = None
    duration_minutes: int | None = Field(None, gt=0, le=1440)
    reason: str | None = Field(None, max_length=255)
    status: AppointmentStatus | None = None
    notes: str | None = None


class AppointmentResponse(ORMModel):
    appointment_id: int
    pet_id: int
    vet_id: int
    scheduled_at: NaiveDatetime
    duration_minutes: int
    reason: str | None
    status: AppointmentStatus
    notes: str | None
    pet: PetBrief
    vet: VeterinarianBrief
