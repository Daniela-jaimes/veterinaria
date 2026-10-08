from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.routers.deps import CurrentUser, SessionDep
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_service(session: SessionDep) -> AuthService:
    return AuthService(session)


ServiceDep = Annotated[AuthService, Depends(get_service)]


@router.post("/login", response_model=TokenResponse)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], service: ServiceDep):
    """Inicia sesión con `username` y `password` (formulario). Devuelve un token Bearer (JWT).

    401 si las credenciales son incorrectas o el usuario está inactivo.
    """
    return await service.login(form.username, form.password)


@router.get("/me", response_model=UserResponse)
async def me(user: CurrentUser):
    """Devuelve el usuario autenticado."""
    return user
