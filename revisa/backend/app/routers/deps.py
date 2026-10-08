from typing import Annotated, Any

from fastapi import Depends, Path, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token
from app.models import AppUser
from app.models.enums import UserRole
from app.repositories.user_repository import UserRepository

SessionDep = Annotated[AsyncSession, Depends(get_session)]

# id de ruta válido para un INTEGER de Postgres
IdPath = Annotated[int, Path(ge=1, le=2_147_483_647, description="Identificador del recurso")]


class Pagination:
    """Paginación limit/offset reutilizable en todos los listados."""

    def __init__(
        self,
        limit: int = Query(20, ge=1, le=100, description="Máximo de registros a devolver"),
        offset: int = Query(0, ge=0, description="Registros a omitir"),
    ):
        self.limit = limit
        self.offset = offset

    def wrap(self, items: list[Any], total: int) -> dict[str, Any]:
        return {"items": items, "total": total, "limit": self.limit, "offset": self.offset}


PaginationDep = Annotated[Pagination, Depends()]


# ---------------------------------------------------------------------------
# Autenticación / autorización
# ---------------------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> AppUser:
    """Valida el JWT y devuelve el usuario activo. 401 si el token es inválido/expirado o el usuario ya no existe."""
    payload = decode_access_token(token)
    try:
        user_id = int(payload["sub"])
    except (KeyError, ValueError, TypeError) as exc:
        raise UnauthorizedError() from exc
    user = await UserRepository(session).get(user_id, UserRepository.DETAIL)
    if user is None or not user.is_active:
        raise UnauthorizedError()
    return user


CurrentUser = Annotated[AppUser, Depends(get_current_user)]


def require_roles(*roles: UserRole):
    """Dependencia que exige que el usuario autenticado tenga uno de los roles dados (403 si no)."""

    async def checker(user: CurrentUser) -> AppUser:
        if user.role not in roles:
            raise ForbiddenError()
        return user

    return checker
