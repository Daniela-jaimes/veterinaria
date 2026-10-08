from datetime import datetime
from typing import ClassVar

from pydantic import Field

from app.schemas.common import Email100, InputModel, ORMModel, UpdateModel


class CustomerCreate(InputModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone: str | None = Field(None, max_length=20)
    email: Email100 | None = None
    address: str | None = Field(None, max_length=200)
    emergency_contact: str | None = Field(None, max_length=20)


class CustomerUpdate(UpdateModel):
    nullable_fields: ClassVar[frozenset[str]] = frozenset({"phone", "email", "address", "emergency_contact"})
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
    phone: str | None = Field(None, max_length=20)
    email: Email100 | None = None
    address: str | None = Field(None, max_length=200)
    emergency_contact: str | None = Field(None, max_length=20)
    is_active: bool | None = None


class CustomerResponse(ORMModel):
    customer_id: int
    first_name: str
    last_name: str
    phone: str | None
    email: str | None
    address: str | None
    emergency_contact: str | None
    is_active: bool
    created_at: datetime