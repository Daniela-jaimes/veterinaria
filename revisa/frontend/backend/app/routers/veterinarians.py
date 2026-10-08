from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.veterinarian import VeterinarianCreate, VeterinarianResponse, VeterinarianUpdate
from app.services.veterinarian_service import VeterinarianService

router = APIRouter(prefix="/veterinarians", tags=["Veterinarians"])


def get_service(session: SessionDep) -> VeterinarianService:
    return VeterinarianService(session)


ServiceDep = Annotated[VeterinarianService, Depends(get_service)]


@router.post("", response_model=VeterinarianResponse, status_code=status.HTTP_201_CREATED)
async def create_veterinarian(payload: VeterinarianCreate, service: ServiceDep):
    """Crea un veterinario. 404 si la especialidad no existe; 409 si licencia o email ya existen."""
    return await service.create(payload)


@router.get("", response_model=Page[VeterinarianResponse])
async def list_veterinarians(
    pagination: PaginationDep,
    service: ServiceDep,
    speciality_id: int | None = Query(None, ge=1, description="Filtra por especialidad"),
    is_active: bool | None = Query(None, description="Filtra por estado activo/inactivo"),
    search: str | None = Query(None, description="Búsqueda parcial por nombre, apellido o licencia"),
):
    """Lista veterinarios (con su especialidad) con paginación y filtros."""
    items, total = await service.list(
        speciality_id=speciality_id, is_active=is_active, search=search,
        limit=pagination.limit, offset=pagination.offset,
    )
    return pagination.wrap(items, total)


@router.get("/{vet_id}", response_model=VeterinarianResponse)
async def get_veterinarian(vet_id: IdPath, service: ServiceDep):
    """Obtiene un veterinario por ID. 404 si no existe."""
    return await service.get(vet_id)


@router.put("/{vet_id}", response_model=VeterinarianResponse)
async def update_veterinarian(vet_id: IdPath, payload: VeterinarianUpdate, service: ServiceDep):
    """Actualiza un veterinario (solo los campos enviados; también permite reactivarlo con is_active=true)."""
    return await service.update(vet_id, payload)


@router.delete("/{vet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_veterinarian(vet_id: IdPath, service: ServiceDep):
    """Borrado lógico (is_active=false). 409 si tiene citas futuras pendientes."""
    await service.delete(vet_id)