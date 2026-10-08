from datetime import date
from typing import Annotated, ClassVar

from pydantic import AfterValidator, Field

from app.models.enums import PetSex
from app.schemas.common import IdInt, InputModel, ORMModel, UpdateModel


def _not_future(value: date) -> date:
    if value > date.today():
        raise ValueError("birth_date no puede ser una fecha futura")
    return value


BirthDate = Annotated[date, AfterValidator(_not_future)]


class PetCreate(InputModel):
    customer_id: IdInt
    breed_id: IdInt
    name: str = Field(min_length=1, max_length=50)
    birth_date: BirthDate | None = None
    sex: PetSex = PetSex.unknown
    microchip_number: str | None = Field(None, min_length=1, max_length=20)
    is_neutered: bool = False


class PetUpdate(UpdateModel):
    nullable_fields: ClassVar[frozenset[str]] = frozenset({"birth_date", "microchip_number"})
    customer_id: IdInt | None = None
    breed_id: IdInt | None = None
    name: str | None = Field(None, min_length=1, max_length=50)
    birth_date: BirthDate | None = None
    sex: PetSex | None = None
    microchip_number: str | None = Field(None, min_length=1, max_length=20)
    is_neutered: bool | None = None
    is_active: bool | None = None


class PetBrief(ORMModel):
    pet_id: int
    name: str
    customer_id: int


class PetResponse(ORMModel):
    pet_id: int
    customer_id: int
    breed_id: int
    name: str
    birth_date: date | None
    sex: PetSex
    microchip_number: str | None
    is_neutered: bool
    is_active: bool
