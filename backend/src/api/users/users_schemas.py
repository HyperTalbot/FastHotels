from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    description: str
    price: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
