from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, pg_enum
from app.models.enums import PetSpecies


class Breed(Base):
    __tablename__ = "breed"
    __table_args__ = (UniqueConstraint("species", "name", name="uq_breed_species_name"),)

    breed_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    species: Mapped[PetSpecies] = mapped_column(pg_enum(PetSpecies, "pet_species"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
