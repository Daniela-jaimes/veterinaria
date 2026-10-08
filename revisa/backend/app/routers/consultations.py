from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.models.enums import ConsultationType
from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.consultation import ConsultationCreate, ConsultationResponse, ConsultationUpdate
from app.services.consultation_service import ConsultationService

router = APIRouter(prefix="/consultations", tags=["Consultations"])


def get_service(session: SessionDep) -> ConsultationService:
    return ConsultationService(session)


ServiceDep = Annotated[ConsultationService, Depends(get_service)]


@router.post("", response_model=ConsultationResponse, status_code=status.HTTP_201_CREATED)
async def create_consultation(payload: ConsultationCreate, service: ServiceDep):
    """Registra una consulta.

    404 si historia clínica, veterinario o cita no existen; 400 si la cita es de otra mascota o está
    cancelada/no_show; 409 si la cita ya tiene consulta. Si la cita estaba 'scheduled' pasa a 'in_consultation'.
    """
    return await service.create(payload)


@router.get("", response_model=Page[ConsultationResponse])
async def list_consultations(
    pagination: PaginationDep,
    service: ServiceDep,
    medical_record_id: int | None = Query(None, ge=1, description="Filtra por historia clínica"),
    pet_id: int | None = Query(None, ge=1, description="Filtra por mascota"),
    vet_id: int | None = Query(None, ge=1, description="Filtra por veterinario"),
    consultation_type: ConsultationType | None = Query(None, description="Filtra por tipo de consulta"),
    date_from: date | None = Query(None, description="Desde esta fecha (inclusive)"),
    date_to: date | None = Query(None, description="Hasta esta fecha (inclusive)"),
):
    """Lista consultas (con veterinario, tratamientos y vacunaciones), más recientes primero."""
    items, total = await service.list(
        medical_record_id=medical_record_id, pet_id=pet_id, vet_id=vet_id,
        consultation_type=consultation_type, date_from=date_from, date_to=date_to,
        limit=pagination.limit, offset=pagination.offset,
    )
    return pagination.wrap(items, total)


@router.get("/{consultation_id}", response_model=ConsultationResponse)
async def get_consultation(consultation_id: IdPath, service: ServiceDep):
    """Obtiene una consulta con sus tratamientos y vacunaciones. 404 si no existe."""
    return await service.get(consultation_id)


@router.put("/{consultation_id}", response_model=ConsultationResponse)
async def update_consultation(consultation_id: IdPath, payload: ConsultationUpdate, service: ServiceDep):
    """Actualiza una consulta (la historia clínica y la cita asociada no se pueden cambiar)."""
    return await service.update(consultation_id, payload)


@router.delete("/{consultation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_consultation(consultation_id: IdPath, service: ServiceDep):
    """Elimina una consulta. 409 si tiene tratamientos o vacunaciones asociados."""
    await service.delete(consultation_id)

