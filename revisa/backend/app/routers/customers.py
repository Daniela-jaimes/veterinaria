from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.routers.deps import IdPath, PaginationDep, SessionDep
from app.schemas.common import Page
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


def get_service(session: SessionDep) -> CustomerService:
    return CustomerService(session)


ServiceDep = Annotated[CustomerService, Depends(get_service)]


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(payload: CustomerCreate, service: ServiceDep):
    """Crea un cliente. 409 si el email ya está registrado."""
    return await service.create(payload)


@router.get("", response_model=Page[CustomerResponse])
async def list_customers(
    pagination: PaginationDep,
    service: ServiceDep,
    is_active: bool | None = Query(None, description="Filtra por estado"),
    search: str | None = Query(None, description="Búsqueda parcial por nombre, email o teléfono"),
):
    """Lista clientes con paginación y filtros."""
    items, total = await service.list(
        is_active=is_active, search=search, limit=pagination.limit, offset=pagination.offset
    )
    return pagination.wrap(items, total)


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: IdPath, service: ServiceDep):
    """Obtiene un cliente por ID. 404 si no existe."""
    return await service.get(customer_id)


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(customer_id: IdPath, payload: CustomerUpdate, service: ServiceDep):
    """Actualiza un cliente (solo los campos enviados). 404 / 409."""
    return await service.update(customer_id, payload)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: IdPath, service: ServiceDep):
    """Desactiva un cliente (borrado lógico). 409 si tiene mascotas activas."""
    await service.delete(customer_id)
