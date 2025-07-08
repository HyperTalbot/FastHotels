from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    is_active: bool
    is_verified: bool
    # len_reviews: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    len_reviews: int | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
