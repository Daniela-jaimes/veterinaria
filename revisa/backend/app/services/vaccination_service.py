from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError
from app.models import Vaccination
from app.repositories.consultation_repository import ConsultationRepository
from app.repositories.vaccination_repository import VaccinationRepository
from app.repositories.vaccine_repository import VaccineRepository
from app.schemas.vaccination import VaccinationCreate, VaccinationUpdate
from app.services.base import BaseService

DUPLICATE_MSG = "Esa vacuna ya está registrada en la misma consulta"


class VaccinationService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = VaccinationRepository(session)
        self.consultations = ConsultationRepository(session)
        self.vaccines = VaccineRepository(session)

    async def create(self, payload: VaccinationCreate) -> Vaccination:
        await self._get_or_404(self.consultations, payload.consultation_id, "Consulta")
        await self._get_or_404(self.vaccines, payload.vaccine_id, "Vacuna")
        if await self.repo.get_duplicate(payload.consultation_id, payload.vaccine_id):
            raise ConflictError(DUPLICATE_MSG)
        async with self._guard("No se pudo crear la vacunación"):
            obj = await self.repo.add(Vaccination(**payload.model_dump(exclude_none=True)))
            await self.session.commit()
        return await self.get(obj.vaccination_id)

    async def list(self, *, consultation_id, vaccine_id, pet_id, date_from, date_to, limit: int, offset: int):
        return await self.repo.search(
            consultation_id=consultation_id, vaccine_id=vaccine_id, pet_id=pet_id,
            date_from=date_from, date_to=date_to, limit=limit, offset=offset,
        )

    async def get(self, vaccination_id: int) -> Vaccination:
        return await self._get_or_404(self.repo, vaccination_id, "Vacunación", self.repo.DETAIL)

    async def update(self, vaccination_id: int, payload: VaccinationUpdate) -> Vaccination:
        obj = await self._get_or_404(self.repo, vaccination_id, "Vacunación")
        changes = payload.changes()

        if "vaccine_id" in changes:
            await self._get_or_404(self.vaccines, changes["vaccine_id"], "Vacuna")
            if await self.repo.get_duplicate(obj.consultation_id, changes["vaccine_id"], exclude_id=vaccination_id):
                raise ConflictError(DUPLICATE_MSG)

        given: date = changes.get("date_given", obj.date_given)
        due: date | None = changes["next_due_date"] if "next_due_date" in changes else obj.next_due_date
        if due is not None and due < given:
            raise BadRequestError("next_due_date no puede ser anterior a date_given")

        async with self._guard("No se pudo actualizar la vacunación"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return await self.get(vaccination_id)

    async def delete(self, vaccination_id: int) -> None:
        await self._hard_delete(self.repo, vaccination_id, "Vacunación", "No se pudo eliminar la vacunación")
