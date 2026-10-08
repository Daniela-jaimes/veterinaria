from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload

from app.models import Veterinarian
from app.repositories.base import BaseRepository


class VeterinarianRepository(BaseRepository[Veterinarian]):
    model = Veterinarian
    pk_name = "vet_id"
    DETAIL = (joinedload(Veterinarian.speciality),)

    async def search(
        self, *, speciality_id: int | None, is_active: bool | None, search: str | None, limit: int, offset: int
    ):
        where = []
        if speciality_id is not None:
            where.append(Veterinarian.speciality_id == speciality_id)
        if is_active is not None:
            where.append(Veterinarian.is_active == is_active)
        if search:
            pattern = f"%{search}%"
            where.append(
                or_(
                    Veterinarian.first_name.ilike(pattern),
                    Veterinarian.last_name.ilike(pattern),
                    Veterinarian.license_number.ilike(pattern),
                )
            )
        return await self.get_page(
            where=where, order_by=[Veterinarian.last_name, Veterinarian.first_name],
            limit=limit, offset=offset, options=self.DETAIL,
        )

    async def get_by_license(self, license_number: str, exclude_id: int | None = None) -> Veterinarian | None:
        conds = [func.lower(Veterinarian.license_number) == license_number.lower()]
        if exclude_id is not None:
            conds.append(Veterinarian.vet_id != exclude_id)
        return await self.first(*conds)

    async def get_by_email(self, email: str, exclude_id: int | None = None) -> Veterinarian | None:
        conds = [func.lower(Veterinarian.email) == email.lower()]
        if exclude_id is not None:
            conds.append(Veterinarian.vet_id != exclude_id)
        return await self.first(*conds)
