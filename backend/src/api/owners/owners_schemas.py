from pydantic import BaseModel, ConfigDict


class OwnerBase(BaseModel):
    name: str
    email: str
    phone: str
    is_verified: bool
    password: str


class OwnerCreate(OwnerBase):
    pass


class OwnerUpdate(OwnerCreate):
    pass


class OwnerUpdatePartial(OwnerCreate):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    is_verified: bool | None = None
    password: str | None = None


class Owner(OwnerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
