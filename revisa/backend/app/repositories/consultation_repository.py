from datetime import date, datetime, time, timedelta

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from app.models.enums import ConsultationType
from app.models import Consultation, MedicalRecord, Treatment, Vaccination
from app.repositories.base import BaseRepository


def consultation_ids_for_pet(pet_id: int):
    """Subquery con los ids de consulta de una mascota (vía su historia clínica)."""
    return (
        select(Consultation.consultation_id)
        .join(MedicalRecord, Consultation.medical_record_id == MedicalRecord.medical_record_id)
        .where(MedicalRecord.pet_id == pet_id)
    )


class ConsultationRepository(BaseRepository[Consultation]):
    model = Consultation
    pk_name = "consultation_id"
    # selectinload en colecciones (1 query extra por colección, sin N+1) y joinedload en many-to-one
    DETAIL = (
        joinedload(Consultation.vet),
        selectinload(Consultation.treatments).joinedload(Treatment.medication),
        selectinload(Consultation.vaccinations).joinedload(Vaccination.vaccine),
    )

    async def search(
        self,
        *,
        medical_record_id: int | None,
        pet_id: int | None,
        vet_id: int | None,
        consultation_type: ConsultationType | None,
        date_from: date | None,
        date_to: date | None,
        limit: int,
        offset: int,
    ):
        where = []
        if medical_record_id is not None:
            where.append(Consultation.medical_record_id == medical_record_id)
        if pet_id is not None:
            where.append(Consultation.consultation_id.in_(consultation_ids_for_pet(pet_id)))
        if vet_id is not None:
            where.append(Consultation.vet_id == vet_id)
        if consultation_type is not None:
            where.append(Consultation.consultation_type == consultation_type)
        if date_from is not None:
            where.append(Consultation.consultation_date >= datetime.combine(date_from, time.min))
        if date_to is not None:
            where.append(Consultation.consultation_date < datetime.combine(date_to + timedelta(days=1), time.min))
        return await self.get_page(
            where=where, order_by=[Consultation.consultation_date.desc()],
            limit=limit, offset=offset, options=self.DETAIL,
        )

    async def get_by_appointment(self, appointment_id: int) -> Consultation | None:
        return await self.first(Consultation.appointment_id == appointment_id)
