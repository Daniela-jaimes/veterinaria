from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.models.enums import AppointmentStatus
from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from app.schemas.common import Page
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Appointments"])


def get_service(session: SessionDep) -> AppointmentService:
    return AppointmentService(session)


ServiceDep = Annotated[AppointmentService, Depends(get_service)]


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(payload: AppointmentCreate, service: ServiceDep):
    """Agenda una cita (estado inicial 'scheduled').

    404 si mascota/veterinario no existen; 400 si alguno está inactivo;
    409 si el veterinario ya tiene una cita que se solapa en ese horario.
    """
    return await service.create(payload)


@router.get("", response_model=Page[AppointmentResponse])
async def list_appointments(
    pagination: PaginationDep,
    service: ServiceDep,
    vet_id: int | None = Query(None, ge=1, description="Filtra por veterinario"),
    pet_id: int | None = Query(None, ge=1, description="Filtra por mascota"),
    status_: AppointmentStatus | None = Query(None, alias="status", description="Filtra por estado"),
    date_from: date | None = Query(None, description="Citas desde esta fecha (inclusive)"),
    date_to: date | None = Query(None, description="Citas hasta esta fecha (inclusive)"),
):
    """Lista citas (con mascota y veterinario) ordenadas por fecha, con paginación y filtros."""
    items, total = await service.list(
        vet_id=vet_id, pet_id=pet_id, status=status_, date_from=date_from, date_to=date_to,
        limit=pagination.limit, offset=pagination.offset,
    )
    return pagination.wrap(items, total)


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(appointment_id: IdPath, service: ServiceDep):
    """Obtiene una cita por ID. 404 si no existe."""
    return await service.get(appointment_id)


@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(appointment_id: IdPath, payload: AppointmentUpdate, service: ServiceDep):
    """Actualiza una cita: reprogramar (solo 'scheduled') o cambiar de estado (400 si la transición no es válida)."""
    return await service.update(appointment_id, payload)


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_appointment(appointment_id: IdPath, service: ServiceDep):
    """Borrado lógico: la cita pasa a 'cancelled'. 409 si ya está completada o fue no_show."""
    await service.delete(appointment_id)