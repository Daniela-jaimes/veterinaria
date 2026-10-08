from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.speciality import Speciality


class Veterinarian(Base):
    __tablename__ = "veterinarian"

    vet_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    speciality_id: Mapped[int] = mapped_column(
        ForeignKey("speciality.speciality_id", ondelete="RESTRICT"), nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    license_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(150), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))

    speciality: Mapped["Speciality"] = relationship(lazy="raise")
