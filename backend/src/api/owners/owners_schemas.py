from pydantic import BaseModel, ConfigDict


class OwnerBase(BaseModel):
    name: str
    description: str
    price: int


class OwnerCreate(OwnerBase):
    pass


class OwnerUpdate(OwnerCreate):
    pass


class OwnerUpdatePartial(OwnerCreate):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class Owner(OwnerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
