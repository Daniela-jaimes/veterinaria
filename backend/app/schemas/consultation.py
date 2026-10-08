from datetime import date
from decimal import Decimal
from typing import ClassVar

from pydantic import Field

from app.models.enums import ConsultationType
from app.schemas.common import IdInt, InputModel, NaiveDatetime, ORMModel, UpdateModel
from app.schemas.treatment import TreatmentResponse
from app.schemas.vaccination import VaccinationResponse
from app.schemas.veterinarian import VeterinarianBrief

_CLINICAL_NULLABLE = frozenset({
    "weight_kg", "temperature_c", "heart_rate", "respiratory_rate", "mucosal_state",
    "anamnesis", "diagnosis", "prognosis", "treatment_plan", "next_checkup", "notes",
})


class ConsultationCreate(InputModel):
    medical_record_id: IdInt
    vet_id: IdInt
    appointment_id: IdInt | None = None
    consultation_type: ConsultationType = ConsultationType.checkup
    consultation_date: NaiveDatetime | None = None  # si no se envía, la BD usa CURRENT_TIMESTAMP

    weight_kg: Decimal | None = Field(None, gt=0, max_digits=5, decimal_places=2)
    temperature_c: Decimal | None = Field(None, gt=0, max_digits=4, decimal_places=1)
    heart_rate: int | None = Field(None, ge=0)
    respiratory_rate: int | None = Field(None, ge=0)
    mucosal_state: str | None = Field(None, max_length=50)

    anamnesis: str | None = None
    diagnosis: str | None = None
    prognosis: str | None = Field(None, max_length=50)
    treatment_plan: str | None = None
    next_checkup: date | None = None
    notes: str | None = None


class ConsultationUpdate(UpdateModel):
    """medical_record_id y appointment_id son inmutables una vez creada la consulta."""
    nullable_fields: ClassVar[frozenset[str]] = _CLINICAL_NULLABLE
    vet_id: IdInt | None = None
    consultation_type: ConsultationType | None = None
    consultation_date: NaiveDatetime | None = None

    weight_kg: Decimal | None = Field(None, gt=0, max_digits=5, decimal_places=2)
    temperature_c: Decimal | None = Field(None, gt=0, max_digits=4, decimal_places=1)
    heart_rate: int | None = Field(None, ge=0)
    respiratory_rate: int | None = Field(None, ge=0)
    mucosal_state: str | None = Field(None, max_length=50)

    anamnesis: str | None = None
    diagnosis: str | None = None
    prognosis: str | None = Field(None, max_length=50)
    treatment_plan: str | None = None
    next_checkup: date | None = None
    notes: str | None = None


class ConsultationResponse(ORMModel):
    consultation_id: int
    medical_record_id: int
    appointment_id: int | None
    vet_id: int
    consultation_type: ConsultationType
    consultation_date: NaiveDatetime
    weight_kg: Decimal | None
    temperature_c: Decimal | None
    heart_rate: int | None
    respiratory_rate: int | None
    mucosal_state: str | None
    anamnesis: str | None
    diagnosis: str | None
    prognosis: str | None
    treatment_plan: str | None
    next_checkup: date | None
    notes: str | None
    vet: VeterinarianBrief
    treatments: list[TreatmentResponse]
    vaccinations: list[VaccinationResponse]
