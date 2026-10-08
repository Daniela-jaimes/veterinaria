from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError
from app.models import PetAllergy
from app.repositories.pet_allergy_repository import PetAllergyRepository
from app.repositories.pet_repository import PetRepository
from app.schemas.pet_allergy import PetAllergyCreate, PetAllergyUpdate
from app.services.base import BaseService


class PetAllergyService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = PetAllergyRepository(session)
        self.pets = PetRepository(session)

    async def create(self, payload: PetAllergyCreate) -> PetAllergy:
        pet = await self._get_or_404(self.pets, payload.pet_id, "Mascota")
        if not pet.is_active:
            raise BadRequestError("La mascota está inactiva")
        if await self.repo.get_duplicate(payload.pet_id, payload.description):
            raise ConflictError("La mascota ya tiene registrada esa alergia")
        async with self._guard("No se pudo crear la alergia"):
            obj = await self.repo.add(PetAllergy(**payload.model_dump()))
            await self.session.commit()
        return await self.get(obj.allergy_id)

    async def list(self, *, pet_id: int | None, search: str | None, limit: int, offset: int):
        return await self.repo.search(pet_id=pet_id, search=search, limit=limit, offset=offset)

    async def get(self, allergy_id: int) -> PetAllergy:
        return await self._get_or_404(self.repo, allergy_id, "Alergia")

    async def update(self, allergy_id: int, payload: PetAllergyUpdate) -> PetAllergy:
        obj = await self._get_or_404(self.repo, allergy_id, "Alergia")
        changes = payload.changes()
        if "description" in changes and await self.repo.get_duplicate(
            obj.pet_id, changes["description"], exclude_id=allergy_id
        ):
            raise ConflictError("La mascota ya tiene registrada esa alergia")
        async with self._guard("No se pudo actualizar la alergia"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return await self.get(allergy_id)

    async def delete(self, allergy_id: int) -> None:
        await self._hard_delete(self.repo, allergy_id, "Alergia", "No se pudo eliminar la alergia")
