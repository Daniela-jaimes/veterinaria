from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.models.enums import UserRole
from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_service(session: SessionDep) -> UserService:
    return UserService(session)


ServiceDep = Annotated[UserService, Depends(get_service)]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, service: ServiceDep):
    """Crea un usuario (la contraseña se hashea con bcrypt en el servicio).

    404 si el veterinario no existe; 409 si username/email ya están en uso o el veterinario ya tiene usuario.
    """
    return await service.create(payload)


@router.get("", response_model=Page[UserResponse])
async def list_users(
    pagination: PaginationDep,
    service: ServiceDep,
    role: UserRole | None = Query(None, description="Filtra por rol"),
    is_active: bool | None = Query(None, description="Filtra por estado activo/inactivo"),
    search: str | None = Query(None, description="Búsqueda parcial por username o email"),
):
    """Lista usuarios con paginación y filtros. Nunca devuelve password_hash."""
    items, total = await service.list(
        role=role, is_active=is_active, search=search, limit=pagination.limit, offset=pagination.offset
    )
    return pagination.wrap(items, total)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: IdPath, service: ServiceDep):
    """Obtiene un usuario por ID. 404 si no existe."""
    return await service.get(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: IdPath, payload: UserUpdate, service: ServiceDep):
    """Actualiza un usuario (solo los campos enviados). Si se envía password, se vuelve a hashear."""
    return await service.update(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: IdPath, service: ServiceDep):
    """Borrado lógico (is_active=false)."""
    await service.delete(user_id)