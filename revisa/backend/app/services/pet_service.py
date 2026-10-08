from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError
from app.models import Pet
from app.repositories.breed_repository import BreedRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.pet_repository import PetRepository
from app.schemas.pet import PetCreate, PetUpdate
from app.services.base import BaseService


class PetService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = PetRepository(session)
        self.customers = CustomerRepository(session)
        self.breeds = BreedRepository(session)

    async def _check_owner(self, customer_id: int) -> None:
        customer = await self._get_or_404(self.customers, customer_id, "Cliente")
        if not customer.is_active:
            raise BadRequestError("El cliente está inactivo")

    async def _check_microchip(self, microchip: str | None, exclude_id: int | None = None) -> None:
        if microchip and await self.repo.get_by_microchip(microchip, exclude_id):
            raise ConflictError("El número de microchip ya está registrado")

    async def create(self, payload: PetCreate) -> Pet:
        await self._check_owner(payload.customer_id)
        await self._get_or_404(self.breeds, payload.breed_id, "Raza")
        await self._check_microchip(payload.microchip_number)
        async with self._guard("No se pudo crear la mascota (microchip duplicado)"):
            obj = await self.repo.add(Pet(**payload.model_dump(exclude_none=True)))
            await self.session.commit()
        return await self.get(obj.pet_id)

    async def list(self, *, customer_id, breed_id, is_active, search, limit: int, offset: int):
        return await self.repo.search(
            customer_id=customer_id, breed_id=breed_id, is_active=is_active, search=search,
            limit=limit, offset=offset,
        )

    async def get(self, pet_id: int) -> Pet:
        return await self._get_or_404(self.repo, pet_id, "Mascota")

    async def update(self, pet_id: int, payload: PetUpdate) -> Pet:
        obj = await self._get_or_404(self.repo, pet_id, "Mascota")
        changes = payload.changes()
        if "customer_id" in changes:
            await self._check_owner(changes["customer_id"])
        if "breed_id" in changes:
            await self._get_or_404(self.breeds, changes["breed_id"], "Raza")
        await self._check_microchip(changes.get("microchip_number"), exclude_id=pet_id)
        async with self._guard("No se pudo actualizar la mascota (microchip duplicado)"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return await self.get(pet_id)

    async def delete(self, pet_id: int) -> None:
        """Borrado lógico (idempotente)."""
        obj = await self._get_or_404(self.repo, pet_id, "Mascota")
        if obj.is_active:
            await self.repo.update(obj, {"is_active": False})
            await self.session.commit()
