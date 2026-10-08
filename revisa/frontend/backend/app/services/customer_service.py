from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.models import Customer, Pet
from app.repositories.customer_repository import CustomerRepository
from app.repositories.pet_repository import PetRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.base import BaseService


class CustomerService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = CustomerRepository(session)
        self.pets = PetRepository(session)

    async def _check_email(self, email: str | None, exclude_id: int | None = None) -> None:
        if email and await self.repo.get_by_email(email, exclude_id):
            raise ConflictError("El correo electrónico ya está registrado")

    async def create(self, payload: CustomerCreate) -> Customer:
        data = payload.model_dump(exclude_none=True)
        if "email" in data:
            data["email"] = data["email"].lower()
        await self._check_email(data.get("email"))
        async with self._guard("No se pudo crear el cliente (email duplicado)"):
            obj = await self.repo.add(Customer(**data))
            await self.session.commit()
        return await self.get(obj.customer_id)

    async def list(self, *, is_active, search, limit: int, offset: int):
        return await self.repo.search(is_active=is_active, search=search, limit=limit, offset=offset)

    async def get(self, customer_id: int) -> Customer:
        return await self._get_or_404(self.repo, customer_id, "Cliente")

    async def update(self, customer_id: int, payload: CustomerUpdate) -> Customer:
        obj = await self._get_or_404(self.repo, customer_id, "Cliente")
        changes = payload.changes()
        if changes.get("email"):
            changes["email"] = changes["email"].lower()
        await self._check_email(changes.get("email"), exclude_id=customer_id)
        async with self._guard("No se pudo actualizar el cliente (email duplicado)"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return await self.get(customer_id)

    async def delete(self, customer_id: int) -> None:
        """Borrado lógico (idempotente). No se puede desactivar con mascotas activas."""
        obj = await self._get_or_404(self.repo, customer_id, "Cliente")
        if not obj.is_active:
            return
        if await self.pets.exists_where(Pet.customer_id == customer_id, Pet.is_active.is_(True)):
            raise ConflictError("No se puede desactivar: el cliente tiene mascotas activas")
        await self.repo.update(obj, {"is_active": False})
        await self.session.commit()
