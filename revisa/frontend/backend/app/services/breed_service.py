from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.models.enums import PetSpecies
from app.models import Breed
from app.repositories.breed_repository import BreedRepository
from app.schemas.breed import BreedCreate, BreedUpdate
from app.services.base import BaseService


class BreedService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = BreedRepository(session)

    async def create(self, payload: BreedCreate) -> Breed:
        if await self.repo.get_duplicate(payload.species, payload.name):
            raise ConflictError(f"La raza '{payload.name}' ya existe para la especie '{payload.species.value}'")
        async with self._guard("No se pudo crear la raza (registro duplicado)"):
            obj = await self.repo.add(Breed(**payload.model_dump()))
            await self.session.commit()
        return obj

    async def list(self, *, species: PetSpecies | None, name: str | None, limit: int, offset: int):
        return await self.repo.search(species=species, name=name, limit=limit, offset=offset)

    async def get(self, breed_id: int) -> Breed:
        return await self._get_or_404(self.repo, breed_id, "Raza")

    async def update(self, breed_id: int, payload: BreedUpdate) -> Breed:
        obj = await self.get(breed_id)
        changes = payload.changes()
        species = changes.get("species", obj.species)
        name = changes.get("name", obj.name)
        if await self.repo.get_duplicate(species, name, exclude_id=breed_id):
            raise ConflictError(f"La raza '{name}' ya existe para la especie '{species.value}'")
        async with self._guard("No se pudo actualizar la raza (registro duplicado)"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return obj

    async def delete(self, breed_id: int) -> None:
        await self._hard_delete(
            self.repo, breed_id, "Raza", "No se puede eliminar: hay mascotas asociadas a esta raza"
        )
