from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError
from app.models.enums import TreatmentStatus
from app.models import Treatment
from app.repositories.consultation_repository import ConsultationRepository
from app.repositories.medication_repository import MedicationRepository
from app.repositories.treatment_repository import TreatmentRepository
from app.schemas.treatment import TreatmentCreate, TreatmentUpdate
from app.services.base import BaseService


class TreatmentService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = TreatmentRepository(session)
        self.consultations = ConsultationRepository(session)
        self.medications = MedicationRepository(session)

    async def create(self, payload: TreatmentCreate) -> Treatment:
        await self._get_or_404(self.consultations, payload.consultation_id, "Consulta")
        await self._get_or_404(self.medications, payload.medication_id, "Medicamento")
        async with self._guard("No se pudo crear el tratamiento"):
            obj = await self.repo.add(Treatment(**payload.model_dump(exclude_none=True)))
            await self.session.commit()
        return await self.get(obj.treatment_id)

    async def list(self, *, consultation_id, medication_id, pet_id, status, limit: int, offset: int):
        return await self.repo.search(
            consultation_id=consultation_id, medication_id=medication_id, pet_id=pet_id,
            status=status, limit=limit, offset=offset,
        )

    async def get(self, treatment_id: int) -> Treatment:
        return await self._get_or_404(self.repo, treatment_id, "Tratamiento", self.repo.DETAIL)

    async def update(self, treatment_id: int, payload: TreatmentUpdate) -> Treatment:
        obj = await self._get_or_404(self.repo, treatment_id, "Tratamiento")
        changes = payload.changes()

        if "medication_id" in changes:
            await self._get_or_404(self.medications, changes["medication_id"], "Medicamento")

        start: date = changes.get("start_date", obj.start_date)
        end: date | None = changes["end_date"] if "end_date" in changes else obj.end_date
        if end is not None and end < start:
            raise BadRequestError("end_date no puede ser anterior a start_date")

        new_status = changes.get("status")
        if obj.status == TreatmentStatus.completed and new_status not in (None, TreatmentStatus.completed):
            raise ConflictError("Un tratamiento completado no puede volver a activarse ni suspenderse")

        async with self._guard("No se pudo actualizar el tratamiento"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return await self.get(treatment_id)

    async def delete(self, treatment_id: int) -> None:
        """Borrado lógico: el tratamiento pasa a 'suspended' (idempotente)."""
        obj = await self._get_or_404(self.repo, treatment_id, "Tratamiento")
        if obj.status == TreatmentStatus.suspended:
            return
        if obj.status == TreatmentStatus.completed:
            raise ConflictError("No se puede suspender un tratamiento ya completado")
        await self.repo.update(obj, {"status": TreatmentStatus.suspended})
        await self.session.commit()
