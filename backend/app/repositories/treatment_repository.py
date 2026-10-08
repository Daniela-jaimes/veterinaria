from sqlalchemy.orm import joinedload

from app.models.enums import TreatmentStatus
from app.models import Treatment
from app.repositories.base import BaseRepository
from app.repositories.consultation_repository import consultation_ids_for_pet


class TreatmentRepository(BaseRepository[Treatment]):
    model = Treatment
    pk_name = "treatment_id"
    DETAIL = (joinedload(Treatment.medication),)

    async def search(
        self,
        *,
        consultation_id: int | None,
        medication_id: int | None,
        pet_id: int | None,
        status: TreatmentStatus | None,
        limit: int,
        offset: int,
    ):
        where = []
        if consultation_id is not None:
            where.append(Treatment.consultation_id == consultation_id)
        if medication_id is not None:
            where.append(Treatment.medication_id == medication_id)
        if pet_id is not None:
            where.append(Treatment.consultation_id.in_(consultation_ids_for_pet(pet_id)))
        if status is not None:
            where.append(Treatment.status == status)
        return await self.get_page(
            where=where, order_by=[Treatment.start_date.desc()], limit=limit, offset=offset, options=self.DETAIL
        )
