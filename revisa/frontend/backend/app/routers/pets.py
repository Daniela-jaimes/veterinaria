from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.pet import PetCreate, PetResponse, PetUpdate
from app.services.pet_service import PetService

router = APIRouter(prefix="/pets", tags=["Pets"])


def get_service(session: SessionDep) -> PetService:
    return PetService(session)


ServiceDep = Annotated[PetService, Depends(get_service)]


@router.post("", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(payload: PetCreate, service: ServiceDep):
    """Crea una mascota. 404 si el cliente o la raza no existen; 409 si el microchip está duplicado."""
    return await service.create(payload)


@router.get("", response_model=Page[PetResponse])
async def list_pets(
    pagination: PaginationDep,
    service: ServiceDep,
    customer_id: int | None = Query(None, ge=1, description="Filtra por dueño"),
    breed_id: int | None = Query(None, ge=1, description="Filtra por raza"),
    is_active: bool | None = Query(None, description="Filtra por estado"),
    search: str | None = Query(None, description="Búsqueda parcial por nombre"),
):
    """Lista mascotas con paginación y filtros."""
    items, total = await service.list(
        customer_id=customer_id, breed_id=breed_id, is_active=is_active, search=search,
        limit=pagination.limit, offset=pagination.offset,
    )
    return pagination.wrap(items, total)


@router.get("/{pet_id}", response_model=PetResponse)
async def get_pet(pet_id: IdPath, service: ServiceDep):
    """Obtiene una mascota por ID. 404 si no existe."""
    return await service.get(pet_id)


@router.put("/{pet_id}", response_model=PetResponse)
async def update_pet(pet_id: IdPath, payload: PetUpdate, service: ServiceDep):
    """Actualiza una mascota (solo los campos enviados). 404 / 409."""
    return await service.update(pet_id, payload)


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(pet_id: IdPath, service: ServiceDep):
    """Desactiva una mascota (borrado lógico)."""
    await service.delete(pet_id)
