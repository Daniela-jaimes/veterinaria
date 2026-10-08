from pydantic import BaseModel, ConfigDict


class PetAllergyBase(BaseModel):
    pet_id: int
    description: str


class PetAllergyCreate(PetAllergyBase):
    pass


class PetAllergyUpdate(PetAllergyBase):
    pass


class PetAllergyResponse(PetAllergyBase):
    allergy_id: int

    model_config = ConfigDict(from_attributes=True)