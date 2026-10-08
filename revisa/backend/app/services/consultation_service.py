from datetime import date, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError
from app.models.enums import AppointmentStatus
from app.models import Consultation
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.consultation_repository import ConsultationRepository
from app.repositories.medical_record_repository import MedicalRecordRepository
from app.repositories.veterinarian_repository import VeterinarianRepository
from app.schemas.consultation import ConsultationCreate, ConsultationUpdate
from app.services.base import BaseService


class ConsultationService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = ConsultationRepository(session)
        self.records = MedicalRecordRepository(session)
        self.vets = VeterinarianRepository(session)
        self.appointments = AppointmentRepository(session)

    async def _check_vet(self, vet_id: int) -> None:
        vet = await self._get_or_404(self.vets, vet_id, "Veterinario")
        if not vet.is_active:
            raise BadRequestError("El veterinario está inactivo")

    @staticmethod
    def _check_next_checkup(next_checkup: date | None, consultation_date: datetime) -> None:
        if next_checkup is not None and next_checkup < consultation_date.date():
            raise BadRequestError("next_checkup no puede ser anterior a la fecha de la consulta")

    async def create(self, payload: ConsultationCreate) -> Consultation:
        record = await self._get_or_404(self.records, payload.medical_record_id, "Historia clínica")
        await self._check_vet(payload.vet_id)
        self._check_next_checkup(payload.next_checkup, payload.consultation_date or datetime.now())

        async with self._guard("No se pudo crear la consulta (la cita ya tiene una consulta asociada)"):
            if payload.appointment_id is not None:
                appt = await self._get_or_404(self.appointments, payload.appointment_id, "Cita")
                if appt.pet_id != record.pet_id:
                    raise BadRequestError("La cita corresponde a una mascota distinta a la de la historia clínica")
                if appt.status in (AppointmentStatus.cancelled, AppointmentStatus.no_show):
                    raise BadRequestError(f"No se puede crear una consulta sobre una cita '{appt.status.value}'")
                if await self.repo.get_by_appointment(payload.appointment_id):
                    raise ConflictError("La cita ya tiene una consulta asociada")
                if appt.status == AppointmentStatus.scheduled:
                    appt.status = AppointmentStatus.in_consultation  # la cita pasa a atenderse
            obj = await self.repo.add(Consultation(**payload.model_dump(exclude_none=True)))
            await self.session.commit()
        return await self.get(obj.consultation_id)

    async def list(self, *, medical_record_id, pet_id, vet_id, consultation_type, date_from, date_to,
                   limit: int, offset: int):
        return await self.repo.search(
            medical_record_id=medical_record_id, pet_id=pet_id, vet_id=vet_id,
            consultation_type=consultation_type, date_from=date_from, date_to=date_to,
            limit=limit, offset=offset,
        )

    async def get(self, consultation_id: int) -> Consultation:
        return await self._get_or_404(self.repo, consultation_id, "Consulta", self.repo.DETAIL)

    async def update(self, consultation_id: int, payload: ConsultationUpdate) -> Consultation:
        obj = await self._get_or_404(self.repo, consultation_id, "Consulta")
        changes = payload.changes()
        if "vet_id" in changes:
            await self._check_vet(changes["vet_id"])
        self._check_next_checkup(
            changes["next_checkup"] if "next_checkup" in changes else obj.next_checkup,
            changes.get("consultation_date", obj.consultation_date),
        )
        async with self._guard("No se pudo actualizar la consulta"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return await self.get(consultation_id)

    async def delete(self, consultation_id: int) -> None:
        await self._hard_delete(
            self.repo, consultation_id, "Consulta",
            "No se puede eliminar: la consulta tiene tratamientos o vacunaciones asociados",
        )
