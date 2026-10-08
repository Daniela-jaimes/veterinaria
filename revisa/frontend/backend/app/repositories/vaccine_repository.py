from sqlalchemy import func

from app.models import Vaccine
from app.repositories.base import BaseRepository


class VaccineRepository(BaseRepository[Vaccine]):
    model = Vaccine
    pk_name = "vaccine_id"

    async def search(self, *, name: str | None, manufacturer: str | None, limit: int, offset: int):
        where = []
        if name:
            where.append(Vaccine.name.ilike(f"%{name}%"))
        if manufacturer:
            where.append(Vaccine.manufacturer.ilike(f"%{manufacturer}%"))
        return await self.get_page(where=where, order_by=[Vaccine.name], limit=limit, offset=offset)

    async def get_duplicate(self, name: str, manufacturer: str | None, exclude_id: int | None = None) -> Vaccine | None:
        # En Postgres UNIQUE(name, manufacturer) no detecta duplicados con manufacturer NULL:
        # se comprueba aquí tratando NULL como un valor más.
        conds = [func.lower(Vaccine.name) == name.lower()]
        if manufacturer is None:
            conds.append(Vaccine.manufacturer.is_(None))
        else:
            conds.append(func.lower(Vaccine.manufacturer) == manufacturer.lower())
        if exclude_id is not None:
            conds.append(Vaccine.vaccine_id != exclude_id)
        return await self.first(*conds)
