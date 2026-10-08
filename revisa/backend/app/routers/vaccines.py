from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.vaccine import VaccineCreate, VaccineResponse, VaccineUpdate
from app.services.vaccine_service import VaccineService

router = APIRouter(prefix="/vaccines", tags=["Vaccines"])


def get_service(session: SessionDep) -> VaccineService:
    return VaccineService(session)


ServiceDep = Annotated[VaccineService, Depends(get_service)]


@router.post("", response_model=VaccineResponse, status_code=status.HTTP_201_CREATED)
async def create_vaccine(payload: VaccineCreate, service: ServiceDep):
    """Crea una vacuna. 409 si ya existe el par (nombre, fabricante)."""
    return await service.create(payload)


@router.get("", response_model=Page[VaccineResponse])
async def list_vaccines(
    pagination: PaginationDep,
    service: ServiceDep,
    name: str | None = Query(None, description="Búsqueda parcial por nombre"),
    manufacturer: str | None = Query(None, description="Búsqueda parcial por fabricante"),
):
    """Lista vacunas con paginación y filtros por nombre y fabricante."""
    items, total = await service.list(
        name=name, manufacturer=manufacturer, limit=pagination.limit, offset=pagination.offset
    )
    return pagination.wrap(items, total)


@router.get("/{vaccine_id}", response_model=VaccineResponse)
async def get_vaccine(vaccine_id: IdPath, service: ServiceDep):
    """Obtiene una vacuna por ID. 404 si no existe."""
    return await service.get(vaccine_id)


@router.put("/{vaccine_id}", response_model=VaccineResponse)
async def update_vaccine(vaccine_id: IdPath, payload: VaccineUpdate, service: ServiceDep):
    """Actualiza una vacuna (solo los campos enviados). 404 / 409."""
    return await service.update(vaccine_id, payload)


@router.delete("/{vaccine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vaccine(vaccine_id: IdPath, service: ServiceDep):
    """Elimina una vacuna. 409 si tiene vacunaciones registradas."""
    await service.delete(vaccine_id)