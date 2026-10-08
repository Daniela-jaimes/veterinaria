from sqlalchemy import func

from app.models import Speciality
from app.repositories.base import BaseRepository


class SpecialityRepository(BaseRepository[Speciality]):
    model = Speciality
    pk_name = "speciality_id"

    async def search(self, *, name: str | None, limit: int, offset: int):
        where = []
        if name:
            where.append(Speciality.name.ilike(f"%{name}%"))
        return await self.get_page(where=where, order_by=[Speciality.name], limit=limit, offset=offset)

    async def get_by_name(self, name: str, exclude_id: int | None = None) -> Speciality | None:
        conds = [func.lower(Speciality.name) == name.lower()]
        if exclude_id is not None:
            conds.append(Speciality.speciality_id != exclude_id)
        return await self.first(*conds)
