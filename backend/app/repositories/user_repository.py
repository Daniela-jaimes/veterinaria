from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.models.enums import UserRole
from app.models import AppUser
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[AppUser]):
    model = AppUser
    pk_name = "user_id"
    DETAIL = (joinedload(AppUser.vet),)

    async def search(
        self, *, role: UserRole | None, is_active: bool | None, search: str | None, limit: int, offset: int
    ):
        where = []
        if role:
            where.append(AppUser.role == role)
        if is_active is not None:
            where.append(AppUser.is_active == is_active)
        if search:
            pattern = f"%{search}%"
            where.append(AppUser.username.ilike(pattern) | AppUser.email.ilike(pattern))
        return await self.get_page(
            where=where, order_by=[AppUser.username], limit=limit, offset=offset, options=self.DETAIL
        )

    async def get_by_username(self, username: str, exclude_id: int | None = None) -> AppUser | None:
        conds = [func.lower(AppUser.username) == username.lower()]
        if exclude_id is not None:
            conds.append(AppUser.user_id != exclude_id)
        return await self.first(*conds)

    async def get_by_email(self, email: str, exclude_id: int | None = None) -> AppUser | None:
        conds = [func.lower(AppUser.email) == email.lower()]
        if exclude_id is not None:
            conds.append(AppUser.user_id != exclude_id)
        return await self.first(*conds)

    async def get_by_vet(self, vet_id: int, exclude_id: int | None = None) -> AppUser | None:
        conds = [AppUser.vet_id == vet_id]
        if exclude_id is not None:
            conds.append(AppUser.user_id != exclude_id)
        return await self.first(*conds)
