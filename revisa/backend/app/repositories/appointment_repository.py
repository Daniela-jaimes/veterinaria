from datetime import date, datetime, time, timedelta

from sqlalchemy import Interval, func, literal_column
from sqlalchemy.orm import joinedload

from app.models.enums import AppointmentStatus
from app.models import Appointment
from app.repositories.base import BaseRepository

# Estados que ocupan la agenda del veterinario
ACTIVE_STATUSES = (AppointmentStatus.scheduled, AppointmentStatus.in_consultation)


class AppointmentRepository(BaseRepository[Appointment]):
    model = Appointment
    pk_name = "appointment_id"
    DETAIL = (joinedload(Appointment.pet), joinedload(Appointment.vet))

    async def search(
        self,
        *,
        vet_id: int | None,
        pet_id: int | None,
        status: AppointmentStatus | None,
        date_from: date | None,
        date_to: date | None,
        limit: int,
        offset: int,
    ):
        where = []
        if vet_id is not None:
            where.append(Appointment.vet_id == vet_id)
        if pet_id is not None:
            where.append(Appointment.pet_id == pet_id)
        if status is not None:
            where.append(Appointment.status == status)
        if date_from is not None:
            where.append(Appointment.scheduled_at >= datetime.combine(date_from, time.min))
        if date_to is not None:  # inclusivo: hasta el final de ese día
            where.append(Appointment.scheduled_at < datetime.combine(date_to + timedelta(days=1), time.min))
        return await self.get_page(
            where=where, order_by=[Appointment.scheduled_at], limit=limit, offset=offset, options=self.DETAIL
        )

    async def has_overlap(
        self, vet_id: int, start: datetime, minutes: int, exclude_id: int | None = None
    ) -> bool:
        """¿El veterinario ya tiene una cita activa que se solape con [start, start+minutes)?"""
        end = start + timedelta(minutes=minutes)
        zero = literal_column("0")
        existing_end = Appointment.scheduled_at + func.make_interval(zero, zero, zero, zero, zero, Appointment.duration_minutes, type_=Interval)
        conds = [
            Appointment.vet_id == vet_id,
            Appointment.status.in_(ACTIVE_STATUSES),
            Appointment.scheduled_at < end,
            existing_end > start,
        ]
        if exclude_id is not None:
            conds.append(Appointment.appointment_id != exclude_id)
        return await self.exists_where(*conds)

    async def has_upcoming_for_vet(self, vet_id: int) -> bool:
        return await self.exists_where(
            Appointment.vet_id == vet_id,
            Appointment.status.in_(ACTIVE_STATUSES),
            Appointment.scheduled_at >= datetime.now(),
        )
