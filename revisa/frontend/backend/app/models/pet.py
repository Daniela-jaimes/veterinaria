from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, pg_enum
from app.models.enums import PetSex


class Pet(Base):
    __tablename__ = "pet"

    pet_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer.customer_id", ondelete="RESTRICT"), nullable=False
    )
    breed_id: Mapped[int] = mapped_column(
        ForeignKey("breed.breed_id", ondelete="RESTRICT"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date)
    sex: Mapped[PetSex] = mapped_column(
        pg_enum(PetSex, "pet_sex"), nullable=False, server_default=text("'unknown'")
    )
    microchip_number: Mapped[str | None] = mapped_column(String(20), unique=True)
    is_neutered: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
