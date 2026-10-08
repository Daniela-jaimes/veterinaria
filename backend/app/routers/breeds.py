from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.models.enums import PetSpecies
from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.breed import BreedCreate, BreedResponse, BreedUpdate
from app.schemas.common import Page
from app.services.breed_service import BreedService

router = APIRouter(prefix="/breeds", tags=["Breeds"])


def get_service(session: SessionDep) -> BreedService:
    return BreedService(session)


ServiceDep = Annotated[BreedService, Depends(get_service)]


@router.post("", response_model=BreedResponse, status_code=status.HTTP_201_CREATED)
async def create_breed(payload: BreedCreate, service: ServiceDep):
    """Crea una raza. 409 si ya existe esa raza para la misma especie."""
    return await service.create(payload)


@router.get("", response_model=Page[BreedResponse])
async def list_breeds(
    pagination: PaginationDep,
    service: ServiceDep,
    species: PetSpecies | None = Query(None, description="Filtra por especie"),
    name: str | None = Query(None, description="Búsqueda parcial por nombre"),
):
    """Lista razas con paginación y filtros por especie y nombre."""
    items, total = await service.list(species=species, name=name, limit=pagination.limit, offset=pagination.offset)
    return pagination.wrap(items, total)


@router.get("/{breed_id}", response_model=BreedResponse)
async def get_breed(breed_id: IdPath, service: ServiceDep):
    """Obtiene una raza por ID. 404 si no existe."""
    return await service.get(breed_id)


@router.put("/{breed_id}", response_model=BreedResponse)
async def update_breed(breed_id: IdPath, payload: BreedUpdate, service: ServiceDep):
    """Actualiza una raza (solo los campos enviados). 404 / 409."""
    return await service.update(breed_id, payload)


@router.delete("/{breed_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_breed(breed_id: IdPath, service: ServiceDep):
    """Elimina una raza. 409 si hay mascotas con esa raza."""
    await service.delete(breed_id)
