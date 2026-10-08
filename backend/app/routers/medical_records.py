from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordResponse, MedicalRecordUpdate
from app.services.medical_record_service import MedicalRecordService

router = APIRouter(prefix="/medical-records", tags=["Medical records"])


def get_service(session: SessionDep) -> MedicalRecordService:
    return MedicalRecordService(session)


ServiceDep = Annotated[MedicalRecordService, Depends(get_service)]


@router.post("", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_medical_record(payload: MedicalRecordCreate, service: ServiceDep):
    """Crea la historia clínica de una mascota. 404 si no existe la mascota; 409 si ya tiene una."""
    return await service.create(payload)


@router.get("", response_model=Page[MedicalRecordResponse])
async def list_medical_records(
    pagination: PaginationDep,
    service: ServiceDep,
    pet_id: int | None = Query(None, ge=1, description="Filtra por mascota"),
):
    """Lista historias clínicas con paginación y filtro por mascota."""
    items, total = await service.list(pet_id=pet_id, limit=pagination.limit, offset=pagination.offset)
    return pagination.wrap(items, total)


@router.get("/{medical_record_id}", response_model=MedicalRecordResponse)
async def get_medical_record(medical_record_id: IdPath, service: ServiceDep):
    """Obtiene una historia clínica por ID. 404 si no existe."""
    return await service.get(medical_record_id)


@router.put("/{medical_record_id}", response_model=MedicalRecordResponse)
async def update_medical_record(medical_record_id: IdPath, payload: MedicalRecordUpdate, service: ServiceDep):
    """Actualiza opened_on y/o general_notes (la mascota no se puede cambiar)."""
    return await service.update(medical_record_id, payload)


@router.delete("/{medical_record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medical_record(medical_record_id: IdPath, service: ServiceDep):
    """Elimina una historia clínica. 409 si tiene consultas asociadas."""
    await service.delete(medical_record_id)
