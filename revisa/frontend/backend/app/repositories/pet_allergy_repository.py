from sqlalchemy import func

from app.models import PetAllergy
from app.repositories.base import BaseRepository


class PetAllergyRepository(BaseRepository[PetAllergy]):
    model = PetAllergy
    pk_name = "allergy_id"

    async def search(self, *, pet_id: int | None, search: str | None, limit: int, offset: int):
        where = []
        if pet_id is not None:
            where.append(PetAllergy.pet_id == pet_id)
        if search:
            where.append(PetAllergy.description.ilike(f"%{search}%"))
        return await self.get_page(
            where=where, order_by=[PetAllergy.pet_id, PetAllergy.description], limit=limit, offset=offset
        )

    async def get_duplicate(
        self, pet_id: int, description: str, exclude_id: int | None = None
    ) -> PetAllergy | None:
        conds = [PetAllergy.pet_id == pet_id, func.lower(PetAllergy.description) == description.lower()]
        if exclude_id is not None:
            conds.append(PetAllergy.allergy_id != exclude_id)
        return await self.first(*conds)
