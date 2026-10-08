from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.models import Medication
from app.repositories.medication_repository import MedicationRepository
from app.schemas.medication import MedicationCreate, MedicationUpdate
from app.services.base import BaseService


class MedicationService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = MedicationRepository(session)

    async def create(self, payload: MedicationCreate) -> Medication:
        if await self.repo.get_by_name(payload.name):
            raise ConflictError(f"Ya existe un medicamento llamado '{payload.name}'")
        async with self._guard("No se pudo crear el medicamento (registro duplicado)"):
            obj = await self.repo.add(Medication(**payload.model_dump()))
            await self.session.commit()
        return obj

    async def list(self, *, name: str | None, limit: int, offset: int):
        return await self.repo.search(name=name, limit=limit, offset=offset)

    async def get(self, medication_id: int) -> Medication:
        return await self._get_or_404(self.repo, medication_id, "Medicamento")

    async def update(self, medication_id: int, payload: MedicationUpdate) -> Medication:
        obj = await self.get(medication_id)
        changes = payload.changes()
        if "name" in changes and await self.repo.get_by_name(changes["name"], exclude_id=medication_id):
            raise ConflictError(f"Ya existe un medicamento llamado '{changes['name']}'")
        async with self._guard("No se pudo actualizar el medicamento (registro duplicado)"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return obj

    async def delete(self, medication_id: int) -> None:
        await self._hard_delete(
            self.repo, medication_id, "Medicamento",
            "No se puede eliminar: el medicamento está usado en tratamientos",
        )
