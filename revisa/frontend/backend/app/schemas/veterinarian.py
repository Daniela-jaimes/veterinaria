from typing import ClassVar

from pydantic import Field

from app.schemas.common import Email150, IdInt, InputModel, ORMModel, UpdateModel
from app.schemas.speciality import SpecialityResponse


class VeterinarianCreate(InputModel):
    speciality_id: IdInt
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    license_number: str = Field(min_length=1, max_length=50)
    phone: str | None = Field(None, max_length=20)
    email: Email150 | None = None


class VeterinarianUpdate(UpdateModel):
    nullable_fields: ClassVar[frozenset[str]] = frozenset({"phone", "email"})
    speciality_id: IdInt | None = None
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
    license_number: str | None = Field(None, min_length=1, max_length=50)
    phone: str | None = Field(None, max_length=20)
    email: Email150 | None = None
    is_active: bool | None = None


class VeterinarianBrief(ORMModel):
    vet_id: int
    first_name: str
    last_name: str


class VeterinarianResponse(ORMModel):
    vet_id: int
    speciality_id: int
    first_name: str
    last_name: str
    license_number: str
    phone: str | None
    email: str | None
    is_active: bool
    speciality: SpecialityResponse
