from sqlalchemy import func, or_

from app.models import Customer
from app.repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    model = Customer
    pk_name = "customer_id"

    async def search(self, *, is_active: bool | None, search: str | None, limit: int, offset: int):
        where = []
        if is_active is not None:
            where.append(Customer.is_active == is_active)
        if search:
            pattern = f"%{search}%"
            where.append(
                or_(
                    Customer.first_name.ilike(pattern),
                    Customer.last_name.ilike(pattern),
                    Customer.email.ilike(pattern),
                    Customer.phone.ilike(pattern),
                )
            )
        return await self.get_page(
            where=where, order_by=[Customer.last_name, Customer.first_name], limit=limit, offset=offset
        )

    async def get_by_email(self, email: str, exclude_id: int | None = None) -> Customer | None:
        conds = [func.lower(Customer.email) == email.lower()]
        if exclude_id is not None:
            conds.append(Customer.customer_id != exclude_id)
        return await self.first(*conds)
