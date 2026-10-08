from sqlalchemy.orm import joinedload

from app.models import MedicalRecord
from app.repositories.base import BaseRepository


class MedicalRecordRepository(BaseRepository[MedicalRecord]):
    model = MedicalRecord
    pk_name = "medical_record_id"
    DETAIL = (joinedload(MedicalRecord.pet),)

    async def search(self, *, pet_id: int | None, limit: int, offset: int):
        where = []
        if pet_id is not None:
            where.append(MedicalRecord.pet_id == pet_id)
        return await self.get_page(
            where=where, order_by=[MedicalRecord.opened_on.desc()], limit=limit, offset=offset, options=self.DETAIL
        )

    async def get_by_pet(self, pet_id: int) -> MedicalRecord | None:
        return await self.first(MedicalRecord.pet_id == pet_id)
