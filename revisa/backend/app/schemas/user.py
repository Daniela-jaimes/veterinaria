from datetime import datetime
from typing import Annotated, ClassVar

from pydantic import AfterValidator, Field, model_validator

from app.models.enums import UserRole
from app.schemas.common import Email100, IdInt, InputModel, ORMModel, UpdateModel
from app.schemas.veterinarian import VeterinarianBrief


def _check_password_bytes(value: str) -> str:
    # bcrypt solo procesa los primeros 72 BYTES
    if len(value.encode("utf-8")) > 72:
        raise ValueError("La contraseña no puede exceder 72 bytes")
    return value


Password = Annotated[str, Field(min_length=8, max_length=72), AfterValidator(_check_password_bytes)]


class UserCreate(InputModel):
    username: str = Field(min_length=3, max_length=50)
    email: Email100
    password: Password
    role: UserRole = UserRole.receptionist
    vet_id: IdInt | None = None

    @model_validator(mode="after")
    def _vet_required_for_veterinarian(self):
        if self.role == UserRole.veterinarian and self.vet_id is None:
            raise ValueError("vet_id es obligatorio cuando el rol es 'veterinarian'")
        return self


class UserUpdate(UpdateModel):
    nullable_fields: ClassVar[frozenset[str]] = frozenset({"vet_id"})
    username: str | None = Field(None, min_length=3, max_length=50)
    email: Email100 | None = None
    password: Password | None = None
    role: UserRole | None = None
    vet_id: IdInt | None = None
    is_active: bool | None = None



class UserResponse(ORMModel):
    """Nunca expone password_hash."""
    user_id: int
    username: str
    email: str
    role: UserRole
    vet_id: int | None
    is_active: bool
    last_login: datetime | None
    created_at: datetime
    vet: VeterinarianBrief | None
