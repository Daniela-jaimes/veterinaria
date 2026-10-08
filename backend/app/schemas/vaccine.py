from typing import ClassVar

from pydantic import Field

from app.schemas.common import InputModel, ORMModel, UpdateModel


class VaccineCreate(InputModel):
    name: str = Field(min_length=1, max_length=100)
    manufacturer: str | None = Field(None, max_length=100)


class VaccineUpdate(UpdateModel):
    nullable_fields: ClassVar[frozenset[str]] = frozenset({"manufacturer"})
    name: str | None = Field(None, min_length=1, max_length=100)
    manufacturer: str | None = Field(None, max_length=100)


class VaccineResponse(ORMModel):
    vaccine_id: int
    name: str
    manufacturer: str | None
