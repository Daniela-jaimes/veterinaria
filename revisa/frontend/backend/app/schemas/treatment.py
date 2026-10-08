from datetime import date
from typing import ClassVar

from pydantic import Field, model_validator

from app.models.enums import TreatmentStatus
from app.schemas.common import IdInt, InputModel, ORMModel, UpdateModel
from app.schemas.medication import MedicationBrief


class TreatmentCreate(InputModel):
    """Todo tratamiento nace en estado 'active'."""
    consultation_id: IdInt
    medication_id: IdInt
    dosage: str | None = Field(None, max_length=50)
    frequency: str | None = Field(None, max_length=50)
    start_date: date
    end_date: date | None = None
    instructions: str | None = None

    @model_validator(mode="after")
    def _check_dates(self):
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date no puede ser anterior a start_date")
        return self


class TreatmentUpdate(UpdateModel):
    nullable_fields: ClassVar[frozenset[str]] = frozenset({"dosage", "frequency", "end_date", "instructions"})
    medication_id: IdInt | None = None
    dosage: str | None = Field(None, max_length=50)
    frequency: str | None = Field(None, max_length=50)
    start_date: date | None = None
    end_date: date | None = None
    instructions: str | None = None
    status: TreatmentStatus | None = None


class TreatmentResponse(ORMModel):
    treatment_id: int
    consultation_id: int
    medication_id: int
    dosage: str | None
    frequency: str | None
    start_date: date
    end_date: date | None
    instructions: str | None
    status: TreatmentStatus
    medication: MedicationBrief
