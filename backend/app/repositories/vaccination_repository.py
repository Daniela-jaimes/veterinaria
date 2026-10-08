from datetime import date

from sqlalchemy.orm import joinedload

from app.models import Vaccination
from app.repositories.base import BaseRepository
from app.repositories.consultation_repository import consultation_ids_for_pet


class VaccinationRepository(BaseRepository[Vaccination]):
    model = Vaccination
    pk_name = "vaccination_id"
    DETAIL = (joinedload(Vaccination.vaccine),)

    async def search(
        self,
        *,
        consultation_id: int | None,
        vaccine_id: int | None,
        pet_id: int | None,
        date_from: date | None,
        date_to: date | None,
        limit: int,
        offset: int,
    ):
        where = []
        if consultation_id is not None:
            where.append(Vaccination.consultation_id == consultation_id)
        if vaccine_id is not None:
            where.append(Vaccination.vaccine_id == vaccine_id)
        if pet_id is not None:
            where.append(Vaccination.consultation_id.in_(consultation_ids_for_pet(pet_id)))
        if date_from is not None:
            where.append(Vaccination.date_given >= date_from)
        if date_to is not None:
            where.append(Vaccination.date_given <= date_to)
        return await self.get_page(
            where=where, order_by=[Vaccination.date_given.desc()], limit=limit, offset=offset, options=self.DETAIL
        )

    async def get_duplicate(self, consultation_id: int, vaccine_id: int, exclude_id: int | None = None):
        conds = [Vaccination.consultation_id == consultation_id, Vaccination.vaccine_id == vaccine_id]
        if exclude_id is not None:
            conds.append(Vaccination.vaccination_id != exclude_id)
        return await self.first(*conds)
