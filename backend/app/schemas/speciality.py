from pydantic import Field

from app.schemas.common import InputModel, ORMModel, UpdateModel


class SpecialityCreate(InputModel):
    name: str = Field(min_length=1, max_length=100)


class SpecialityUpdate(UpdateModel):
    name: str | None = Field(None, min_length=1, max_length=100)


class SpecialityResponse(ORMModel):
    speciality_id: int
    name: str
