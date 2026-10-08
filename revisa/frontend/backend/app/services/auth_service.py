from datetime import datetime

from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.models import AppUser
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse
from app.services.base import BaseService

_DUMMY_HASH = hash_password("contraseña-de-relleno")


class AuthService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.users = UserRepository(session)

    async def login(self, username: str, password: str) -> TokenResponse:
        user: AppUser | None = await self.users.get_by_username(username.strip())
        hash_to_check = user.password_hash if user else _DUMMY_HASH
        try:
            valid = await run_in_threadpool(verify_password, password, hash_to_check)
        except ValueError:  # hash almacenado con formato inválido
            valid = False
        if user is None or not valid or not user.is_active:
            raise UnauthorizedError("Usuario o contraseña incorrectos")

        user.last_login = datetime.now()
        await self.session.commit()

        token = create_access_token(subject=str(user.user_id), role=user.role.value)
        full_user = await self.users.get(user.user_id, UserRepository.DETAIL)  # carga la relación `vet`
        return TokenResponse(
            access_token=token,
            expires_in=settings.access_token_expire_minutes * 60,
            user=full_user,
        )
