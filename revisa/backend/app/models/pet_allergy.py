from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PetAllergy(Base):
    __tablename__ = "pet_allergy"

    allergy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("pet.pet_id", ondelete="CASCADE"), nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=False)
