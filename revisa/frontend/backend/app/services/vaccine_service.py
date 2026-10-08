from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.models import Vaccine
from app.repositories.vaccine_repository import VaccineRepository
from app.schemas.vaccine import VaccineCreate, VaccineUpdate
from app.services.base import BaseService


class VaccineService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = VaccineRepository(session)

    async def create(self, payload: VaccineCreate) -> Vaccine:
        if await self.repo.get_duplicate(payload.name, payload.manufacturer):
            raise ConflictError("Ya existe una vacuna con ese nombre y fabricante")
        async with self._guard("No se pudo crear la vacuna (registro duplicado)"):
            obj = await self.repo.add(Vaccine(**payload.model_dump()))
            await self.session.commit()
        return obj

    async def list(self, *, name: str | None, manufacturer: str | None, limit: int, offset: int):
        return await self.repo.search(name=name, manufacturer=manufacturer, limit=limit, offset=offset)

    async def get(self, vaccine_id: int) -> Vaccine:
        return await self._get_or_404(self.repo, vaccine_id, "Vacuna")

    async def update(self, vaccine_id: int, payload: VaccineUpdate) -> Vaccine:
        obj = await self.get(vaccine_id)
        changes = payload.changes()
        name = changes.get("name", obj.name)
        manufacturer = changes["manufacturer"] if "manufacturer" in changes else obj.manufacturer
        if await self.repo.get_duplicate(name, manufacturer, exclude_id=vaccine_id):
            raise ConflictError("Ya existe una vacuna con ese nombre y fabricante")
        async with self._guard("No se pudo actualizar la vacuna (registro duplicado)"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return obj

    async def delete(self, vaccine_id: int) -> None:
        await self._hard_delete(
            self.repo, vaccine_id, "Vacuna", "No se puede eliminar: la vacuna tiene vacunaciones registradas"
        )
