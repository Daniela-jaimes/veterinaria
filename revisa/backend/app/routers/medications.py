from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.medication import MedicationCreate, MedicationResponse, MedicationUpdate
from app.services.medication_service import MedicationService

router = APIRouter(prefix="/medications", tags=["Medications"])


def get_service(session: SessionDep) -> MedicationService:
    return MedicationService(session)


ServiceDep = Annotated[MedicationService, Depends(get_service)]


@router.post("", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
async def create_medication(payload: MedicationCreate, service: ServiceDep):
    """Crea un medicamento. 409 si el nombre ya existe."""
    return await service.create(payload)


@router.get("", response_model=Page[MedicationResponse])
async def list_medications(
    pagination: PaginationDep,
    service: ServiceDep,
    name: str | None = Query(None, description="Búsqueda parcial por nombre"),
):
    """Lista medicamentos con paginación y filtro opcional por nombre."""
    items, total = await service.list(name=name, limit=pagination.limit, offset=pagination.offset)
    return pagination.wrap(items, total)


@router.get("/{medication_id}", response_model=MedicationResponse)
async def get_medication(medication_id: IdPath, service: ServiceDep):
    """Obtiene un medicamento por ID. 404 si no existe."""
    return await service.get(medication_id)


@router.put("/{medication_id}", response_model=MedicationResponse)
async def update_medication(medication_id: IdPath, payload: MedicationUpdate, service: ServiceDep):
    """Actualiza un medicamento (solo los campos enviados). 404 / 409."""
    return await service.update(medication_id, payload)


@router.delete("/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medication(medication_id: IdPath, service: ServiceDep):
    """Elimina un medicamento. 409 si está usado en tratamientos."""
    await service.delete(medication_id)
