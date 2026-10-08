from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.speciality import SpecialityCreate, SpecialityResponse, SpecialityUpdate
from app.services.speciality_service import SpecialityService

router = APIRouter(prefix="/specialities", tags=["Specialities"])


def get_service(session: SessionDep) -> SpecialityService:
    return SpecialityService(session)


ServiceDep = Annotated[SpecialityService, Depends(get_service)]


@router.post("", response_model=SpecialityResponse, status_code=status.HTTP_201_CREATED)
async def create_speciality(payload: SpecialityCreate, service: ServiceDep):
    """Crea una especialidad. 409 si ya existe una con el mismo nombre (sin distinguir mayúsculas)."""
    return await service.create(payload)


@router.get("", response_model=Page[SpecialityResponse])
async def list_specialities(
    pagination: PaginationDep,
    service: ServiceDep,
    name: str | None = Query(None, description="Búsqueda parcial por nombre"),
):
    """Lista especialidades con paginación y filtro opcional por nombre."""
    items, total = await service.list(name=name, limit=pagination.limit, offset=pagination.offset)
    return pagination.wrap(items, total)


@router.get("/{speciality_id}", response_model=SpecialityResponse)
async def get_speciality(speciality_id: IdPath, service: ServiceDep):
    """Obtiene una especialidad por ID. 404 si no existe."""
    return await service.get(speciality_id)


@router.put("/{speciality_id}", response_model=SpecialityResponse)
async def update_speciality(speciality_id: IdPath, payload: SpecialityUpdate, service: ServiceDep):
    """Actualiza una especialidad (solo los campos enviados). 404 / 409."""
    return await service.update(speciality_id, payload)


@router.delete("/{speciality_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_speciality(speciality_id: IdPath, service: ServiceDep):
    """Elimina una especialidad. 409 si tiene veterinarios asociados."""
    await service.delete(speciality_id)