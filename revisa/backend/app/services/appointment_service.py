from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError
from app.models.enums import AppointmentStatus as S
from app.models import Appointment
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.pet_repository import PetRepository
from app.repositories.veterinarian_repository import VeterinarianRepository
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.services.base import BaseService

# Máquina de estados de una cita
ALLOWED_TRANSITIONS: dict[S, set[S]] = {
    S.scheduled: {S.in_consultation, S.cancelled, S.no_show},
    S.in_consultation: {S.completed, S.cancelled},
    S.completed: set(),
    S.cancelled: set(),
    S.no_show: set(),
}
RESCHEDULE_FIELDS = {"pet_id", "vet_id", "scheduled_at", "duration_minutes"}


class AppointmentService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = AppointmentRepository(session)
        self.pets = PetRepository(session)
        self.vets = VeterinarianRepository(session)

    async def _validate_refs(self, pet_id: int, vet_id: int) -> None:
        pet = await self._get_or_404(self.pets, pet_id, "Mascota")
        if not pet.is_active:
            raise BadRequestError("La mascota está inactiva")
        vet = await self._get_or_404(self.vets, vet_id, "Veterinario")
        if not vet.is_active:
            raise BadRequestError("El veterinario está inactivo")

    async def _ensure_free_slot(self, vet_id: int, start: datetime, minutes: int, exclude_id: int | None = None):
        if await self.repo.has_overlap(vet_id, start, minutes, exclude_id):
            raise ConflictError("El veterinario ya tiene una cita en ese horario")

    async def create(self, payload: AppointmentCreate) -> Appointment:
        await self._validate_refs(payload.pet_id, payload.vet_id)
        await self._ensure_free_slot(payload.vet_id, payload.scheduled_at, payload.duration_minutes)
        async with self._guard("No se pudo crear la cita"):
            obj = await self.repo.add(Appointment(**payload.model_dump(exclude_none=True)))
            await self.session.commit()
        return await self.get(obj.appointment_id)

    async def list(self, *, vet_id, pet_id, status, date_from, date_to, limit: int, offset: int):
        return await self.repo.search(
            vet_id=vet_id, pet_id=pet_id, status=status,
            date_from=date_from, date_to=date_to, limit=limit, offset=offset,
        )

    async def get(self, appointment_id: int) -> Appointment:
        return await self._get_or_404(self.repo, appointment_id, "Cita", self.repo.DETAIL)

    async def update(self, appointment_id: int, payload: AppointmentUpdate) -> Appointment:
        obj = await self._get_or_404(self.repo, appointment_id, "Cita")
        changes = payload.changes()

        new_status = changes.get("status")
        if new_status is None or new_status == obj.status:
            changes.pop("status", None)
        elif new_status not in ALLOWED_TRANSITIONS[obj.status]:
            raise BadRequestError(f"Transición de estado no permitida: {obj.status.value} → {new_status.value}")

        if RESCHEDULE_FIELDS & changes.keys():
            if obj.status != S.scheduled:
                raise ConflictError("Solo se puede modificar mascota, veterinario u horario de una cita 'scheduled'")
            pet_id = changes.get("pet_id", obj.pet_id)
            vet_id = changes.get("vet_id", obj.vet_id)
            start = changes.get("scheduled_at", obj.scheduled_at)
            minutes = changes.get("duration_minutes", obj.duration_minutes)
            await self._validate_refs(pet_id, vet_id)
            await self._ensure_free_slot(vet_id, start, minutes, exclude_id=appointment_id)

        async with self._guard("No se pudo actualizar la cita"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return await self.get(appointment_id)

    async def delete(self, appointment_id: int) -> None:
        """Borrado lógico: la cita pasa a 'cancelled' (idempotente)."""
        obj = await self._get_or_404(self.repo, appointment_id, "Cita")
        if obj.status == S.cancelled:
            return
        if S.cancelled not in ALLOWED_TRANSITIONS[obj.status]:
            raise ConflictError(f"No se puede cancelar una cita en estado '{obj.status.value}'")
        await self.repo.update(obj, {"status": S.cancelled})
        await self.session.commit()
