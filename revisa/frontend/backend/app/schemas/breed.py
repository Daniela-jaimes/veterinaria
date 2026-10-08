from pydantic import Field

from app.models.enums import PetSpecies
from app.schemas.common import InputModel, ORMModel, UpdateModel


class BreedCreate(InputModel):
    species: PetSpecies
    name: str = Field(min_length=1, max_length=50)


class BreedUpdate(UpdateModel):
    species: PetSpecies | None = None
    name: str | None = Field(None, min_length=1, max_length=50)


class BreedResponse(ORMModel):
    breed_id: int
    species: PetSpecies
    name: str
