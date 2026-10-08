from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.models import Speciality
from app.repositories.speciality_repository import SpecialityRepository
from app.schemas.speciality import SpecialityCreate, SpecialityUpdate
from app.services.base import BaseService


class SpecialityService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = SpecialityRepository(session)

    async def create(self, payload: SpecialityCreate) -> Speciality:
        if await self.repo.get_by_name(payload.name):
            raise ConflictError(f"Ya existe una especialidad llamada '{payload.name}'")
        async with self._guard("No se pudo crear la especialidad (registro duplicado)"):
            obj = await self.repo.add(Speciality(**payload.model_dump()))
            await self.session.commit()
        return obj

    async def list(self, *, name: str | None, limit: int, offset: int):
        return await self.repo.search(name=name, limit=limit, offset=offset)

    async def get(self, speciality_id: int) -> Speciality:
        return await self._get_or_404(self.repo, speciality_id, "Especialidad")

    async def update(self, speciality_id: int, payload: SpecialityUpdate) -> Speciality:
        obj = await self.get(speciality_id)
        changes = payload.changes()
        if "name" in changes and await self.repo.get_by_name(changes["name"], exclude_id=speciality_id):
            raise ConflictError(f"Ya existe una especialidad llamada '{changes['name']}'")
        async with self._guard("No se pudo actualizar la especialidad (registro duplicado)"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return obj

    async def delete(self, speciality_id: int) -> None:
        await self._hard_delete(
            self.repo, speciality_id, "Especialidad",
            "No se puede eliminar: hay veterinarios asociados a esta especialidad",
        )
