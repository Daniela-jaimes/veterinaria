from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.models import Veterinarian
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.speciality_repository import SpecialityRepository
from app.repositories.veterinarian_repository import VeterinarianRepository
from app.schemas.veterinarian import VeterinarianCreate, VeterinarianUpdate
from app.services.base import BaseService


class VeterinarianService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = VeterinarianRepository(session)
        self.specialities = SpecialityRepository(session)
        self.appointments = AppointmentRepository(session)

    async def _check_unique(self, license_number: str | None, email: str | None, exclude_id: int | None = None):
        if license_number and await self.repo.get_by_license(license_number, exclude_id):
            raise ConflictError(f"Ya existe un veterinario con la licencia '{license_number}'")
        if email and await self.repo.get_by_email(email, exclude_id):
            raise ConflictError(f"Ya existe un veterinario con el email '{email}'")

    async def _check_can_deactivate(self, vet_id: int) -> None:
        if await self.appointments.has_upcoming_for_vet(vet_id):
            raise ConflictError("No se puede desactivar: el veterinario tiene citas futuras pendientes")

    async def create(self, payload: VeterinarianCreate) -> Veterinarian:
        await self._get_or_404(self.specialities, payload.speciality_id, "Especialidad")
        data = payload.model_dump(exclude_none=True)
        if "email" in data:
            data["email"] = data["email"].lower()
        await self._check_unique(data["license_number"], data.get("email"))
        async with self._guard("No se pudo crear el veterinario (licencia o email duplicado)"):
            obj = await self.repo.add(Veterinarian(**data))
            await self.session.commit()
        return await self.get(obj.vet_id)

    async def list(self, *, speciality_id: int | None, is_active: bool | None, search: str | None,
                   limit: int, offset: int):
        return await self.repo.search(
            speciality_id=speciality_id, is_active=is_active, search=search, limit=limit, offset=offset
        )

    async def get(self, vet_id: int) -> Veterinarian:
        return await self._get_or_404(self.repo, vet_id, "Veterinario", self.repo.DETAIL)

    async def update(self, vet_id: int, payload: VeterinarianUpdate) -> Veterinarian:
        obj = await self._get_or_404(self.repo, vet_id, "Veterinario")
        changes = payload.changes()
        if changes.get("email"):
            changes["email"] = changes["email"].lower()
        if "speciality_id" in changes:
            await self._get_or_404(self.specialities, changes["speciality_id"], "Especialidad")
        await self._check_unique(changes.get("license_number"), changes.get("email"), exclude_id=vet_id)
        if changes.get("is_active") is False and obj.is_active:
            await self._check_can_deactivate(vet_id)
        async with self._guard("No se pudo actualizar el veterinario (licencia o email duplicado)"):
            await self.repo.update(obj, changes)
            await self.session.commit()
        return await self.get(vet_id)

    async def delete(self, vet_id: int) -> None:
        """Borrado lógico: is_active = false (idempotente)."""
        obj = await self._get_or_404(self.repo, vet_id, "Veterinario")
        if not obj.is_active:
            return
        await self._check_can_deactivate(vet_id)
        await self.repo.update(obj, {"is_active": False})
        await self.session.commit()
