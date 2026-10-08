from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.pet_allergy import PetAllergyCreate, PetAllergyResponse, PetAllergyUpdate
from app.services.pet_allergy_service import PetAllergyService

router = APIRouter(prefix="/pet-allergies", tags=["Pet allergies"])


def get_service(session: SessionDep) -> PetAllergyService:
    return PetAllergyService(session)


ServiceDep = Annotated[PetAllergyService, Depends(get_service)]


@router.post("", response_model=PetAllergyResponse, status_code=status.HTTP_201_CREATED)
async def create_pet_allergy(payload: PetAllergyCreate, service: ServiceDep):
    """Registra una alergia de una mascota. 404 si no existe la mascota; 409 si la alergia ya está registrada."""
    return await service.create(payload)


@router.get("", response_model=Page[PetAllergyResponse])
async def list_pet_allergies(
    pagination: PaginationDep,
    service: ServiceDep,
    pet_id: int | None = Query(None, ge=1, description="Filtra por mascota"),
    search: str | None = Query(None, description="Búsqueda parcial por descripción"),
):
    """Lista alergias con paginación y filtros por mascota y descripción."""
    items, total = await service.list(
        pet_id=pet_id, search=search, limit=pagination.limit, offset=pagination.offset
    )
    return pagination.wrap(items, total)


@router.get("/{allergy_id}", response_model=PetAllergyResponse)
async def get_pet_allergy(allergy_id: IdPath, service: ServiceDep):
    """Obtiene una alergia por ID. 404 si no existe."""
    return await service.get(allergy_id)


@router.put("/{allergy_id}", response_model=PetAllergyResponse)
async def update_pet_allergy(allergy_id: IdPath, payload: PetAllergyUpdate, service: ServiceDep):
    """Actualiza la descripción de una alergia (la mascota no se puede cambiar). 404 / 409."""
    return await service.update(allergy_id, payload)


@router.delete("/{allergy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet_allergy(allergy_id: IdPath, service: ServiceDep):
    """Elimina una alergia."""
    await service.delete(allergy_id)
