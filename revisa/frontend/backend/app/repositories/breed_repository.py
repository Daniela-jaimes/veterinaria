from sqlalchemy import func

from app.models.enums import PetSpecies
from app.models import Breed
from app.repositories.base import BaseRepository


class BreedRepository(BaseRepository[Breed]):
    model = Breed
    pk_name = "breed_id"

    async def search(self, *, species: PetSpecies | None, name: str | None, limit: int, offset: int):
        where = []
        if species:
            where.append(Breed.species == species)
        if name:
            where.append(Breed.name.ilike(f"%{name}%"))
        return await self.get_page(where=where, order_by=[Breed.species, Breed.name], limit=limit, offset=offset)

    async def get_duplicate(self, species: PetSpecies, name: str, exclude_id: int | None = None) -> Breed | None:
        conds = [Breed.species == species, func.lower(Breed.name) == name.lower()]
        if exclude_id is not None:
            conds.append(Breed.breed_id != exclude_id)
        return await self.first(*conds)
