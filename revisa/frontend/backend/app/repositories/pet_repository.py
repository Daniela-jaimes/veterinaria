from app.models import Pet
from app.repositories.base import BaseRepository


class PetRepository(BaseRepository[Pet]):
    model = Pet
    pk_name = "pet_id"

    async def search(
        self,
        *,
        customer_id: int | None,
        breed_id: int | None,
        is_active: bool | None,
        search: str | None,
        limit: int,
        offset: int,
    ):
        where = []
        if customer_id is not None:
            where.append(Pet.customer_id == customer_id)
        if breed_id is not None:
            where.append(Pet.breed_id == breed_id)
        if is_active is not None:
            where.append(Pet.is_active == is_active)
        if search:
            where.append(Pet.name.ilike(f"%{search}%"))
        return await self.get_page(where=where, order_by=[Pet.name], limit=limit, offset=offset)

    async def get_by_microchip(self, microchip: str, exclude_id: int | None = None) -> Pet | None:
        conds = [Pet.microchip_number == microchip]
        if exclude_id is not None:
            conds.append(Pet.pet_id != exclude_id)
        return await self.first(*conds)
