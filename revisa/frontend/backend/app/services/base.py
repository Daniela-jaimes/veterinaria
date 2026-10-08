from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.repositories.base import BaseRepository


class BaseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    @asynccontextmanager
    async def _guard(self, conflict_message: str) -> AsyncIterator[None]:
        """Traduce violaciones de integridad de la BD (UNIQUE / FK RESTRICT) a HTTP 409."""
        try:
            yield
        except IntegrityError as exc:
            await self.session.rollback()
            raise ConflictError(conflict_message) from exc

    @staticmethod
    async def _get_or_404(repo: BaseRepository, entity_id: int, label: str, options: Sequence[Any] = ()) -> Any:
        obj = await repo.get(entity_id, options)
        if obj is None:
            raise NotFoundError(label, entity_id)
        return obj

    async def _hard_delete(self, repo: BaseRepository, entity_id: int, label: str, conflict_message: str) -> None:
        await self._get_or_404(repo, entity_id, label)
        async with self._guard(conflict_message):
            await repo.delete_by_id(entity_id)
            await self.session.commit()
