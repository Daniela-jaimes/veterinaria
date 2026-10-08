from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError
from app.core.security import hash_password
from app.models.enums import UserRole
from app.models import AppUser
from app.repositories.user_repository import UserRepository
from app.repositories.veterinarian_repository import VeterinarianRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = UserRepository(session)
        self.vets = VeterinarianRepository(session)

    async def _check_unique(self, username: str | None, email: str | None, exclude_id: int | None = None):
        if username and await self.repo.get_by_username(username, exclude_id):
            raise ConflictError(f"El nombre de usuario '{username}' ya está en uso")
        if email and await self.repo.get_by_email(email, exclude_id):
            raise ConflictError(f"El email '{email}' ya está en uso")

    async def _check_vet(self, vet_id: int, exclude_user_id: int | None = None) -> None:
        vet = await self._get_or_404(self.vets, vet_id, "Veterinario")
        if not vet.is_active:
            raise BadRequestError("El veterinario está inactivo")
        if await self.repo.get_by_vet(vet_id, exclude_user_id):
            raise ConflictError("Ese veterinario ya tiene un usuario asociado")

    async def create(self, payload: UserCreate) -> AppUser:
        email = payload.email.lower()
        await self._check_unique(payload.username, email)
        if payload.vet_id is not None:
            await self._check_vet(payload.vet_id)
        data = payload.model_dump(exclude={"password"}, exclude_none=True)
        data["email"] = email
        # bcrypt es CPU-bound: se ejecuta en un hilo para no bloquear el event loop
        data["password_hash"] = await run_in_threadpool(hash_password, payload.password)
        async with self._guard("No se pudo crear el usuario (username o email duplicado)"):
            obj = await self.repo.add(AppUser(**data))
            await self.session.commit()
        return await self.get(obj.user_id)

    async def list(self, *, role: UserRole | None, is_active: bool | None, search: str | None,
                   limit: int, offset: int):
        return await self.repo.search(role=role, is_active=is_active, search=search, limit=limit, offset=offset)

    async def get(self, user_id: int) -> AppUser:
        return await self._get_or_404(self.repo, user_id, "Usuario", self.repo.DETAIL)

    async def update(self, user_id: int, payload: UserUpdate) -> AppUser:
        obj = await self._get_or_404(self.repo, user_id, "Usuario")
        changes = payload.changes()

        if changes.get("email"):
            changes["email"] = changes["email"].lower()
        await self._check_unique(changes.get("username"), changes.get("email"), exclude_id=user_id)

        role = changes.get("role", obj.role)
        vet_id = changes["vet_id"] if "vet_id" in changes else obj.vet_id
        if role == UserRole.veterinarian and vet_id is None:
            raise BadRequestError("vet_id es obligatorio cuando el rol es 'veterinarian'")
        if changes.get("vet_id") is not None:
            await self._check_vet(changes["vet_id"], exclude_user_id=user_id)

        if "password" in changes:
            changes["password_hash"] = await run_in_threadpool(hash_password, changes.pop("password"))

        async with self._guard("No se pudo actualizar el usuario (username o email duplicado)"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return await self.get(user_id)

    async def delete(self, user_id: int) -> None:
        """Borrado lógico: is_active = false (idempotente)."""
        obj = await self._get_or_404(self.repo, user_id, "Usuario")
        if obj.is_active:
            await self.repo.update(obj, {"is_active": False})
            await self.session.commit()
