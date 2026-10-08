from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine
from app.models.enums import UserRole
from app.routers.deps import get_current_user, require_roles
from app.routers import (
    appointments,
    auth,
    breeds,
    consultations,
    customers,
    medical_records,
    medications,
    pet_allergies,
    pets,
    specialitis,
    treatments,
    users,
    vaccinations,
    vaccines,
    veterinarians,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="Sistema de Gestión de Clínica Veterinaria",
    description="API REST para la gestión de una clínica veterinaria",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Todos los recursos exigen un usuario autenticado (Bearer token).
protected = [Depends(get_current_user)]
for module in (
    customers, pets, pet_allergies, appointments, breeds, consultations, medical_records, medications,
    specialitis, treatments, vaccinations, vaccines, veterinarians,
):
    app.include_router(module.router, dependencies=protected)

# La gestión de usuarios es solo para administradores.
app.include_router(users.router, dependencies=[Depends(require_roles(UserRole.admin))])

# Login y /auth/me (el login es público; /auth/me valida el token por su cuenta).
app.include_router(auth.router)


@app.get("/", tags=["Health"])
async def root():
    return {"mensaje": "API de Clínica Veterinaria funcionando", "version": "1.0.0"}


@app.get("/db-test", tags=["Health"])
async def database_test():
    """Comprueba la conexión con PostgreSQL usando el engine async."""
    try:
        async with engine.connect() as connection:
            value = (await connection.execute(text("SELECT 1"))).scalar()
        return {"mensaje": "Conexión con PostgreSQL exitosa", "resultado": value}
    except Exception as exc:
        return {"mensaje": "Error al conectar con PostgreSQL", "error": str(exc)}
