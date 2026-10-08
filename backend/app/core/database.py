from collections.abc import AsyncIterator

from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


def _build_url(raw_url: str) -> URL:
    """Convierte una URL estándar de Postgres/Neon a una URL válida para asyncpg.
    """
    url = make_url(raw_url).set(drivername="postgresql+asyncpg")
    query = {k: v for k, v in url.query.items() if k not in {"sslmode", "channel_binding", "ssl"}}
    query["prepared_statement_cache_size"] = "0"
    return url.set(query=query)


engine = create_async_engine(
    _build_url(settings.database_url),
    pool_pre_ping=True,
    connect_args={
        "ssl": "require" if settings.db_ssl else "disable",
        "statement_cache_size": 0,
    },
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Dependencia de FastAPI: una sesión por request (los servicios hacen commit)."""
    async with SessionLocal() as session:
        yield session
