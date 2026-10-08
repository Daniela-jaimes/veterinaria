from collections.abc import Callable
from datetime import datetime
from typing import Annotated, Any, ClassVar, Generic, TypeVar

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, Field, model_validator

# FK / ids que caben en un INTEGER de Postgres
IdInt = Annotated[int, Field(ge=1, le=2_147_483_647)]


def _to_naive(value: datetime) -> datetime:
    """Las columnas son TIMESTAMP sin zona: se descarta el tzinfo (se conserva la hora de pared)."""
    return value.replace(tzinfo=None)


NaiveDatetime = Annotated[datetime, AfterValidator(_to_naive)]


def _max_len(limit: int) -> Callable[[str], str]:
    def check(value: str) -> str:
        if len(value) > limit:
            raise ValueError(f"Máximo {limit} caracteres")
        return value

    return check


Email100 = Annotated[EmailStr, AfterValidator(_max_len(100))]
Email150 = Annotated[EmailStr, AfterValidator(_max_len(150))]


class ORMModel(BaseModel):
    """Base de los schemas de respuesta."""
    model_config = ConfigDict(from_attributes=True)


class InputModel(BaseModel):
    """Base de los schemas Create."""
    model_config = ConfigDict(str_strip_whitespace=True)


class UpdateModel(InputModel):
    """Base de los schemas Update (PUT con semántica parcial: solo se aplican los campos enviados)."""

    nullable_fields: ClassVar[frozenset[str]] = frozenset()

    @model_validator(mode="after")
    def _validate_payload(self):
        if not self.model_fields_set:
            raise ValueError("Debe enviar al menos un campo a actualizar")
        for name in self.model_fields_set:
            if getattr(self, name) is None and name not in self.nullable_fields:
                raise ValueError(f"El campo '{name}' no puede ser null")
        return self

    def changes(self) -> dict[str, Any]:
        return self.model_dump(exclude_unset=True)


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    limit: int
    offset: int
