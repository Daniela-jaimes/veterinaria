from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import delete, exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

ModelT = TypeVar("ModelT", bound=DeclarativeBase)


class BaseRepository(Generic[ModelT]):
    """Acceso a datos genérico. Los repositorios concretos solo añaden filtros propios.

    Los repositorios hacen ``flush`` pero NUNCA ``commit``: la transacción la controla el servicio.
    """

    model: type[ModelT]
    pk_name: str

    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    def _pk(self):
        return getattr(self.model, self.pk_name)

    async def get(self, entity_id: int, options: Sequence[Any] = ()) -> ModelT | None:
        stmt = (
            select(self.model)
            .where(self._pk == entity_id)
            .options(*options)
            # evita relaciones obsoletas si el objeto ya estaba en el identity map
            .execution_options(populate_existing=True)
        )
        return (await self.session.execute(stmt)).unique().scalar_one_or_none()

    async def get_page(
        self,
        *,
        where: Sequence[Any] = (),
        order_by: Sequence[Any] = (),
        limit: int = 20,
        offset: int = 0,
        options: Sequence[Any] = (),
    ) -> tuple[list[ModelT], int]:
        total = (
            await self.session.execute(select(func.count()).select_from(self.model).where(*where))
        ).scalar_one()
        stmt = (
            select(self.model)
            .where(*where)
            .order_by(*order_by, self._pk)  # el pk desempata para paginar de forma estable
            .limit(limit)
            .offset(offset)
            .options(*options)
        )
        rows = (await self.session.execute(stmt)).unique().scalars().all()
        return list(rows), total

    async def first(self, *where: Any) -> ModelT | None:
        stmt = select(self.model).where(*where).limit(1)
        return (await self.session.execute(stmt)).scalars().first()

    async def exists_where(self, *where: Any) -> bool:
        return bool((await self.session.execute(select(exists().where(*where)))).scalar())

    async def add(self, obj: ModelT) -> ModelT:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(self, obj: ModelT, data: dict[str, Any]) -> ModelT:
        for key, value in data.items():
            setattr(obj, key, value)
        await self.session.flush()
        return obj

    async def delete_by_id(self, entity_id: int) -> None:
        """DELETE directo (sin cargar relaciones); las FK RESTRICT lanzan IntegrityError."""
        await self.session.execute(delete(self.model).where(self._pk == entity_id))
