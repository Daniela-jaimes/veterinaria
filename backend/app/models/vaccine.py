from sqlalchemy import (
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Vaccine(Base):
    __tablename__ = "vaccine"
    __table_args__ = (UniqueConstraint("name", "manufacturer", name="uq_vaccine_name_manufacturer"),)

    vaccine_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    manufacturer: Mapped[str | None] = mapped_column(String(100))
