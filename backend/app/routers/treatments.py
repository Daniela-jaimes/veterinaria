from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.models.enums import TreatmentStatus
from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.treatment import TreatmentCreate, TreatmentResponse, TreatmentUpdate
from app.services.treatment_service import TreatmentService

router = APIRouter(prefix="/treatments", tags=["Treatments"])


def get_service(session: SessionDep) -> TreatmentService:
    return TreatmentService(session)


ServiceDep = Annotated[TreatmentService, Depends(get_service)]


@router.post("", response_model=TreatmentResponse, status_code=status.HTTP_201_CREATED)
async def create_treatment(payload: TreatmentCreate, service: ServiceDep):
    """Crea un tratamiento (estado inicial 'active'). 404 si la consulta o el medicamento no existen."""
    return await service.create(payload)


@router.get("", response_model=Page[TreatmentResponse])
async def list_treatments(
    pagination: PaginationDep,
    service: ServiceDep,
    consultation_id: int | None = Query(None, ge=1, description="Filtra por consulta"),
    medication_id: int | None = Query(None, ge=1, description="Filtra por medicamento"),
    pet_id: int | None = Query(None, ge=1, description="Filtra por mascota"),
    status_: TreatmentStatus | None = Query(None, alias="status", description="Filtra por estado"),
):
    """Lista tratamientos (con su medicamento) con paginación y filtros."""
    items, total = await service.list(
        consultation_id=consultation_id, medication_id=medication_id, pet_id=pet_id,
        status=status_, limit=pagination.limit, offset=pagination.offset,
    )
    return pagination.wrap(items, total)


@router.get("/{treatment_id}", response_model=TreatmentResponse)
async def get_treatment(treatment_id: IdPath, service: ServiceDep):
    """Obtiene un tratamiento por ID. 404 si no existe."""
    return await service.get(treatment_id)


@router.put("/{treatment_id}", response_model=TreatmentResponse)
async def update_treatment(treatment_id: IdPath, payload: TreatmentUpdate, service: ServiceDep):
    """Actualiza un tratamiento (solo los campos enviados). 400 si las fechas son incoherentes."""
    return await service.update(treatment_id, payload)


@router.delete("/{treatment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def suspend_treatment(treatment_id: IdPath, service: ServiceDep):
    """Borrado lógico: el tratamiento pasa a 'suspended'. 409 si ya está completado."""
    await service.delete(treatment_id)