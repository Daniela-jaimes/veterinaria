from typing import ClassVar

from pydantic import Field

from app.schemas.common import InputModel, ORMModel, UpdateModel


class MedicationCreate(InputModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None


class MedicationUpdate(UpdateModel):
    nullable_fields: ClassVar[frozenset[str]] = frozenset({"description"})
    name: str | None = Field(None, min_length=1, max_length=150)
    description: str | None = None


class MedicationResponse(ORMModel):
    medication_id: int
    name: str
    description: str | None


class MedicationBrief(ORMModel):
    medication_id: int
    name: str

