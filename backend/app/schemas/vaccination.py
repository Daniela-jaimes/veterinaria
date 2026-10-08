from datetime import date
from typing import ClassVar

from pydantic import Field, model_validator

from app.schemas.common import IdInt, InputModel, ORMModel, UpdateModel
from app.schemas.vaccine import VaccineResponse


class VaccinationCreate(InputModel):
    consultation_id: IdInt
    vaccine_id: IdInt
    batch_number: str | None = Field(None, max_length=100)
    date_given: date
    next_due_date: date | None = None
    notes: str | None = None

    @model_validator(mode="after")
    def _check_dates(self):
        if self.next_due_date is not None and self.next_due_date < self.date_given:
            raise ValueError("next_due_date no puede ser anterior a date_given")
        return self


class VaccinationUpdate(UpdateModel):
    nullable_fields: ClassVar[frozenset[str]] = frozenset({"batch_number", "next_due_date", "notes"})
    vaccine_id: IdInt | None = None
    batch_number: str | None = Field(None, max_length=100)
    date_given: date | None = None
    next_due_date: date | None = None
    notes: str | None = None


class VaccinationResponse(ORMModel):
    vaccination_id: int
    consultation_id: int
    vaccine_id: int
    batch_number: str | None
    date_given: date
    next_due_date: date | None
    notes: str | None
    vaccine: VaccineResponse
