from sqlalchemy import func

from app.models import Medication
from app.repositories.base import BaseRepository


class MedicationRepository(BaseRepository[Medication]):
    model = Medication
    pk_name = "medication_id"

    async def search(self, *, name: str | None, limit: int, offset: int):
        where = []
        if name:
            where.append(Medication.name.ilike(f"%{name}%"))
        return await self.get_page(where=where, order_by=[Medication.name], limit=limit, offset=offset)

    async def get_by_name(self, name: str, exclude_id: int | None = None) -> Medication | None:
        conds = [func.lower(Medication.name) == name.lower()]
        if exclude_id is not None:
            conds.append(Medication.medication_id != exclude_id)
        return await self.first(*conds)
