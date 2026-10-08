from datetime import date
from typing import Annotated, ClassVar

from pydantic import AfterValidator

from app.schemas.common import IdInt, InputModel, ORMModel, UpdateModel
from app.schemas.pet import PetBrief


def _not_future(value: date) -> date:
    if value > date.today():
        raise ValueError("opened_on no puede ser una fecha futura")
    return value


OpenedOn = Annotated[date, AfterValidator(_not_future)]


class MedicalRecordCreate(InputModel):
    pet_id: IdInt
    opened_on: OpenedOn | None = None  # si no se envía, la BD usa CURRENT_DATE
    general_notes: str | None = None



class MedicalRecordUpdate(UpdateModel):
    """El pet_id no se puede cambiar: la historia clínica pertenece a una única mascota."""
    nullable_fields: ClassVar[frozenset[str]] = frozenset({"general_notes"})
    opened_on: OpenedOn | None = None
    general_notes: str | None = None


class MedicalRecordResponse(ORMModel):
    medical_record_id: int
    pet_id: int
    opened_on: date
    general_notes: str | None
    pet: PetBrief
