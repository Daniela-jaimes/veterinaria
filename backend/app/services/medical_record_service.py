from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError
from app.models import MedicalRecord
from app.repositories.medical_record_repository import MedicalRecordRepository
from app.repositories.pet_repository import PetRepository
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate
from app.services.base import BaseService


class MedicalRecordService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = MedicalRecordRepository(session)
        self.pets = PetRepository(session)

    async def create(self, payload: MedicalRecordCreate) -> MedicalRecord:
        pet = await self._get_or_404(self.pets, payload.pet_id, "Mascota")
        if not pet.is_active:
            raise BadRequestError("La mascota está inactiva")
        if await self.repo.get_by_pet(payload.pet_id):
            raise ConflictError("La mascota ya tiene una historia clínica")
        async with self._guard("No se pudo crear la historia clínica (la mascota ya tiene una)"):
            obj = await self.repo.add(MedicalRecord(**payload.model_dump(exclude_none=True)))
            await self.session.commit()
        return await self.get(obj.medical_record_id)

    async def list(self, *, pet_id: int | None, limit: int, offset: int):
        return await self.repo.search(pet_id=pet_id, limit=limit, offset=offset)

    async def get(self, medical_record_id: int) -> MedicalRecord:
        return await self._get_or_404(self.repo, medical_record_id, "Historia clínica", self.repo.DETAIL)

    async def update(self, medical_record_id: int, payload: MedicalRecordUpdate) -> MedicalRecord:
        obj = await self._get_or_404(self.repo, medical_record_id, "Historia clínica")
        async with self._guard("No se pudo actualizar la historia clínica"):
            await self.repo.update(obj, payload.changes())
            await self.session.commit()
        return await self.get(medical_record_id)

    async def delete(self, medical_record_id: int) -> None:
        await self._hard_delete(
            self.repo, medical_record_id, "Historia clínica",
            "No se puede eliminar: la historia clínica tiene consultas asociadas",
        )
