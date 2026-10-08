from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.vaccination import VaccinationCreate, VaccinationResponse, VaccinationUpdate
from app.services.vaccination_service import VaccinationService

router = APIRouter(prefix="/vaccinations", tags=["Vaccinations"])


def get_service(session: SessionDep) -> VaccinationService:
    return VaccinationService(session)


ServiceDep = Annotated[VaccinationService, Depends(get_service)]


@router.post("", response_model=VaccinationResponse, status_code=status.HTTP_201_CREATED)
async def create_vaccination(payload: VaccinationCreate, service: ServiceDep):
    """Registra una vacunación. 404 si consulta o vacuna no existen; 409 si esa vacuna ya está en la consulta."""
    return await service.create(payload)


@router.get("", response_model=Page[VaccinationResponse])
async def list_vaccinations(
    pagination: PaginationDep,
    service: ServiceDep,
    consultation_id: int | None = Query(None, ge=1, description="Filtra por consulta"),
    vaccine_id: int | None = Query(None, ge=1, description="Filtra por vacuna"),
    pet_id: int | None = Query(None, ge=1, description="Carnet de vacunación de una mascota"),
    date_from: date | None = Query(None, description="Aplicadas desde (inclusive)"),
    date_to: date | None = Query(None, description="Aplicadas hasta (inclusive)"),
):
    """Lista vacunaciones (con su vacuna) con paginación y filtros."""
    items, total = await service.list(
        consultation_id=consultation_id, vaccine_id=vaccine_id, pet_id=pet_id,
        date_from=date_from, date_to=date_to, limit=pagination.limit, offset=pagination.offset,
    )
    return pagination.wrap(items, total)


@router.get("/{vaccination_id}", response_model=VaccinationResponse)
async def get_vaccination(vaccination_id: IdPath, service: ServiceDep):
    """Obtiene una vacunación por ID. 404 si no existe."""
    return await service.get(vaccination_id)


@router.put("/{vaccination_id}", response_model=VaccinationResponse)
async def update_vaccination(vaccination_id: IdPath, payload: VaccinationUpdate, service: ServiceDep):
    """Actualiza una vacunación (la consulta no se puede cambiar)."""
    return await service.update(vaccination_id, payload)


@router.delete("/{vaccination_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vaccination(vaccination_id: IdPath, service: ServiceDep):
    """Elimina una vacunación."""
    await service.delete(vaccination_id)